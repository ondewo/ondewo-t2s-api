# Copyright (c) 2019 NVIDIA Corporation
import argparse
import math
import os
from functools import partial

import nemo
import nemo.collections.asr as nemo_asr
import nemo.collections.tts as nemo_tts
import nemo.utils.argparse as nm_argparse
from nemo.collections.tts import (
    tacotron2_eval_log_to_tb_func,
    tacotron2_log_to_tb_func,
    tacotron2_process_eval_batch,
    tacotron2_process_final_eval,
)
from ruamel.yaml import YAML

from pylog.logger import logger_console as logger


def parse_args():
    parser = argparse.ArgumentParser(
        parents=[nm_argparse.NemoArgParser()], description='Tacotron2', conflict_handler='resolve',
    )
    args = parser.parse_args()

    # if args.lr_policy:
    #    raise NotImplementedError("Tacotron 2 does not support lr policy arg")
    if args.eval_freq % 25 != 0:
        raise ValueError("eval_freq should be a multiple of 25.")

    return args, "tacotron2_de_exp"


def create_NMs(tacotron2_config_file, labels, decoder_infer=False):
    data_preprocessor = nemo_asr.AudioToMelSpectrogramPreprocessor.import_from_config(
        tacotron2_config_file, "AudioToMelSpectrogramPreprocessor"
    )
    text_embedding = nemo_tts.TextEmbedding.import_from_config(
        tacotron2_config_file, "TextEmbedding", overwrite_params={"n_symbols": len(labels) + 3}
    )
    t2_enc = nemo_tts.Tacotron2Encoder.import_from_config(tacotron2_config_file, "Tacotron2Encoder")
    if decoder_infer:
        t2_dec = nemo_tts.Tacotron2DecoderInfer.import_from_config(tacotron2_config_file,
                                                                   "Tacotron2DecoderInfer")
    else:
        t2_dec = nemo_tts.Tacotron2Decoder.import_from_config(tacotron2_config_file, "Tacotron2Decoder")
    t2_postnet = nemo_tts.Tacotron2Postnet.import_from_config(tacotron2_config_file, "Tacotron2Postnet")
    t2_loss = nemo_tts.Tacotron2Loss.import_from_config(tacotron2_config_file, "Tacotron2Loss")
    makegatetarget = nemo_tts.MakeGate()

    total_weights = text_embedding.num_weights + t2_enc.num_weights + t2_dec.num_weights + t2_postnet.num_weights

    logger.info('================================')
    logger.info(f"Total number of parameters: {total_weights}")
    logger.info('================================')

    return (
        data_preprocessor,
        text_embedding,
        t2_enc,
        t2_dec,
        t2_postnet,
        t2_loss,
        makegatetarget,
    )


def create_train_dag(
        neural_factory,
        neural_modules,
        tacotron2_config_file,
        train_dataset,
        batch_size,
        log_freq,
        checkpoint_save_freq,
        labels,
        cpu_per_dl=1,
):
    (data_preprocessor, text_embedding, t2_enc, t2_dec, t2_postnet, t2_loss, makegatetarget) = neural_modules

    data_layer = nemo_asr.AudioToTextDataLayer.import_from_config(
        tacotron2_config_file,
        "AudioToTextDataLayer_train",
        overwrite_params={
            "manifest_filepath": train_dataset,
            "batch_size": batch_size,
            "num_workers": cpu_per_dl,
            "bos_id": len(labels),
            "eos_id": len(labels) + 1,
            "pad_id": len(labels) + 2,
            "trim_silence": True,
        },
    )

    N = len(data_layer)
    steps_per_epoch = math.ceil(N / (batch_size * neural_factory.world_size))
    logger.info(f'Have {N} examples to train on.')

    # Train DAG
    audio, audio_len, transcript, transcript_len = data_layer()
    spec_target, spec_target_len = data_preprocessor(input_signal=audio, length=audio_len)

    transcript_embedded = text_embedding(char_phone=transcript)
    transcript_encoded = t2_enc(char_phone_embeddings=transcript_embedded, embedding_length=transcript_len)
    mel_decoder, gate, alignments = t2_dec(
        char_phone_encoded=transcript_encoded, encoded_length=transcript_len, mel_target=spec_target,
    )
    mel_postnet = t2_postnet(mel_input=mel_decoder)
    gate_target = makegatetarget(mel_target=spec_target, target_len=spec_target_len)
    loss_t = t2_loss(
        mel_out=mel_decoder,
        mel_out_postnet=mel_postnet,
        gate_out=gate,
        mel_target=spec_target,
        gate_target=gate_target,
        target_len=spec_target_len,
        seq_len=audio_len,
    )

    # Callbacks needed to print info to console and Tensorboard
    train_callback = nemo.core.SimpleLossLoggerCallback(
        tensors=[loss_t, spec_target, mel_postnet, gate, gate_target, alignments],
        print_func=lambda x: logger.info(f"Loss: {x[0].data}"),
        log_to_tb_func=partial(tacotron2_log_to_tb_func, log_images=True, log_images_freq=log_freq),
        tb_writer=neural_factory.tb_writer,
    )

    chpt_callback = nemo.core.CheckpointCallback(folder=neural_factory.checkpoint_dir,
                                                 step_freq=checkpoint_save_freq)

    callbacks = [train_callback, chpt_callback]
    return loss_t, callbacks, steps_per_epoch


