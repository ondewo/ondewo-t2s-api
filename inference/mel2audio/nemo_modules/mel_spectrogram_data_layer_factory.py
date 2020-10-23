from typing import List

import numpy as np

from inference.mel2audio.nemo_modules.mel_spectrogram_data_layer import MelSpectrogramDataLayer


# We need this factory method due to a cythonization bug in NeMo
def get_mel_spectrogram_data_layer(mel_spectrograms: List[np.ndarray], batch_size: int) -> MelSpectrogramDataLayer:
    return MelSpectrogramDataLayer(
        mel_spectrograms,
        batch_size=batch_size,
        num_workers=1,
        shuffle=False
    )
