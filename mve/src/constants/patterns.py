from mve.src.constants.timestamp_format import SHORT_HAND
from mve.src.helpers.pattern import Pattern

CONFIG_NAME: Pattern = Pattern(
    r'[a-z0-9-]+',  'alphanumeric characters or hyphens')
INTEGER_SECONDS: Pattern = Pattern(r'-?[0-9]+', 'integer number of seconds')
LEADING_NUMBER: Pattern = Pattern(r'[0-9]+', 'leading number')
TREATED_FILE_NAME: Pattern = Pattern(
    r'[a-zA-Z0-9 .\-_]+', "alphanumeric characters, ' ', '.', '-', or '_'")
TIMESTAMP: Pattern = Pattern(
    fr'([0-5]?[0-9]{SHORT_HAND})?[0-5]?[0-9]{SHORT_HAND}[0-5]?[0-9]',
    f'timestamp in form <[hour]{SHORT_HAND}min{SHORT_HAND}sec>')
