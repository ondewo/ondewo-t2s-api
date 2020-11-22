import os
from typing import List, Dict, Any, Callable
import argparse
import multiprocessing
from pathlib import Path
from ruamel.yaml import YAML
import numpy as np

from scipy.io.wavfile import write as audio_write


def gen_samples(config: Dict[str, Any], sentences: List[str], output_dir: Path) -> None:
    from inference.inference_interface import Inference
    from inference.inference_factory import InferenceFactory
    from normalization.pipeline_constructor import NormalizerPipeline
    from normalization.postprocessor import Postprocessor
    import tensorflow as tf
    gpus = tf.config.experimental.list_physical_devices('GPU')
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)

    inference: Inference = InferenceFactory.get_inference(config['inference'])

    preprocess_pipeline: NormalizerPipeline = NormalizerPipeline(config=config['normalization'])
    postprocessor = Postprocessor()

    for i, sentence in enumerate(sentences):
        # infer
        texts: List[str] = preprocess_pipeline.apply([sentence])
        audio_list: List[np.ndarray] = inference.synthesize(texts=texts)
        audio = postprocessor.postprocess(audio_list)

        # convert and save wav
        # conversion to 16-bit PCM
        audio *= 32768
        audio = audio.astype("int16")

        # save audio to file
        filepath = output_dir / f"sample_{i}.wav"
        audio_write(str(filepath), 22050, audio)


def main() -> None:
    parser = argparse.ArgumentParser(description="Script for creating samples of wav")
    parser.add_argument("--config_dir", type=str, default="evaluation/configs",
                        help="Path to folder with configs of model setups")
    parser.add_argument("--text_samples_path", type=str, default="evaluation/sentences.txt",
                        help="Path of the txt file with text samples (sentences)")
    parser.add_argument("--n_samples", type=int, default=10,
                        help="How many samples to generate per model setup, set to < 1 to use all")
    parser.add_argument("--output_dir", type=str, default="samples",
                        help="Path to folder where to output the samples")
    args = parser.parse_args()

    # read sentences from a txt file
    sentences: List[str] = []
    with open(args.text_samples_path) as f:
        sentences = [line.rstrip() for line in f]
        sentences = sentences[:args.n_samples] if args.n_samples > 0 else sentences

    yaml = YAML(typ="safe")
    # Go through all configs in config_folder and generate their samples
    for config_name in os.listdir(args.config_dir):
        config_path = Path(args.config_dir) / config_name
        out_dir = Path(args.output_dir) / config_path.stem
        os.makedirs(out_dir, exist_ok=True)

        # load config
        with open(config_path) as f:
            config: Dict[str, Any] = yaml.load(f)
            #config["inference"]["composite_inference"]["mel2audio"]["mb_melgan_tf"]["model_path"] = "/home/utanko/train.mb_melgan.germans/checkpoints/generator-300000.h5"

        # using multiprocessing so that GPU memory gets released after each run
        proc = multiprocessing.Process(target=gen_samples, args=(config, sentences, out_dir))
        proc.start()
        proc.join()

        # this part is used for evaluation of different mb_melgan generator (at different steps)
        # for steps in [500_000, 760_000, 1_000_000, 1_220_000, 1_360_000, 1_500_000, 1_760_000, 2_000_000]:
        #     config["inference"]["composite_inference"]["mel2audio"]["mb_melgan_tf"]["model_path"] = f"/home/utanko/train.mb_melgan.libritts/checkpoints/generator-{steps}.h5"
        #     out_dir_steps = out_dir / str(steps)
        #     os.makedirs(out_dir_steps, exist_ok=True)
        #     # using multiprocessing so that GPU memory gets released after each run
        #     proc = multiprocessing.Process(target=gen_samples, args=(config, sentences, out_dir_steps))
        #     proc.start()
        #     proc.join()

    # Write the used sentences to file
    with open(Path(args.output_dir) / "sentences.txt", "w") as f:
        for sentence in sentences:
            f.write(sentence + "\n")


if __name__ == "__main__":
    main()
