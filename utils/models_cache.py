from typing import Any, Dict, List, Optional

from utils.data_classes.config_dataclass import GlowTTSDataclass, HiFiGanDataclass


class ModelCache:
    cached_models: Dict[str, Any] = {}

    @classmethod
    def clean_cache(cls) -> None:
        cls.cached_models = {}

    @classmethod
    def create_text_processor_key(
            cls, path: Optional[str], lang: str, blank: bool, list_param: Optional[List[str]]) -> str:
        list_param = list_param or []
        assert isinstance(list_param, list)
        path = path or ''
        assert isinstance(path, str)
        return path + "_blank" * blank + "_" + lang + \
            ("_" + str(abs(hash(str(sorted(list_param)))))) * bool(list_param)

    @classmethod
    def create_glow_tts_key(cls, config: GlowTTSDataclass) -> str:
        return f'{config.path}-{"cuda" * config.use_gpu + "cpu" * (not config.use_gpu)}'

    @classmethod
    def create_hifi_key(cls, config: HiFiGanDataclass) -> str:
        return f'{config.model_path}-{"cuda" * config.use_gpu + "cpu" * (not config.use_gpu)}'
