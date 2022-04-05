import pytest

from normalization.text_preprocessing_nato import TextNormalizerATC

normalizer = TextNormalizerATC()


class TestNormalizationATC:

    @staticmethod
    @pytest.mark.parametrize('number, expected_result', [
        ('0', 'zero'),
        ('000', 'zero zero zero'),
        ('10', 'wun zero'),
        ('100', 'wun hun dred'),
        ('1000', 'wun tousand'),
        ('1500', 'wun tousand fife hun dred'),
        ('22500', 'too too tousand fife hun dred'),
        ('0022500', 'zero zero too too tousand fife hun dred'),
    ])
    def test_texturize_single_number(number: str, expected_result: str) -> None:
        number_text = normalizer.texturize_single_number(number)
        assert isinstance(number_text, str)
        assert number_text == expected_result

    @staticmethod
    @pytest.mark.parametrize('number, expected_result', [
        ('0.0', 'zero, dayseemal, zero,'),
        ('000.000', 'zero zero zero, dayseemal, zero zero zero,'),
        ('0022500.0022500', 'zero zero too too tousand fife hun dred, '
                            'dayseemal, zero zero too too tousand fife hun dred,'),
    ])
    def test_texturize_numbers(number: str, expected_result: str) -> None:
        number_text = normalizer.texturize_numbers(number)
        assert isinstance(number_text, str)
        assert number_text == expected_result
