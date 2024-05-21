import os
import pathlib


def make_history_paths(base_paths: list[str]) -> list[str]:
    parent = pathlib.Path(
        os.getenv('MVE_HISTORY', '..')
    )
    return parent + base_paths


QUEUE = make_history_paths(['queue'])
HISTORY = make_history_paths(['history'])
ERRORS = make_history_paths(['errors'])
CONFIGS = make_history_paths(['configs'])
