from scipy.io.wavfile import write
import librosa
import numpy as np
from typing import List, Dict, Any
import json

dataset = ""
sr = 22050
max_wav_value = 32768.0
trim_fft_size = 1024
trim_hop_size = 256
trim_top_db = 23
silence_audio_size = 2


def main():

    sample_list: List[Dict[str, Any]] = []
    with open(dataset, "r") as d_file:
        for line in d_file:
            sample_list.append(json.loads(line))

    for sample in sample_list:
        wav_file = sample["audio_filepath"]
        data, sampling_rate = librosa.core.load(wav_file, sr)
        data = data / np.abs(data).max() * 0.999
        data = librosa.effects.trim(data, top_db=trim_top_db, frame_length=trim_fft_size, hop_length=trim_hop_size)[0]
        data_ = data * max_wav_value
        data_ = np.append(data_, [0.] * silence_audio_size)
        data_ = data_.astype(dtype=np.int16)
        write(wav_file, sr, data_)


if __name__ == "__main__":
    main()
