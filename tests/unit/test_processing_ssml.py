import os
from typing import List, Dict, Any
import pytest
from ruamel import yaml
from normalization.normalization_pipeline import NormalizerPipeline
from utils.data_classes.config_dataclass import NormalizationDataclass


def get_normalizer_pipeline(config_path: str) -> NormalizerPipeline:
    with open(os.path.join('tests', 'resources', config_path), 'r') as f:
        config_dict: Dict[str, Any] = yaml.load(f, Loader=yaml.Loader)
        config = NormalizationDataclass.from_dict(config_dict)  # type: ignore
    return NormalizerPipeline(config)


class TestTextSSMLPreprocessor:
    @staticmethod
    @pytest.mark.parametrize('config_path, text, expected', [
        ('normalizer_pipeline_de.yaml', '<say-as interpret-as="spell">ABCDEFGHIJKLMNOPQRSTUVWXYZ</say-as>',
         ['{a} .', ' {b} .', ' {c} .', ' {d} .', ' {e} .', ' {f} .', ' {g} .', ' {h} .', ' {i} .', ' {j} .', ' {k} .',
          ' {l} .', ' {m} .', ' {n} .', ' {o} .', ' {p} .', ' {q} .', ' {r} .', ' {s} .', ' {t} .', ' {u} .', ' {v} .',
          ' {w} .', ' {x} .', ' {y} .', ' {z} .']),
        ('normalizer_pipeline_de.yaml', '<say-as interpret-as="spell">ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789</say-as>',
         ['{a} .', ' {b} .', ' {c} .', ' {d} .', ' {e} .', ' {f} .', ' {g} .', ' {h} .', ' {i} .', ' {j} .', ' {k} .',
          ' {l} .', ' {m} .', ' {n} .', ' {o} .', ' {p} .', ' {q} .', ' {r} .', ' {s} .', ' {t} .', ' {u} .', ' {v} .',
          ' {w} .', ' {x} .', ' {y} .', ' {z} .', ' eiins.', ' zweiii.', ' dreiii.', ' viieer.', ' fünnff.', ' sex.',
          ' siiebeenn.', ' aachttth.', ' neunhh.']),
    ])
    def test_ssml_processing__spell(config_path: str, text: str, expected: List[str]) -> None:
        normalizer_pipeline = get_normalizer_pipeline(config_path=config_path)
        normalized_text = normalizer_pipeline.apply(text)
        assert normalized_text == expected

    @staticmethod
    @pytest.mark.parametrize('config_path, text, expected', [
        ('normalizer_pipeline_de.yaml', '<say-as interpret-as="spell-with-names">ABCDEFGHIJKLMNOPQRSTUVWXYZ</say-as>',
         ['{a} , wie anna.', ' {b} , wie berta.', ' {c} , wie cäsar.', ' {d} , wie daniel.', ' {e} , wie emil.',
          ' {f} , wie friedrich.', ' {g} , wie gustav.', ' {h} , wie heinrich.', ' {i} , wie ida.', ' {j} , wie jakob.',
          ' {k} , wie kaiser.', ' {l} , wie leopold.', ' {m} , wie marie.', ' {n} , wie niklaus.', ' {o} , wie otto.',
          ' {p} , wie peter.', ' {q} , wie quasi.', ' {r} , wie rosa.', ' {s} , wie sophie.', ' {t} , wie theodor.',
          ' {u} , wie ulrich.', ' {v} , wie viktor.', ' {w} , wie wilhelm.', ' {x} , wie xavier.',
          ' {y} , wie ypsilon.',
          ' {z} , wie zürich.']),
        ('normalizer_pipeline_de.yaml', '<say-as interpret-as="spell-with-names">ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789'
                                        '</say-as>',
         ['{a} , wie anna.', ' {b} , wie berta.', ' {c} , wie cäsar.', ' {d} , wie daniel.', ' {e} , wie emil.',
          ' {f} , wie friedrich.', ' {g} , wie gustav.', ' {h} , wie heinrich.', ' {i} , wie ida.', ' {j} , wie jakob.',
          ' {k} , wie kaiser.', ' {l} , wie leopold.', ' {m} , wie marie.', ' {n} , wie niklaus.', ' {o} , wie otto.',
          ' {p} , wie peter.', ' {q} , wie quasi.', ' {r} , wie rosa.', ' {s} , wie sophie.', ' {t} , wie theodor.',
          ' {u} , wie ulrich.', ' {v} , wie viktor.', ' {w} , wie wilhelm.', ' {x} , wie xavier.',
          ' {y} , wie ypsilon.',
          ' {z} , wie zürich.', ' eiins.', ' zweiii.', ' dreiii.', ' viieer.', ' fünnff.', ' sex.', ' siiebeenn.',
          ' aachttth.', ' neunhh.']),

    ])
    def test_ssml_processing__spell_with_names(config_path: str, text: str, expected: List[str]) -> None:
        normalizer_pipeline = get_normalizer_pipeline(config_path=config_path)
        normalized_text = normalizer_pipeline.apply(text)
        assert normalized_text == expected

    @staticmethod
    @pytest.mark.parametrize('config_path, text, expected', [
        ('normalizer_pipeline_de.yaml', '<say-as interpret-as="phone">1561187227</say-as>',
         ['eiins.', ' fünnff.', ' sex.', ' eiins.', ' eiins.', ' aachttth.', ' siiebeenn.', ' zweiii.', ' zweiii.',
          ' siiebeenn.']),
        ('normalizer_pipeline_de.yaml', '<say-as interpret-as="phone">+1561187227</say-as>',
         ['{+} .', ' eiins.', ' fünnff.', ' sex.', ' eiins.', ' eiins.', ' aachttth.', ' siiebeenn.', ' zweiii.',
          ' zweiii.',
          ' siiebeenn.']),
        ('normalizer_pipeline_de.yaml', '<say-as interpret-as="phone">+156-118-7227</say-as>',
         ['{+} .', ' eiins.', ' fünnff.', ' sex.', ' {-} .', ' eiins.', ' eiins.', ' aachttth.', ' {-} .',
          ' siiebeenn.',
          ' zweiii.', ' zweiii.', ' siiebeenn.']
         ),
        ('normalizer_pipeline_de.yaml', '<say-as interpret-as="phone">156 118 7227</say-as>',
         ['eiins.', ' fünnff.', ' sex.', ' eiins.', ' eiins.', ' aachttth.', ' siiebeenn.', ' zweiii.', ' zweiii.',
          ' siiebeenn.']),
        ('normalizer_pipeline_de.yaml', '<say-as interpret-as="phone">+156 118 7227</say-as>',
         ['{+} .', ' eiins.', ' fünnff.', ' sex.', ' eiins.', ' eiins.', ' aachttth.', ' siiebeenn.', ' zweiii.',
          ' zweiii.',
          ' siiebeenn.']),

    ])
    def test_ssml_processing__phone(config_path: str, text: str, expected: List[str]) -> None:
        normalizer_pipeline = get_normalizer_pipeline(config_path=config_path)
        normalized_text = normalizer_pipeline.apply(text)
        assert normalized_text == expected

    @staticmethod
    @pytest.mark.parametrize('config_path, text, expected', [
        ('normalizer_pipeline_de.yaml', '<say-as interpret-as="email">abcd@gmail.com</say-as>',
         ['abcd {@} gmail {punkt} com.']),
        ('normalizer_pipeline_de.yaml', '<say-as interpret-as="email">abcd123@gmail.com</say-as>',
         ['abcd hundertdreiiiundzwaanzikk {@} gmail {punkt} com.']),
        ('normalizer_pipeline_de.yaml', '<say-as interpret-as="email">abcd123-_*@gmail.com</say-as>',
         ['abcd hundertdreiiiundzwaanzikk {-} {_} {*} {@} gmail {punkt} com.']),
        ('normalizer_pipeline_de.yaml', '<say-as interpret-as="email">abcd123!#$%^&*()_-+={}[];:@gmail.com</say-as>',
         ['abcd hundertdreiiiundzwaanzikk {ausrufezeichen} {#} {$}  {&} {*} {(} {)} {_} '
          '{-} {+} {=} {  }  {@} gmail {punkt} com.']),

    ])
    def test_ssml_processing__email(config_path: str, text: str, expected: List[str]) -> None:
        normalizer_pipeline = get_normalizer_pipeline(config_path=config_path)
        normalized_text = normalizer_pipeline.apply(text)
        assert normalized_text == expected

    @staticmethod
    @pytest.mark.parametrize('config_path, text, expected', [
        ('normalizer_pipeline_de.yaml', '<say-as interpret-as="url">google.com</say-as>',
         ['google {punkt} com.']),
        ('normalizer_pipeline_de.yaml', '<say-as interpret-as="url">www.google.com</say-as>',
         ['{w} {w} {w} {punkt} google {punkt} com.']),
        ('normalizer_pipeline_de.yaml', '<say-as interpret-as="url">google.com.ar</say-as>',
         ['google {punkt} com {punkt} {a} {r}.']),
        ('normalizer_pipeline_de.yaml', '<say-as interpret-as="url">https://open.spotify.com/playlist'
                                        '/37i9dQZF1E4nr6hJNUgTDh</say-as>',
         ['https : {/} {/} open {punkt} spotify {punkt} com {/} playlist {/} '
          'siiebeennunddreiißßiigkkk i9dqzf eiins e4nr sex hjnugtdh.']),

    ])
    def test_ssml_processing__url(config_path: str, text: str, expected: List[str]) -> None:
        normalizer_pipeline = get_normalizer_pipeline(config_path=config_path)
        normalized_text = normalizer_pipeline.apply(text)
        assert normalized_text == expected