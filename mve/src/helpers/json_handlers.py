import json
import sys
import typing

import mve.src.constants.error as error
import mve.src.constants.json_settings as json_settings

import mve.src.helpers.colouring as colouring
import mve.src.helpers.files as files
import mve.src.helpers.util as util


def write_to_json(item: typing.Any, joined_path: str):
    with open(joined_path, 'w') as f:
        json.dump(item, f, indent=json_settings.INDENT_SPACES)


def read_from_json(joined_path: str, bold: bool) -> typing.Any:
    try:
        with open(joined_path, 'r') as f:
            data = json.load(f)
        return data
    except json.decoder.JSONDecodeError as e:
        coloured_path = colouring.highlight_path(
            files.split_path(joined_path), bold)
        util.print_error(
            f"syntax error in the json file '{coloured_path}'", bold)
        print(str(e))
        sys.exit(error.BAD_JSON_FILE)
