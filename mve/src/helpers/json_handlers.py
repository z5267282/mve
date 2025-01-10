import json
import typing

import mve.src.constants.json_settings as json_settings


def write_to_json(item: typing.Any, joined_path: str):
    with open(joined_path, 'w') as f:
        json.dump(item, f, indent=json_settings.INDENT_SPACES)


def read_from_json(joined_path: str) -> typing.Any:
    with open(joined_path, 'r') as f:
        data = json.load(f)
    return data
