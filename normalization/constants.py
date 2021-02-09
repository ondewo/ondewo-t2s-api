import re

UUID4_RGX: str = r'[^\W_]{8}-[^\W_]{4}-[^\W_]{4}-[^\W_]{4}-[^\W_]{12}'
CUSTOM_PHONEMIZER_PREFIX: str = r'[A-Za-z_1-9\-]*'
CUSTOM_PHONEMIZER_ID: str = rf'(:?[A-Za-z_1-9\-]*_)?{UUID4_RGX}'
CUSTOM_PHONEMIZER_ID_PTTRN: re.Pattern = re.compile(CUSTOM_PHONEMIZER_ID)
CUSTOM_PHONEMIZER_PREFIX_PTTRN: re.Pattern = re.compile(CUSTOM_PHONEMIZER_PREFIX)