def create_eval_dags(
        neural_factory,
        neural_modules,
        tacotron2_config_file,
        eval_datasets,
        eval_batch_size,
        eval_freq,
        labels,
        cpu_per_dl=1,
):
    (data_preprocessor, text_embedding, t2_enc, t2_dec, t2_postnet, t2_loss, makegatetarget) = neural_modules

    callbacks = []
    # assemble eval DAGs
    for eval_dataset in eval_datasets:
        data_layer_eval = nemo_asr.AudioToTextDataLayer.import_from_config(
            tacotron2_config_file,
            "AudioToTextDataLayer_eval",
            overwrite_params={
                "manifest_filepath": eval_dataset,
                "batch_size": eval_batch_size,
                "num_workers": cpu_per_dl,
                "bos_id": len(labels),
                "eos_id": len(labels) + 1,
                "pad_id": len(labels) + 2,
                "trim_silence": True,
            },
        )

        audio, audio_len, transcript, transcript_len = data_layer_eval()
        spec_target, spec_target_len = data_preprocessor(input_signal=audio, length=audio_len)

        transcript_embedded = text_embedding(char_phone=transcript)
        transcript_encoded = t2_enc(char_phone_embeddings=transcript_embedded,
                                    embedding_length=transcript_len)
        mel_decoder, gate, alignments = t2_dec(
            char_phone_encoded=transcript_encoded, encoded_length=transcript_len, mel_target=spec_target,
        )
        mel_postnet = t2_postnet(mel_input=mel_decoder)
        gate_target = makegatetarget(mel_target=spec_target, target_len=spec_target_len)
        loss = t2_loss(
            mel_out=mel_decoder,
            mel_out_postnet=mel_postnet,
            gate_out=gate,
            mel_target=spec_target,
            gate_target=gate_target,
            target_len=spec_target_len,
            seq_len=audio_len,
        )

        # create corresponding eval callback
        tagname = os.path.basename(eval_dataset).split(".")[0]
        eval_tensors = [
            loss,
            spec_target,
            mel_postnet,
            gate,
            gate_target,
            alignments,
        ]
        eval_callback = nemo.core.EvaluatorCallback(
            eval_tensors=eval_tensors,
            user_iter_callback=tacotron2_process_eval_batch,
            user_epochs_done_callback=partial(tacotron2_process_final_eval, tag=tagname),
            tb_writer_func=partial(tacotron2_eval_log_to_tb_func, tag=tagname),
            eval_step=eval_freq,
            tb_writer=neural_factory.tb_writer,
        )

        callbacks.append(eval_callback)
    return callbacks


