import json
from typing import List

from normalization.text_preprocessing_de import TextNormalizer

normalizer = TextNormalizer()


def normalize(list_of_strings: List[str]) -> List[str]:
    """

    Args:
        list_of_strings:

    Returns:

    """
    list_of_strings_normalized: List[str] = []
    for text in list_of_strings:
        normalized_split_texts: List[str] = normalizer.normalize_and_split(text=text)
        list_of_strings_normalized.extend(normalized_split_texts)
    list_of_strings_normalized = list(set(list_of_strings_normalized))
    return list_of_strings_normalized


if __name__ == '__main__':
    with open('training/data/text/usays_umbuchen.json', mode='r') as f:
        list_of_string: List[str] = json.load(f)

    list_of_string = normalize(list_of_string)

    with open('training/data/text/usays_um_normalized.json', mode='w') as f:
        json.dump(list_of_string, f)
