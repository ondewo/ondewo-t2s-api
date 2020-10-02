import os
import uuid
from dataclasses import dataclass
from shutil import copy
from typing import List, Union, Type, Tuple
from typing import TYPE_CHECKING

import yaml

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
        models_path: str = "./models",
    ) -> 'DirTree':
        """
        construct dataclass from /models/ directory
        any time this function is called, the directory is rescanned
        will also read the config file data of all model setups

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
