import datetime as dt
import json
import sys

import constants.json_settings as jsn
import constants.file_structure as fst

def write_to_json(item, file_path):
    with open(file_path, 'w') as f:
        json.dump(item, f, indent=jsn.INDENT_SPACES)

def read_from_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def load_remaining():
    return read_from_json(fst.REMAINING) 

def write_remaining(remaining):
    write_to_json(remaining, fst.REMAINING)


def get_timestamp():
    right_now = dt.datetime.now()
    return right_now.strftime('%d.%m.%Y - %H%M')


def stderr_print(message):
    print(message, file=sys.stderr)
