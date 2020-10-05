from typing import Dict, Any

from inference.text2mel.tacotron2 import Tacotron2
from inference.text2mel.text2mel import Text2Mel


class Text2MelFactory:

    @classmethod
    def get_text2mel(cls, config: Dict[str, Any]) -> Text2Mel:
        if config.get('type') == 'tacotron2':
            text2mel: Text2Mel = Tacotron2(config=config['tacotron2'])
        else:
            raise ValueError(
                f'Supported Tex2Mel models are: ["tacotron2"]. Got {config.get("type")}.')
        return text2mel
