import os
import uuid
from queue import Queue, Empty
from threading import Thread
from typing import Dict, Optional, List, Tuple

import numpy as np
from cachetools import LFUCache
from scipy.io.wavfile import read as read_wav
from scipy.io.wavfile import write

from inference.inference_interface import Inference
from ondewologging.logger import logger_console as logger

from utils.data_classes.config_dataclass import CachingDataclass


class CachedInference(Inference):

    def __init__(self, inference: Inference, config: CachingDataclass):
        self.save_cache: bool = config.save_cache
        self.memory_cache_max_size: int = config.memory_cache_max_size
        self.cache_save_dir: str = config.cache_save_dir
        self.sr: int = config.sampling_rate

        self.inference: Inference = inference

        # Cache loaded in memory, limited in size
        # Key: text, value: audio waveform
        self.memory_cache: LFUCache = LFUCache(maxsize=self.memory_cache_max_size)
        # Second, unlimited cache of all audio which has been synthesized
        # Key: text, value: audio filename
        self.file_cache: Dict[str, str] = {}

        if config.load_cache:
            logger.info('Started loading the cache from filesystem.')
            self.load_cache()
            logger.info(f'Loading of the memory cache is done. '
                        f'Memory cache has {len(self.memory_cache)} elements. '
                        f'The loaded cached texts are: {list(self.memory_cache.keys())}')
            logger.info(f'Loading of the file cache is done. '
                        f'File cache has {len(self.file_cache)} elements.')

        if self.save_cache:
            if not os.path.isdir(self.cache_save_dir):
                os.mkdir(self.cache_save_dir)

            self.saving_queue: Queue[Tuple[str, np.ndarray]] = Queue()
            self.saved_file_queue: Queue[Tuple[str, str]] = Queue()
            self.caching_thread: Thread = Thread(target=self.saving_cache_loop,
                                                 args=(self.saving_queue,
                                                       self.saved_file_queue,
                                                       self.cache_save_dir,
                                                       self.sr))
            self.caching_thread.start()

    def load_cache(self) -> None:
        if not os.path.isdir(self.cache_save_dir):
            return
        for file in os.listdir(self.cache_save_dir):
            if file.endswith('.txt'):
                txt_path = os.path.join(self.cache_save_dir, file)
                wav_path = txt_path[:-3] + 'wav'
                if not os.path.isfile(wav_path):
                    continue

                with open(txt_path, mode='r') as fi:
                    text = fi.read()
                audio = self.read_audio(wav_path)

                # Don't need to add more things in the memory cache if it's full
                if len(self.memory_cache) <= self.memory_cache_max_size:
                    self.memory_cache[text] = audio
                self.file_cache[text] = wav_path

    def saving_cache_loop(self,
                          saving_queue: Queue,
                          saved_file_queue: Queue,
                          cache_save_dir: str,
                          sr: int) -> None:
        try:
            while True:
                text, audio = saving_queue.get()
                file_name_base: str = str(uuid.uuid5(uuid.NAMESPACE_DNS, text))
                wav_file_path: str = os.path.join(cache_save_dir, file_name_base + '.wav')
                text_file_path: str = os.path.join(cache_save_dir, file_name_base + '.txt')

                # Save text file
                with open(text_file_path, "w", encoding="utf-8") as fi:
                    fi.write(text)

                # Save audio file
                audio *= 32768
                audio = audio.astype("int16")
                write(wav_file_path, sr, audio)

                logger.info(f'Saved text "{text}" and its audio to disc.')
                saved_file_queue.put((text, wav_file_path))
        except Exception:
            logger.exception("Saving cache loop exception.")

    def cache_audio(self, text: str, audio: np.ndarray) -> None:
        self.memory_cache[text] = audio
        logger.info(f'Text "{text}" is added to the memory cache. '
                    f' Memory cache has {len(self.memory_cache)} elements now.')
        if self.save_cache:
            self.saving_queue.put((text, np.copy(audio)))

    def synthesize(self, texts: List[str], length_scale: Optional[float], noise_scale: Optional[float]) -> List[np.ndarray]:

        logger.warning(f'You are using cached inference with length scale and noise scale '
                       f'{length_scale, noise_scale}. Note that changing these values '
                       f'will not be available for cached audio. You can only set it up once before caching.')

        # Firstly, update the file cache
        try:
            while not self.saved_file_queue.empty():
                text, audiofile = self.saved_file_queue.get(block=False)
                self.file_cache[text] = audiofile
                logger.info(f'Updated file cache. File cache has {len(self.file_cache)} elements now.')
        except Empty:
            logger.exception("Saving file queue is empty!")

        texts_not_in_cache: List[str] = []
        audio_result: Dict[str, np.ndarray] = {}
        for text in texts:
            if text in self.memory_cache:
                audio_result[text] = self.memory_cache[text]
                logger.info(f'Text "{text}" taken from the memory cache.')
            elif text in self.file_cache:
                audio_result[text] = self.read_audio(self.file_cache[text])
                self.memory_cache[text] = audio_result[text]
                logger.info(f'Text "{text}" taken from the file cache.')
            else:
                texts_not_in_cache.append(text)

        if len(texts_not_in_cache) > 0:
            logger.info(f'Start synthesizing audio for texts {texts_not_in_cache}')
            audio_list: List[np.ndarray] = self.inference.synthesize(
                texts=texts_not_in_cache,
                length_scale=length_scale,
                noise_scale=noise_scale
            )
            logger.info('Synthesizing is finished.')
            for text, audio in zip(texts_not_in_cache, audio_list):
                audio_result[text] = audio
                self.cache_audio(text=text, audio=audio)

        return [audio_result[text] for text in texts]

    def read_audio(self, wav_path: str) -> np.ndarray:
        sr, audio = read_wav(wav_path)
        if sr != self.sr:
            raise ValueError("")
        return audio.astype('float32') / 32768
