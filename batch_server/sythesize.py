import re
from typing import List
import numpy as np

from batch_server import normalizer, inference, postprocesser
from utils.logger import logger


def synthesize(text: str) -> np.array:
    if re.search(r'[A-Za-z0-9]+', text):
        logger.info(f'Text to transcribe: "{text}"')
        texts: List[str] = normalizer.normalize_and_split(text)
        logger.info(f'After normalization texts are: {texts}')

        audio_list: List[np.ndarray] = inference.synthesize(texts=texts)
        audio = postprocesser.postprocess(audio_list)
        return audio
    else:
        logger.info(f'Text to synthesize should contain at least one letter or number. Got "{text}". '
                    f'Silence will be synthesized.')
        return np.zeros((10000,))
