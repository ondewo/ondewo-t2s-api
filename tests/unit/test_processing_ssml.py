from normalization.text_markup_dataclass import BaseMarkup
from normalization.text_markup_extractor import CompositeTextMarkupExtractor

import pytest

from normalization.text_processing_ssml import SSMLProcessorFactory


class TestProcessingSSML:

    @staticmethod
    @pytest.mark.parametrize('text, expected_result', [
        ('<say-as interpret-as="spell">ABCD</say-as>', '{AH AH1} .  {B EH1} .  {TZ EH1} .  {D EH EH1} .'),
        ('<say-as interpret-as="spell">A9B109CD</say-as>',
         '{AH AH1} . nouin.  {B EH1} . eins. null. nouin.  {TZ EH1} .  {D EH EH1} .'),
        ('<say-as interpret-as="spell">A9B-109-CD</say-as>',
         '{AH AH1} . nouin.  {B EH1} .  {SH T R IH X} . eins. null. nouin.  {SH T R IH '
         'X} .  {TZ EH1} .  {D EH EH1} .'),
        ('<say-as interpret-as="spell">9657</say-as>', 'nouin. sechss. fünff. sieben.'),
        ('<say-as interpret-as="spell">96AAA57</say-as>',
         'nouin. sechss.  {AH AH1} .  {AH AH1} .  {AH AH1} . fünff. sieben.'),
        ('<say-as interpret-as="spell-with-names">ABCD</say-as>',
         '{AH AH1} , wie  anna.   {B EH1} , wie  berta.   {TZ EH1} , wie  cäsar.   {D '
         'EH EH1} , wie  daniel.'),
        ('<say-as interpret-as="spell-with-names">A9B109CD</say-as>',
         '{AH AH1} , wie  anna.  nouin.  {B EH1} , wie  berta.  eins. null. nouin.  '
         '{TZ EH1} , wie  cäsar.   {D EH EH1} , wie  daniel.'),
        ('<say-as interpret-as="spell-with-names">A9B-109-CD</say-as>',
         '{AH AH1} , wie  anna.  nouin.  {B EH1} , wie  berta.   {SH T R IH X} . eins. '
         'null. nouin.  {SH T R IH X} .  {TZ EH1} , wie  cäsar.   {D EH EH1} , wie  '
         'daniel.'),
        ('<say-as interpret-as="spell-with-names">9657</say-as>', 'nouin. sechss. fünff. sieben.'),
        ('<say-as interpret-as="spell-with-names">96AAA57</say-as>',
         'nouin. sechss.  {AH AH1} , wie  anna.   {AH AH1} , wie  anna.   {AH AH1} , '
         'wie  anna.  fünff. sieben.'),
    ])
    def test_texturize_ssml_de(text: str, expected_result: str) -> None:
        ssml_processor = SSMLProcessorFactory.create_ssml_processor(language='de')
        markup: BaseMarkup = CompositeTextMarkupExtractor.extract(text)[0]
        texturized_texts = ssml_processor.texturize_ssml(markup.text, markup.type, markup.attribute)
        joined_texturized_text = ' '.join([texturized_text.text for texturized_text in texturized_texts])
        assert joined_texturized_text == expected_result

    @staticmethod
    @pytest.mark.parametrize('text, expected_result', [
        ('<say-as interpret-as="spell-with-names">ABCD</say-as>',
         '{AH AH1} , wie  anton.   {B EH1} , wie  berta.   {TZ EH1} , wie  cäsar.   {D '
         'EH EH1} , wie  dora.'),
        ('<say-as interpret-as="spell-with-names">A9B109CD</say-as>',
         '{AH AH1} , wie  anton.  nouin.  {B EH1} , wie  berta.  eins. null. nouin.  '
         '{TZ EH1} , wie  cäsar.   {D EH EH1} , wie  dora.'),
        ('<say-as interpret-as="spell-with-names">A9B-109-CD</say-as>',
         '{AH AH1} , wie  anton.  nouin.  {B EH1} , wie  berta.   {SH T R IH X} . '
         'eins. null. nouin.  {SH T R IH X} .  {TZ EH1} , wie  cäsar.   {D EH EH1} , '
         'wie  dora.'),
        ('<say-as interpret-as="spell-with-names">9657</say-as>', 'nouin. sechss. fünff. sieben.'),
        ('<say-as interpret-as="spell-with-names">96AAA57</say-as>',
         'nouin. sechss.  {AH AH1} , wie  anton.   {AH AH1} , wie  anton.   {AH AH1} , '
         'wie  anton.  fünff. sieben.'),
    ])
    def test_texturize_ssml_at(text: str, expected_result: str) -> None:
        ssml_processor = SSMLProcessorFactory.create_ssml_processor(language='at')
        markup: BaseMarkup = CompositeTextMarkupExtractor.extract(text)[0]
        texturized_texts = ssml_processor.texturize_ssml(markup.text, markup.type, markup.attribute)
        joined_texturized_text = ' '.join([texturized_text.text for texturized_text in texturized_texts])
        assert joined_texturized_text == expected_result

    @staticmethod
    @pytest.mark.parametrize('text, expected_result', [
        ('<say-as interpret-as="spell-with-names">ABCD</say-as>',
         '{EY IH0} , like  alfred.   {B IH0} , like  benjamin.   {S IH1} , like  '
         'charles.   {D IH1} , like  david.'),
        ('<say-as interpret-as="spell-with-names">A9B109CD</say-as>',
         '{EY IH0} , like  alfred.  nine.  {B IH0} , like  benjamin.  one. zero. '
         'nine.  {S IH1} , like  charles.   {D IH1} , like  david.'),
        ('<say-as interpret-as="spell-with-names">A9B-109-CD</say-as>',
         '{EY IH0} , like  alfred.  nine.  {B IH0} , like  benjamin.   {D AE1 SH} . '
         'one. zero. nine.  {D AE1 SH} .  {S IH1} , like  charles.   {D IH1} , like  '
         'david.'),
        ('<say-as interpret-as="spell-with-names">9657</say-as>', 'nine. six. five. seven.'),
        ('<say-as interpret-as="spell-with-names">96AAA57</say-as>',
         'nine. six.  {EY IH0} , like  alfred.   {EY IH0} , like  alfred.   {EY IH0} , '
         'like  alfred.  five. seven.'),
    ])
    def test_texturize_ssml_en(text: str, expected_result: str) -> None:
        ssml_processor = SSMLProcessorFactory.create_ssml_processor(language='en')
        markup: BaseMarkup = CompositeTextMarkupExtractor.extract(text)[0]
        texturized_texts = ssml_processor.texturize_ssml(markup.text, markup.type, markup.attribute)
        joined_texturized_text = ' '.join([texturized_text.text for texturized_text in texturized_texts])
        assert joined_texturized_text == expected_result
