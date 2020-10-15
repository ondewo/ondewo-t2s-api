import os
import uuid
from dataclasses import dataclass
from shutil import copy
from typing import List, Union, Type, Tuple
from typing import TYPE_CHECKING

import yaml

from grpc_config_server.config import MODELS_PATH
from grpc_config_server.ondewo.audio import text_to_speech_pb2

if TYPE_CHECKING:
    from grpc_config_server.t2s_manager.manager import TextToSpeechManager


@dataclass
class ModelConfig:
    name: str
    full_path: str
    model_id: str
    config_yaml_path: str
    config_data: dict
    language_code: str

    @staticmethod
    def read_config_data(config_path: str) -> dict:
        with open(config_path) as file:
            config_data = yaml.safe_load(file)
        if not type(config_data) == dict:
            raise IOError(
                f"Failed to load config data from file {config_path}! File might be corrupted or empty")
        return config_data  # type: ignore

    def set(self, active_config_yaml: str) -> Tuple[bool, str]:
        copy(src=self.config_yaml_path, dst=active_config_yaml)
        return True, ""

    def get_proto_config(self) -> text_to_speech_pb2.Text2SpeechConfig:
        return self.get_proto_from_dict(config_data=self.config_data)

    @staticmethod
    def get_proto_from_dict(config_data: dict) -> text_to_speech_pb2.Text2SpeechConfig:
        return text_to_speech_pb2.Text2SpeechConfig(
            inference=text_to_speech_pb2.Inference(
                type=config_data["inference"]["type"],
                composite_inference=text_to_speech_pb2.CompositeInference(
                    text_2_mel=text_to_speech_pb2.Text2Mel(
                        type=config_data["inference"]["composite_inference"]["text2mel"]["type"],
                        tacotron_2=text_to_speech_pb2.Tacotron2(
                            batch_size=config_data["inference"]["composite_inference"]["text2mel"]["tacotron2"][
                                "batch_size"],
                            path=config_data["inference"]["composite_inference"]["text2mel"]["tacotron2"]["path"],
                            param_config_path=config_data["inference"]["composite_inference"]["text2mel"]["tacotron2"][
                                "param_config_path"],
                            step=config_data["inference"]["composite_inference"]["text2mel"]["tacotron2"]["step"],
                        ),
                        glow_tts=text_to_speech_pb2.GlowTTS(
                            batch_size=config_data["inference"]["composite_inference"]["text2mel"]["glow_tts"][
                                "batch_size"],
                            use_gpu=config_data["inference"]["composite_inference"]["text2mel"]["glow_tts"][
                                "use_gpu"],
                            length_scale=config_data["inference"]["composite_inference"]["text2mel"]["glow_tts"][
                                "length_scale"],
                            noise_scale=config_data["inference"]["composite_inference"]["text2mel"]["glow_tts"][
                                "noise_scale"],
                            batch_inference=config_data["inference"]["composite_inference"]["text2mel"]["glow_tts"][
                                "batch_inference"],
                            path=config_data["inference"]["composite_inference"]["text2mel"]["glow_tts"]["path"],
                            param_config_path=config_data["inference"]["composite_inference"]["text2mel"]["glow_tts"][
                                "param_config_path"],
                        ),
                    ),
                    mel_2_audio=text_to_speech_pb2.Mel2Audio(
                        type=config_data["inference"]["composite_inference"]["mel2audio"]["type"],
                        waveglow=text_to_speech_pb2.Waveglow(
                            batch_size=config_data["inference"]["composite_inference"]["mel2audio"]["waveglow"][
                                "batch_size"],
                            path=config_data["inference"]["composite_inference"]["mel2audio"]["waveglow"]["path"],
                            param_config_path=config_data["inference"]["composite_inference"]["mel2audio"]["waveglow"][
                                "param_config_path"],
                            sigma=config_data["inference"]["composite_inference"]["mel2audio"]["waveglow"][
                                "sigma"],
                            denoiser=text_to_speech_pb2.Denoiser(
                                active=config_data["inference"]["composite_inference"]["mel2audio"]["waveglow"][
                                    "denoiser"]["active"],
                                strength=config_data["inference"]["composite_inference"]["mel2audio"]["waveglow"][
                                    "denoiser"]["strength"],
                            ),
                        ),
                        waveglow_triton=text_to_speech_pb2.WaveglowTriton(
                            param_config_path=config_data["inference"]["composite_inference"]["mel2audio"]["waveglow_triton"][
                                "param_config_path"],
                            sigma=config_data["inference"]["composite_inference"]["mel2audio"]["waveglow_triton"][
                                "sigma"],
                            max_spect_size=config_data["inference"]["composite_inference"]["mel2audio"]["waveglow_triton"][
                                "max_spect_size"],
                            triton_model_name=config_data["inference"]["composite_inference"]["mel2audio"]["waveglow_triton"][
                                "triton_model_name"],
                            triton_url=config_data["inference"]["composite_inference"]["mel2audio"]["waveglow_triton"][
                                "triton_url"],
                        )
                    )
                ),
                caching=text_to_speech_pb2.Caching(
                    active=config_data["inference"]["caching"]["active"],
                    memory_cache_max_size=config_data["inference"]["caching"]["memory_cache_max_size"],
                    sampling_rate=config_data["inference"]["caching"]["sampling_rate"],
                    load_cache=config_data["inference"]["caching"]["load_cache"],
                    save_cache=config_data["inference"]["caching"]["save_cache"],
                    cache_save_dir=config_data["inference"]["caching"]["cache_save_dir"],
                )
            )
        )

    @staticmethod
    def get_dict_from_proto(config_data: text_to_speech_pb2.Text2SpeechConfig) -> dict:
        return {'inference':
                {'type': config_data.inference.type,
                 'composite_inference': {
                     'text2mel': {'type': config_data.inference.composite_inference.text_2_mel.type,
                                  'tacotron2': {
                                      'batch_size': config_data.inference.composite_inference.text_2_mel.tacotron_2.batch_size,
                                      'path': config_data.inference.composite_inference.text_2_mel.tacotron_2.path,
                                      'param_config_path': config_data.inference.composite_inference.text_2_mel.tacotron_2.param_config_path,
                                      'step': config_data.inference.composite_inference.text_2_mel.tacotron_2.step},
                                  'glow_tts': {
                                      'batch_size': config_data.inference.composite_inference.text_2_mel.glow_tts.batch_size,
                                      'use_gpu': config_data.inference.composite_inference.text_2_mel.glow_tts.use_gpu,
                                      'length_scale': config_data.inference.composite_inference.text_2_mel.glow_tts.length_scale,
                                      'noise_scale': config_data.inference.composite_inference.text_2_mel.glow_tts.noise_scale,
                                      'batch_inference': config_data.inference.composite_inference.text_2_mel.glow_tts.batch_inference,
                                      'path': config_data.inference.composite_inference.text_2_mel.glow_tts.path,
                                      'param_config_path': config_data.inference.composite_inference.text_2_mel.glow_tts.param_config_path}},
                     'mel2audio': {'type': config_data.inference.composite_inference.mel_2_audio.type,
                                   'waveglow': {
                                       'batch_size': config_data.inference.composite_inference.mel_2_audio.waveglow.batch_size,
                                       'path': config_data.inference.composite_inference.mel_2_audio.waveglow.path,
                                       'param_config_path': config_data.inference.composite_inference.mel_2_audio.waveglow.param_config_path,
                                       'sigma': config_data.inference.composite_inference.mel_2_audio.waveglow.sigma,
                                       'denoiser': {
                                           'active': config_data.inference.composite_inference.mel_2_audio.waveglow.denoiser.active,
                                           'strength': config_data.inference.composite_inference.mel_2_audio.waveglow.denoiser.strength}},
                                   'waveglow_triton': {
                                       'param_config_path': config_data.inference.composite_inference.mel_2_audio.waveglow_triton.param_config_path,
                                       'sigma': config_data.inference.composite_inference.mel_2_audio.waveglow_triton.sigma,
                                       'max_spect_size': config_data.inference.composite_inference.mel_2_audio.waveglow_triton.max_spect_size,
                                       'triton_model_name': config_data.inference.composite_inference.mel_2_audio.waveglow_triton.triton_model_name,
                                       'triton_url': config_data.inference.composite_inference.mel_2_audio.waveglow_triton.triton_url}}},
                 'caching': {'active': config_data.inference.caching.active,
                             'memory_cache_max_size': config_data.inference.caching.memory_cache_max_size,
                             'sampling_rate': config_data.inference.caching.sampling_rate,
                             'load_cache': config_data.inference.caching.load_cache,
                             'save_cache': config_data.inference.caching.save_cache,
                             'cache_save_dir': config_data.inference.caching.cache_save_dir}}}


