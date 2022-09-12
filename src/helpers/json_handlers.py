import json

import constants.file_structure as fst
import constants.json_settings as jsn


def write_to_json(item, joined_path):
    with open(joined_path, 'w') as f:
        json.dump(item, f, indent=jsn.INDENT_SPACES)

def read_from_json(joined_path):
    with open(joined_path, 'r') as f:
        data = json.load(f)
    return data

def load_remaining():
    return read_from_json(fst.REMAINING)

def write_remaining(remaining):
    write_to_json(remaining, fst.REMAINING)
