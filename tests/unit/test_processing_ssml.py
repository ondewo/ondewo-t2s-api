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
        ('<say-as interpret-as="spell">ABCD</say-as>', '{aaah.} {beehh.} {zeeh.} {deeehh.}'),
        ('<say-as interpret-as="spell">A9B109CD</say-as>',
         '{aaah.}  nouin.  {beehh.}  eins. null. nouin.  {zeeh.} {deeehh.}'),
        ('<say-as interpret-as="spell">A9B-109-CD</say-as>',
         '{aaah.}  nouin.  {beehh.} {Bindestrich.}  eins. null. nouin.  {Bindestrich.} '
         '{zeeh.} {deeehh.}'),
        ('<say-as interpret-as="spell">9657</say-as>', 'nouin. sechss. fünff. sieben.'),
        ('<say-as interpret-as="spell">96AAA57</say-as>',
         'nouin. sechss.  {aaah.} {aaah.} {aaah.}  fünff. sieben.'),
        ('<say-as interpret-as="spell-with-names">ABCD</say-as>',
         '{aaah} , wie  anton.   {beehh} , wie  berta.   {zeeh} , wie  cäsar.   '
         '{deeehh} , wie  dora.'),
        ('<say-as interpret-as="spell-with-names">A9B109CD</say-as>',
         '{aaah} , wie  anton.  nouin.  {beehh} , wie  berta.  eins. null. nouin.  '
         '{zeeh} , wie  cäsar.   {deeehh} , wie  dora.'),
        ('<say-as interpret-as="spell-with-names">A9B-109-CD</say-as>',
         '{aaah} , wie  anton.  nouin.  {beehh} , wie  berta.   {Bindestrich.}  eins. '
         'null. nouin.  {Bindestrich.} {zeeh} , wie  cäsar.   {deeehh} , wie  dora.'),
        ('<say-as interpret-as="spell-with-names">9657</say-as>', 'nouin. sechss. fünff. sieben.'),
        ('<say-as interpret-as="spell-with-names">96AAA57</say-as>',
         'nouin. sechss.  {aaah} , wie  anton.   {aaah} , wie  anton.   {aaah} , wie  '
         'anton.  fünff. sieben.'),
    ])
    def test_texturize_ssml_at(text: str, expected_result: str) -> None:
        ssml_processor = SSMLProcessorFactory.create_ssml_processor(language='at')
        markup: BaseMarkup = CompositeTextMarkupExtractor.extract(text)[0]
        texturized_texts = ssml_processor.texturize_ssml(markup.text, markup.type, markup.attribute)
        joined_texturized_text = ' '.join([texturized_text.text for texturized_text in texturized_texts])
        assert joined_texturized_text == expected_result

    @staticmethod
    @pytest.mark.parametrize('text, expected_result', [
        ('<say-as interpret-as="spell">ABCD</say-as>', '{ei.} {bee.} {cee.} {dee.}'),
        ('<say-as interpret-as="spell">A9B109CD</say-as>',
         '{ei.}  nine.  {bee.}  one. zero. nine.  {cee.} {dee.}'),
        ('<say-as interpret-as="spell">A9B-109-CD</say-as>',
         '{ei.}  nine.  {bee.} {dash.}  one. zero. nine.  {dash.} {cee.} {dee.}'),
        ('<say-as interpret-as="spell">9657</say-as>', 'nine. six. five. seven.'),
        ('<say-as interpret-as="spell">96AAA57</say-as>', 'nine. six.  {ei.} {ei.} {ei.}  five. seven.'),
        ('<say-as interpret-as="spell-with-names">ABCD</say-as>',
         '{ei} , like  alfred.   {bee} , like  benjamin.   {cee} , like  charles.   '
         '{dee} , like  david.'),
        ('<say-as interpret-as="spell-with-names">A9B109CD</say-as>',
         '{ei} , like  alfred.  nine.  {bee} , like  benjamin.  one. zero. nine.  '
         '{cee} , like  charles.   {dee} , like  david.'),
        ('<say-as interpret-as="spell-with-names">A9B-109-CD</say-as>',
         '{ei} , like  alfred.  nine.  {bee} , like  benjamin.   {dash.}  one. zero. '
         'nine.  {dash.} {cee} , like  charles.   {dee} , like  david.'),
        ('<say-as interpret-as="spell-with-names">9657</say-as>', 'nine. six. five. seven.'),
        ('<say-as interpret-as="spell-with-names">96AAA57</say-as>',
         'nine. six.  {ei} , like  alfred.   {ei} , like  alfred.   {ei} , like  '
         'alfred.  five. seven.'),
    ])
    def test_texturize_ssml_en(text: str, expected_result: str) -> None:
        ssml_processor = SSMLProcessorFactory.create_ssml_processor(language='en')
        markup: BaseMarkup = CompositeTextMarkupExtractor.extract(text)[0]
        texturized_texts = ssml_processor.texturize_ssml(markup.text, markup.type, markup.attribute)
        joined_texturized_text = ' '.join([texturized_text.text for texturized_text in texturized_texts])
        assert joined_texturized_text == expected_result
