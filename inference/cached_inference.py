import os
import uuid
from multiprocessing import Process, Queue
from typing import Dict, Any, List, Optional

import numpy as np
from scipy.io.wavfile import read as read_wav
from scipy.io.wavfile import write

from inference.inference import Inference
from utils.logger import logger


class CachedInference(Inference):
    cache: Optional[Dict[str, np.ndarray]] = {}
    saving_queue: Queue = Queue()
    CACHE_DIR = "cache"
    sr = 22050

    def __init__(self, inference: Inference, config: Dict[str, Any]):
        self.inference = inference
        self.save_cache: bool = config['save_cache']
        if not os.path.isdir(self.CACHE_DIR):
            os.mkdir(self.CACHE_DIR)
        if config['load_cache']:
            logger.info('Start loading the cache')
            self.load_cache()
            logger.info(f'Load the cahce is done. The cached texts loaded are {self.cache.keys()}')
            logger.info(f"Cache has {len(self.cache)} elements")
        if self.save_cache:
            self.pickle_thread: Process = Process(target=self.saving_cache_loop, args=(self.saving_queue,))
            self.pickle_thread.start()

    def load_cache(self) -> None:
        """

        Returns:

        """
        if not os.path.isdir(self.CACHE_DIR):
            return
        for file in os.listdir(self.CACHE_DIR):
            if file.endswith('.txt'):
                txt_path = os.path.join(self.CACHE_DIR, file)
                wav_path = txt_path[:-3] + 'wav'
                if not os.path.isfile(wav_path):
                    continue
                with open(txt_path, mode='r') as fi:
                    text = fi.read()
                    audio = self.read_audio(wav_path)
                    self.cache[text] = audio

    def saving_cache_loop(self, saving_cache_queue: Queue) -> None:
        """
        
        Args:
            saving_cache_queue: 

        Returns:

        """
        while True:
            text, response = saving_cache_queue.get()
            file_name_base: str = str(uuid.uuid5(uuid.NAMESPACE_DNS, text))
            wav_file_path: str = os.path.join(self.CACHE_DIR, file_name_base + '.wav')
            text_file_path: str = os.path.join(self.CACHE_DIR, file_name_base + '.txt')
            with open(text_file_path, "w", encoding="utf-8") as fi:
                fi.write(text)
            response *= 32768
            response = response.astype("int16")
            write(wav_file_path, self.sr, response)
            logger.info(f'Audio for text {text} is saved on the disc.')

    def cache_response(self, response: np.ndarray, text: str) -> None:
        """

        Args:
            response:
            text:

        Returns:

        """
        self.cache[text] = response
        logger.info(f"{text} added to cache, now cache has {len(self.cache)} elements")
        if self.save_cache:
            self.saving_queue.put((text, response))

    def synthesize(self, texts: List[str]) -> List[np.ndarray]:
        """

        Args:
            texts:

        Returns:

        """
        texts_not_in_cache: List[str] = []
        result: Dict[str] = {}
        for text in texts:
            if text in self.cache:
                result[text] = self.cache[text]
            else:
                texts_not_in_cache.append(text)
        logger.info(f'{result.keys()} are taken from the cache')
        logger.info(f'Start synthesizing audio for {texts_not_in_cache}')
        audio_list: List[np.ndarray] = self.inference.synthesize(texts=texts_not_in_cache)
        logger.info('Synthesizing is finished')
        for text, audio in zip(texts_not_in_cache, audio_list):
            result[text] = audio
            self.cache_response(response=audio, text=text)
        logger.info(f'Texts {texts_not_in_cache} are saved in the cache')
        return [result[text] for text in texts]

    def read_audio(self, wav_path: str) -> np.ndarray:
        sr, audio = read_wav(wav_path)
        if sr != self.sr:
            raise ValueError("")
        return audio.astype('float32') / 32768