@dataclass
class DirSpeaker:
    name: str
    model_configs: List[ModelConfig]

    def get_model_config(self, name: str) -> Union[ModelConfig, None]:
        """get the model config object with the given name"""
        for model_config in self.model_configs:
            if name == model_config.name:
                return model_config
        return None


@dataclass
class DirDomain:
    name: str
    speakers: List[DirSpeaker]

    def get_speaker(self, name: str) -> Union[DirSpeaker, None]:
        """get the model config object with the given name"""
        for speaker in self.speakers:
            if name == speaker.name:
                return speaker
        return None


@dataclass
class DirLanguage:
    name: str
    domains: List[DirDomain]

    def get_domain(self, name: str) -> Union[DirDomain, None]:
        """get the dir domain object with the given name"""
        for domain in self.domains:
            if name == domain.name:
                return domain
        return None


@dataclass
class DirCompany:
    name: str
    languages: List[DirLanguage]

    def get_language(self, name: str) -> Union[DirLanguage, None]:
        """get the dir language object with the given name"""
        for language in self.languages:
            if name == language.name:
                return language
        return None


@dataclass
class DirTree:
    directory: str
    companies: List[DirCompany]
    manager: 'TextToSpeechManager'

    def get_all_languages(self) -> List[DirLanguage]:
        """get all available languages"""
        languages = []
        for company in self.companies:
            languages.extend([language for language in company.languages])
        return languages

    def get_company(self, name: str) -> DirCompany:
        """get the dir company object with the given name"""
        for company in self.companies:
            if name == company.name:
                return company
        raise ValueError(
            f"no company with this name available: {name}" +
            f", available: {[company.name for company in self.companies]}")

    def get_associated_model_setup(self, config_data: dict) -> ModelConfig:
        """get the ModelConfig object associated with the given config_data"""
        setups = self.extract_model_config_list()
        for setup in setups:
            if config_data == setup.config_data:
                return setup
        raise FileNotFoundError("Could not find path of active config.yaml. No files in " +
                                "./model/<company>/<language>/<domain>/<speaker>/<setup>/config/config.yaml" +
                                " match the config")

    def get_model_by_id(self, model_id: Type[str]) -> ModelConfig:
        """get the ModelConfig associated with this model_id"""
        setups = self.extract_model_config_list()
        for setup in setups:
            if setup.model_id == model_id:
                return setup
        raise ModuleNotFoundError(f"could not find model configuration with this id: {model_id}!")

    @staticmethod
    def load_from_path(
            manager: 'TextToSpeechManager',
            config_path_relative: str,
            models_path: str = MODELS_PATH,
    ) -> 'DirTree':
        """
        construct dataclass from /models/ directory
        any time this function is called, the directory is rescanned
        will also read the config file data of all model setups
        will assign new uuids to configs every time it is called

        Args:
            manager: superior of DirTree, instance of speech to text manager
            config_path_relative: path of config.yaml in ./models relative to /<model_setup>/
            models_path: (optional, default "./models")
                         path of models with directory structure
                         /models/<company>/<language>/<domain>/<speaker>/<model_setup>/
                         preferably relative
        """

        # get companies from /models/
        company_list = []
        companies = os.listdir(models_path)
        for company in companies:
            cpath = models_path + f"/{company}"

            # get languages from /models/<company>/
            language_list = []
            languages = os.listdir(cpath)
            for language in languages:
                lpath = cpath + f"/{language}"

                # get domains from /models/<company>/<language>/
                domain_list = []
                domains = os.listdir(lpath)
                for domain in domains:
                    dpath = lpath + f"/{domain}"

                    # get speakers from /models/<company>/<language>/<domain>/
                    speaker_list = []
                    speakers = os.listdir(dpath)
                    for speaker in speakers:
                        spath = dpath + f"/{speaker}"

                        # get model setups from /models/<company>/<language>/<domain>/<speaker>/
                        model_list = []
                        model_setups = os.listdir(spath)
                        for model_setup in model_setups:
                            mpath = spath + f"/{model_setup}"

                            # NOTE: directory: /models/<company>/<language>/<domain>/<speaker>/<model_setup>/

                            # load config of this setup
                            config_yaml_path = mpath + config_path_relative
                            config_data = ModelConfig.read_config_data(config_path=config_yaml_path)

                            # save model setups
                            model_list.append(ModelConfig(
                                name=model_setup,
                                full_path=mpath,
                                config_yaml_path=config_yaml_path,
                                model_id=str(uuid.uuid4()),
                                language_code=language,
                                config_data=config_data,
                            ))

                        # save speakers
                        speaker_list.append(DirSpeaker(
                            name=speaker,
                            model_configs=model_list,
                        ))

                    # save domains
                    domain_list.append(DirDomain(
                        name=domain,
                        speakers=speaker_list,
                    ))

                # save languages
                language_list.append(DirLanguage(
                    name=language,
                    domains=domain_list,
                ))

            # save companies
            company_list.append(DirCompany(
                name=company,
                languages=language_list,
            ))

        # construct dir object
        return DirTree(
            directory=models_path,
            companies=company_list,
            manager=manager,
        )

    def extract_model_config_list(
            self,
            company_name: Union[str, None] = None,
            language_code: Union[str, None] = None,
            speaker_name: Union[str, None] = None,
            domain_name: Union[str, None] = None,
            model_setup_name: Union[str, None] = None,
    ) -> List[ModelConfig]:
        """
        extracts a list with all model setup configs
        if arguments are provided, checks whether the argument is in the setup's path

        Args: (all optional)
            company_name: (optional) company name to filter for
            language_code: (optional) language to filter for
            domain_name: (optional) domain to filter for
            model_setup_name: (optional) model setup name/code to filter for

        Returns:
            list of model config objects
        """
        model_config_list: List[ModelConfig] = []

        # check company name
        if company_name:
            companies = [self.get_company(name=company_name)]
        else:
            companies = self.companies  # type: ignore
        for a_company in companies:
            if not a_company:
                continue

            # check language code
            if language_code:
                languages = [a_company.get_language(name=language_code)]
            else:
                languages = a_company.languages  # type: ignore
            for a_language in languages:
                if not a_language:
                    continue

                # check domain name
                if domain_name:
                    domains = [a_language.get_domain(name=domain_name)]
                else:
                    domains = a_language.domains  # type: ignore
                for a_domain in domains:
                    if not a_domain:
                        continue

                    # check speaker name
                    if speaker_name:
                        speakers = [a_domain.get_speaker(name=speaker_name)]
                    else:
                        speakers = a_domain.speakers  # type: ignore
                    for a_speaker in speakers:
                        if not a_speaker:
                            continue

                        # check model setup name
                        if model_setup_name:
                            setups = [a_speaker.get_model_config(name=model_setup_name)]
                        else:
                            setups = a_speaker.model_configs  # type: ignore

                        # append all that match
                        for a_model in setups:
                            if not a_model:
                                continue
                            else:
                                model_config_list.append(a_model)

        # trial for streamlined code
        # will check full path instead of every part of the path, which can lead to wrong results
        # if e.g. language-code is in the company name, domain name in company name, etc. pp.
        # for a_company in self.companies:
        #     for a_language in a_company.languages:
        #         for a_domain in a_language.domains:
        #               for a_speaker in a_domain.speakers:
        #                   for a_config in a_domain.model_configs:
        #                       if all(condition in a_config.full_path for condition in [
        #                           some_condition for some_condition in [
        #                               company_name, language_code, domain_name, model_setup_name
        #                           ] if some_condition is not None
        #                       ]):
        #                           model_config_list.append(a_config)

        return model_config_list
