import os
from typing import List, Dict, Any, Callable
import argparse
import multiprocessing
from pathlib import Path
from ruamel.yaml import YAML
import numpy as np
import soundfile as sf

from utils.data_classes.config_dataclass import T2SConfigDataclass


def gen_samples(config: T2SConfigDataclass, sentences: List[str], output_dir: Path) -> None:
    from inference.inference_interface import Inference
    from inference.inference_factory import InferenceFactory
    from normalization.normalization_pipeline import NormalizerPipeline
    from normalization.postprocessor import Postprocessor

    inference: Inference = InferenceFactory.get_inference(config.inference)

    preprocess_pipeline: NormalizerPipeline = NormalizerPipeline(config=config.normalization)
    postprocessor = Postprocessor(config.postprocessing)

    for i, sentence in enumerate(sentences):
        # infer
        texts: List[str] = preprocess_pipeline.apply(sentence)
        audio_list: List[np.ndarray] = inference.synthesize(
            texts=texts, length_scale=None, noise_scale=None, use_cache=False)
        audio = postprocessor.postprocess(audio_list)

        # save audio to file
        filepath = output_dir / f"sample_{i}.wav"
        sf.write(str(filepath), audio, 22050)


def main() -> None:
    parser = argparse.ArgumentParser(description="Script for creating samples of wav")
    parser.add_argument("--config_dir", type=str, default="evaluation/configs",
                        help="Path to folder with configs of model setups")
    parser.add_argument("--text_samples_path", type=str, default="evaluation/sentences_eloqai.txt",
                        help="Path of the txt file with text samples (sentences)")
    parser.add_argument("--n_samples", type=int, default=20,
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
            config_dict: Dict[str, Any] = yaml.load(f)
            config: T2SConfigDataclass = T2SConfigDataclass.from_dict(config_dict)  # type: ignore

        # using multiprocessing so that GPU memory gets released after each run
        proc = multiprocessing.Process(target=gen_samples, args=(config, sentences, out_dir))
        proc.start()
        proc.join()

    # Write the used sentences to file
    with open(Path(args.output_dir) / args.text_samples_path.split('/')[1], "w") as f:
        for sentence in sentences:
            f.write(sentence + "\n")


if __name__ == "__main__":
    main()