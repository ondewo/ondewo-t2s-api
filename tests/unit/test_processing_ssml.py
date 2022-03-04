from normalization.text_markup_dataclass import BaseMarkup
from normalization.text_markup_extractor import CompositeTextMarkupExtractor

import pytest

from normalization.text_processing_ssml import SSMLProcessorFactory


class TestProcessingSSML:

    @staticmethod
    @pytest.mark.parametrize('text, expected_result', [
        ('<say-as interpret-as="spell">ABCD</say-as>', 'ah beh tsehe deh'),
        ('<say-as interpret-as="spell">A9B109CD</say-as>', 'ah  neun  beh  eins null neun  tsehe deh'),
        ('<say-as interpret-as="spell">A9B-109-CD</say-as>', 'ah  neun  beh strich  eins null neun  strich tsehe deh'),
        ('<say-as interpret-as="spell">9657</say-as>', 'neun sechs fünf sieben'),
        ('<say-as interpret-as="spell">96AAA57</say-as>', 'neun sechs  ah ah ah  fünf sieben'),
        ('<say-as interpret-as="spell-with-names">ABCD</say-as>',
         'ah , wie  anna.   beh , wie  berta.   tsehe , wie  cäsar.   deh , wie  daniel.'),
        ('<say-as interpret-as="spell-with-names">A9B109CD</say-as>',
         'ah , wie  anna.  neun  beh , wie  berta.  eins null neun  tsehe , wie  '
         'cäsar.   deh , wie  daniel.'),
        ('<say-as interpret-as="spell-with-names">A9B-109-CD</say-as>',
         'ah , wie  anna.  neun  beh , wie  berta.   strich  eins null neun  strich '
         'tsehe , wie  cäsar.   deh , wie  daniel.'),
        ('<say-as interpret-as="spell-with-names">9657</say-as>', 'neun sechs fünf sieben'),
        ('<say-as interpret-as="spell-with-names">96AAA57</say-as>',
         'neun sechs  ah , wie  anna.   ah , wie  anna.   ah , wie  anna.  fünf sieben'),
    ])
    def test_texturize_ssml_de(text: str, expected_result: str) -> None:
        ssml_processor = SSMLProcessorFactory.create_ssml_processor(language='de')
        markup: BaseMarkup = CompositeTextMarkupExtractor.extract(text)[0]
        texturized_texts = ssml_processor.texturize_ssml(markup.text, markup.type, markup.attribute)
        joined_texturized_text = ' '.join([texturized_text.text for texturized_text in texturized_texts])
        assert joined_texturized_text == expected_result

    @staticmethod
    @pytest.mark.parametrize('text, expected_result', [
        ('<say-as interpret-as="spell">ABCD</say-as>', 'ah beh tsehe deh'),
        ('<say-as interpret-as="spell">A9B109CD</say-as>', 'ah  neun  beh  eins null neun  tsehe deh'),
        ('<say-as interpret-as="spell">A9B-109-CD</say-as>', 'ah  neun  beh strich  eins null neun  strich tsehe deh'),
        ('<say-as interpret-as="spell">9657</say-as>', 'neun sechs fünf sieben'),
        ('<say-as interpret-as="spell">96AAA57</say-as>', 'neun sechs  ah ah ah  fünf sieben'),
        ('<say-as interpret-as="spell-with-names">ABCD</say-as>',
         'ah , wie  anton.   beh , wie  berta.   tsehe , wie  cäsar.   deh , wie  dora.'),
        ('<say-as interpret-as="spell-with-names">A9B109CD</say-as>',
         'ah , wie  anton.  neun  beh , wie  berta.  eins null neun  tsehe , wie  '
         'cäsar.   deh , wie  dora.'),
        ('<say-as interpret-as="spell-with-names">A9B-109-CD</say-as>',
         'ah , wie  anton.  neun  beh , wie  berta.   strich  eins null neun  strich '
         'tsehe , wie  cäsar.   deh , wie  dora.'),
        ('<say-as interpret-as="spell-with-names">9657</say-as>', 'neun sechs fünf sieben'),
        ('<say-as interpret-as="spell-with-names">96AAA57</say-as>',
         'neun sechs  ah , wie  anton.   ah , wie  anton.   ah , wie  anton.  fünf '
         'sieben'),
    ])
    def test_texturize_ssml_at(text: str, expected_result: str) -> None:
        ssml_processor = SSMLProcessorFactory.create_ssml_processor(language='at')
        markup: BaseMarkup = CompositeTextMarkupExtractor.extract(text)[0]
        texturized_texts = ssml_processor.texturize_ssml(markup.text, markup.type, markup.attribute)
        joined_texturized_text = ' '.join([texturized_text.text for texturized_text in texturized_texts])
        assert joined_texturized_text == expected_result

    @staticmethod
    @pytest.mark.parametrize('text, expected_result', [
        ('<say-as interpret-as="spell">ABCD</say-as>', 'ei bee cee dee'),
        ('<say-as interpret-as="spell">A9B109CD</say-as>', 'ei  nine  bee  one zero nine  cee dee'),
        ('<say-as interpret-as="spell">A9B-109-CD</say-as>', 'ei  nine  bee dash  one zero nine  dash cee dee'),
        ('<say-as interpret-as="spell">9657</say-as>', 'nine six five seven'),
        ('<say-as interpret-as="spell">96AAA57</say-as>', 'nine six  ei ei ei  five seven'),
        ('<say-as interpret-as="spell-with-names">ABCD</say-as>',
         'ei , like  alfred.   bee , like  benjamin.   cee , like  charles.   dee , '
         'like  david.'),
        ('<say-as interpret-as="spell-with-names">A9B109CD</say-as>',
         'ei , like  alfred.  nine  bee , like  benjamin.  one zero nine  cee , like  '
         'charles.   dee , like  david.'),
        ('<say-as interpret-as="spell-with-names">A9B-109-CD</say-as>',
         'ei , like  alfred.  nine  bee , like  benjamin.   dash  one zero nine  dash '
         'cee , like  charles.   dee , like  david.'),
        ('<say-as interpret-as="spell-with-names">9657</say-as>', 'nine six five seven'),
        ('<say-as interpret-as="spell-with-names">96AAA57</say-as>',
         'nine six  ei , like  alfred.   ei , like  alfred.   ei , like  alfred.  five '
         'seven'),
    ])
    def test_texturize_ssml_en(text: str, expected_result: str) -> None:
        ssml_processor = SSMLProcessorFactory.create_ssml_processor(language='en')
        markup: BaseMarkup = CompositeTextMarkupExtractor.extract(text)[0]
        texturized_texts = ssml_processor.texturize_ssml(markup.text, markup.type, markup.attribute)
        joined_texturized_text = ' '.join([texturized_text.text for texturized_text in texturized_texts])
        assert joined_texturized_text == expected_result
