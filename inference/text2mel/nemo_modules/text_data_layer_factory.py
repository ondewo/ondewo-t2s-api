from typing import List

from inference.text2mel.nemo_modules.text_data_layer import TextDataLayer


# We need this factory method due to a cythonization bug in NeMo
def get_text_data_layer(texts: List[str],
                        labels: List[str],
                        batch_size: int,
                        bos_id: int,
                        eos_id: int,
                        pad_id: int) -> TextDataLayer:
    return TextDataLayer(
        texts=texts,
        labels=labels,
        batch_size=batch_size,
        num_workers=1,
        bos_id=bos_id,
        eos_id=eos_id,
        pad_id=pad_id,
        shuffle=False,
    )