def create_all_dags(
        neural_factory,
        neural_modules,
        tacotron2_config_file,
        train_dataset,
        batch_size,
        eval_freq,
        labels,
        checkpoint_save_freq=None,
        eval_datasets=None,
        eval_batch_size=None,
):
    # Calculate num_workers for dataloader
    cpu_per_dl = max(int(os.cpu_count() / neural_factory.world_size), 1)

    training_loss, training_callbacks, steps_per_epoch = create_train_dag(
        neural_factory=neural_factory,
        neural_modules=neural_modules,
        tacotron2_config_file=tacotron2_config_file,
        train_dataset=train_dataset,
        batch_size=batch_size,
        log_freq=eval_freq,
        checkpoint_save_freq=checkpoint_save_freq,
        cpu_per_dl=cpu_per_dl,
        labels=labels,
    )

    eval_callbacks = []
    if eval_datasets:
        eval_callbacks = create_eval_dags(
            neural_factory=neural_factory,
            neural_modules=neural_modules,
            tacotron2_config_file=tacotron2_config_file,
            eval_datasets=eval_datasets,
            eval_batch_size=eval_batch_size,
            eval_freq=eval_freq,
            cpu_per_dl=cpu_per_dl,
            labels=labels,
        )
    else:
        logger.info("There were no val datasets passed")

    callbacks = training_callbacks + eval_callbacks
    return training_loss, callbacks, steps_per_epoch


def main():
    args, name = parse_args()

    TRAIN_DATASET = '/opt/stella/data/ramona_final_train_small.json'
    TEST_DATASET = '/opt/stella/data/ramona_final_test_small.json'
    model_config = "/opt/models/tacotron2/de/tacotron2_lowercase.yaml"
    checkpoint_dir = 'checkpoints_ramona_2'

    log_dir = name
    if args.work_dir:
        log_dir = os.path.join(args.work_dir, name)

    # hyperparams
    max_steps = 60000
    num_epochs = 500
    optimizer = "adam"
    beta1 = 0.9
    beta2 = 0.999
    lr = 0.001
    lr_policy = None
    amp_opt_level = "O0"
    create_tb_writer = True
    weight_decay = 1e-6
    batch_size = 48
    eval_batch_size = 64
    grad_norm_clip = None  # 1.0
    min_lr = 1e-5
    eval_freq = 1000
    checkpoint_save_freq = 1000

    # instantiate Neural Factory with supported backend
    neural_factory = nemo.core.NeuralModuleFactory(
        backend=nemo.core.Backend.PyTorch,
        local_rank=args.local_rank,
        optimization_level=amp_opt_level,
        log_dir=log_dir,
        checkpoint_dir=checkpoint_dir,
        create_tb_writer=create_tb_writer,
        files_to_copy=[model_config, __file__],
        cudnn_benchmark=args.cudnn_benchmark,
        tensorboard_dir=None
    )

    if args.local_rank is not None:
        logger.info('Doing ALL GPU')

    yaml = YAML(typ="safe")
    with open(model_config) as file:
        tacotron2_params = yaml.load(file)
        labels = tacotron2_params["labels"]
    # instantiate neural modules
    neural_modules = create_NMs(model_config, labels)

    # build dags
    train_loss, callbacks, steps_per_epoch = create_all_dags(
        neural_factory=neural_factory,
        neural_modules=neural_modules,
        tacotron2_config_file=model_config,
        train_dataset=TRAIN_DATASET,
        batch_size=batch_size,
        eval_freq=eval_freq,
        checkpoint_save_freq=checkpoint_save_freq,
        eval_datasets=[TEST_DATASET],
        eval_batch_size=eval_batch_size,
        labels=labels,
    )

    # train model
    # total_steps = max_steps if max_steps is not None else num_epochs * steps_per_epoch
    neural_factory.train(
        tensors_to_optimize=[train_loss],
        callbacks=callbacks,
        lr_policy=lr_policy,  # CosineAnnealing(total_steps, min_lr=min_lr),
        optimizer=optimizer,
        optimization_params={
            "num_epochs": num_epochs,
            "max_steps": max_steps,
            "lr": lr,
            "weight_decay": weight_decay,
            "betas": (beta1, beta2),
            "grad_norm_clip": grad_norm_clip,
        },
        batches_per_step=args.iter_per_step
    )


if __name__ == '__main__':
    main()
