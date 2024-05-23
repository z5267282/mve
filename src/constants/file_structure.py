import os
import pathlib


# folders

def make_history_paths(base_paths: list[str]) -> list[str]:
    parent = pathlib.Path(
        os.getenv('MVE_HISTORY', '..')
    )
    return parent + base_paths


# folders
QUEUE = make_history_paths(['queue'])
HISTORY = make_history_paths(['history'])
ERRORS = make_history_paths(['errors'])
CONFIGS = make_history_paths(['configs'])

# files
REMAINING = "remaining.json"
CONFIG = "config.json"
