import json

import constants.json_settings as json_settings


def write_to_json(item, joined_path):
    with open(joined_path, 'w') as f:
        json.dump(item, f, indent=json_settings.INDENT_SPACES)


def read_from_json(joined_path):
    with open(joined_path, 'r') as f:
        data = json.load(f)
    return data
