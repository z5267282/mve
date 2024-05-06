import os
import pathlib

# files
CONFIG    = 'config.py'
REMAINING = 'remaining.json'

PARENT = list(
    pathlib.Path(
        os.getenv('MVE_HISTORY', '..')
    ).parts
)

# folders
QUEUE   = PARENT + ['queue']
HISTORY = PARENT + ['history']
ERRORS  = PARENT + ['errors']

# configs
CONFIGS = ['configs']
CURRENT_CONFIG = 'current.json'
