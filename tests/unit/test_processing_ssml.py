from normalization.text_markup_dataclass import BaseMarkup
from normalization.text_markup_extractor import CompositeTextMarkupExtractor

import pytest

from normalization.text_processing_ssml import SSMLProcessorFactory

ssml_processor_de = SSMLProcessorFactory.create_ssml_processor(language='de')
ssml_processor_en = SSMLProcessorFactory.create_ssml_processor(language='en')
ssml_processor_at = SSMLProcessorFactory.create_ssml_processor(language='at')


class TestProcessingSSML:

    @staticmethod
    @pytest.mark.parametrize('text, expected_result', [
        ('<say-as interpret-as="spell">ABCD</say-as>',
         f'{ssml_processor_de.text_normalizer.char_mapping["a"]} .  '
         f'{ssml_processor_de.text_normalizer.char_mapping["b"]} .  '
         f'{ssml_processor_de.text_normalizer.char_mapping["c"]} .  '
         f'{ssml_processor_de.text_normalizer.char_mapping["d"]} .'),
        ('<say-as interpret-as="spell">A9B109CD</say-as>',
         f'{ssml_processor_de.text_normalizer.char_mapping["a"]} . nouin.  '
         f'{ssml_processor_de.text_normalizer.char_mapping["b"]} . eins. null. nouin.  '
         f'{ssml_processor_de.text_normalizer.char_mapping["c"]} .  '
         f'{ssml_processor_de.text_normalizer.char_mapping["d"]} .'),
        ('<say-as interpret-as="spell">A9B-109-CD</say-as>',
         f'{ssml_processor_de.text_normalizer.char_mapping["a"]} . nouin.  '
         f'{ssml_processor_de.text_normalizer.char_mapping["b"]} .  '
         f'{ssml_processor_de.text_normalizer.char_mapping["-"]} . eins. null. nouin.  '
         f'{ssml_processor_de.text_normalizer.char_mapping["-"]} .  '
         f'{ssml_processor_de.text_normalizer.char_mapping["c"]} .  '
         f'{ssml_processor_de.text_normalizer.char_mapping["d"]} .'),
        ('<say-as interpret-as="spell">9657</say-as>', 'nouin. sechss. fünff. sieben.'),
        ('<say-as interpret-as="spell">96AAA57</say-as>',
         f'nouin. sechss.  {ssml_processor_de.text_normalizer.char_mapping["a"]} .  '
         f'{ssml_processor_de.text_normalizer.char_mapping["a"]} .  '
         f'{ssml_processor_de.text_normalizer.char_mapping["a"]} . fünff. sieben.'),
        ('<say-as interpret-as="spell-with-names">ABCD</say-as>',
         f'{ssml_processor_de.text_normalizer.char_mapping["a"]} , wie  anna.   '
         f'{ssml_processor_de.text_normalizer.char_mapping["b"]} , wie  berta.   '
         f'{ssml_processor_de.text_normalizer.char_mapping["c"]} , wie  cäsar.   '
         f'{ssml_processor_de.text_normalizer.char_mapping["d"]} , wie  daniel.'),
        ('<say-as interpret-as="spell-with-names">A9B109CD</say-as>',
         f'{ssml_processor_de.text_normalizer.char_mapping["a"]} , wie  anna.  nouin.  '
         f'{ssml_processor_de.text_normalizer.char_mapping["b"]} , wie  berta.  eins. null. nouin.  '
         f'{ssml_processor_de.text_normalizer.char_mapping["c"]} , wie  cäsar.   '
         f'{ssml_processor_de.text_normalizer.char_mapping["d"]} , wie  daniel.'),
        ('<say-as interpret-as="spell-with-names">A9B-109-CD</say-as>',
         f'{ssml_processor_de.text_normalizer.char_mapping["a"]} , wie  anna.  nouin.  '
         f'{ssml_processor_de.text_normalizer.char_mapping["b"]} , wie  berta.   '
         f'{ssml_processor_de.text_normalizer.char_mapping["-"]} . eins. '
         f'null. nouin.  {ssml_processor_de.text_normalizer.char_mapping["-"]} .  '
         f'{ssml_processor_de.text_normalizer.char_mapping["c"]} , wie  cäsar.   '
         f'{ssml_processor_de.text_normalizer.char_mapping["d"]} , wie  daniel.'
         ),
        ('<say-as interpret-as="spell-with-names">9657</say-as>', 'nouin. sechss. fünff. sieben.'),
        ('<say-as interpret-as="spell-with-names">96AAA57</say-as>',
         f'nouin. sechss.  {ssml_processor_de.text_normalizer.char_mapping["a"]} , wie  anna.   '
         f'{ssml_processor_de.text_normalizer.char_mapping["a"]} , wie  anna.   '
         f'{ssml_processor_de.text_normalizer.char_mapping["a"]} , wie  anna.  fünff. sieben.'),
    ])
    def test_texturize_ssml_de(text: str, expected_result: str) -> None:
        markup: BaseMarkup = CompositeTextMarkupExtractor.extract(text)[0]
        texturized_texts = ssml_processor_de.texturize_ssml(markup.text, markup.type, markup.attribute)
        joined_texturized_text = ' '.join([texturized_text.text for texturized_text in texturized_texts])
        assert joined_texturized_text == expected_result

    @staticmethod
    @pytest.mark.parametrize('text, expected_result', [
        ('<say-as interpret-as="spell-with-names">ABCD</say-as>',
         f'{ssml_processor_at.text_normalizer.char_mapping["a"]} , wie  anton.   '
         f'{ssml_processor_at.text_normalizer.char_mapping["b"]} , wie  berta.   '
         f'{ssml_processor_at.text_normalizer.char_mapping["c"]} , wie  cäsar.   '
         f'{ssml_processor_at.text_normalizer.char_mapping["d"]} , wie  dora.'),
        ('<say-as interpret-as="spell-with-names">A9B109CD</say-as>',
         f'{ssml_processor_at.text_normalizer.char_mapping["a"]} , wie  anton.  nouin.  '
         f'{ssml_processor_at.text_normalizer.char_mapping["b"]} , wie  berta.  eins. null. nouin.  '
         f'{ssml_processor_at.text_normalizer.char_mapping["c"]} , wie  cäsar.   '
         f'{ssml_processor_at.text_normalizer.char_mapping["d"]} , wie  dora.'),
        ('<say-as interpret-as="spell-with-names">A9B-109-CD</say-as>',
         f'{ssml_processor_at.text_normalizer.char_mapping["a"]} , wie  anton.  nouin.  '
         f'{ssml_processor_at.text_normalizer.char_mapping["b"]} , wie  berta.   '
         f'{ssml_processor_at.text_normalizer.char_mapping["-"]} . eins. '
         f'null. nouin.  {ssml_processor_at.text_normalizer.char_mapping["-"]} .  '
         f'{ssml_processor_at.text_normalizer.char_mapping["c"]} , wie  cäsar.   '
         f'{ssml_processor_at.text_normalizer.char_mapping["d"]} , wie  dora.'),
        ('<say-as interpret-as="spell-with-names">9657</say-as>', 'nouin. sechss. fünff. sieben.'),
        ('<say-as interpret-as="spell-with-names">96AAA57</say-as>',
         f'nouin. sechss.  {ssml_processor_at.text_normalizer.char_mapping["a"]} , wie  anton.   '
         f'{ssml_processor_at.text_normalizer.char_mapping["a"]} , wie  anton.   '
         f'{ssml_processor_at.text_normalizer.char_mapping["a"]} , '
         'wie  anton.  fünff. sieben.'),
    ])
    def test_texturize_ssml_at(text: str, expected_result: str) -> None:
        markup: BaseMarkup = CompositeTextMarkupExtractor.extract(text)[0]
        texturized_texts = ssml_processor_at.texturize_ssml(markup.text, markup.type, markup.attribute)
        joined_texturized_text = ' '.join([texturized_text.text for texturized_text in texturized_texts])
        assert joined_texturized_text == expected_result

    @staticmethod
    @pytest.mark.parametrize('text, expected_result', [
        ('<say-as interpret-as="spell-with-names">ABCD</say-as>',
         f'{ssml_processor_en.text_normalizer.char_mapping["a"]} , like  alfred.   '
         f'{ssml_processor_en.text_normalizer.char_mapping["b"]} , like  benjamin.   '
         f'{ssml_processor_en.text_normalizer.char_mapping["c"]} , like  '
         f'charles.   {ssml_processor_en.text_normalizer.char_mapping["d"]} , like  david.'),
        ('<say-as interpret-as="spell-with-names">A9B109CD</say-as>',
         f'{ssml_processor_en.text_normalizer.char_mapping["a"]} , '
         f'like  alfred.  nine.  {ssml_processor_en.text_normalizer.char_mapping["b"]} , like  benjamin.  one. zero. '
         f'nine.  {ssml_processor_en.text_normalizer.char_mapping["c"]} , '
         f'like  charles.   {ssml_processor_en.text_normalizer.char_mapping["d"]} , like  david.'),
        ('<say-as interpret-as="spell-with-names">A9B-109-CD</say-as>',
         f'{ssml_processor_en.text_normalizer.char_mapping["a"]} , like  alfred.  nine.  '
         f'{ssml_processor_en.text_normalizer.char_mapping["b"]} , like  benjamin.   '
         f'{ssml_processor_en.text_normalizer.char_mapping["-"]} . one. zero. nine.  '
         f'{ssml_processor_en.text_normalizer.char_mapping["-"]} .  '
         f'{ssml_processor_en.text_normalizer.char_mapping["c"]} , like  charles.   '
         f'{ssml_processor_en.text_normalizer.char_mapping["d"]} , like  david.'),
        ('<say-as interpret-as="spell-with-names">9657</say-as>', 'nine. six. five. seven.'),
        ('<say-as interpret-as="spell-with-names">96AAA57</say-as>',
         f'nine. six.  {ssml_processor_en.text_normalizer.char_mapping["a"]} , like  alfred.   '
         f'{ssml_processor_en.text_normalizer.char_mapping["a"]} , like  alfred.   '
         f'{ssml_processor_en.text_normalizer.char_mapping["a"]} , '
         'like  alfred.  five. seven.'),
    ])
    def test_texturize_ssml_en(text: str, expected_result: str) -> None:
        markup: BaseMarkup = CompositeTextMarkupExtractor.extract(text)[0]
        texturized_texts = ssml_processor_en.texturize_ssml(markup.text, markup.type, markup.attribute)
        joined_texturized_text = ' '.join([texturized_text.text for texturized_text in texturized_texts])
        assert joined_texturized_text == expected_result
