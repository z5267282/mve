import datetime as dt
import json
import sys

import config as cfg

import constants.colour as clr
import constants.json_settings as jsn
import constants.file_structure as fst
import constants.treatment_format as trf

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

def generate_timestamped_file_name():
    return f'{get_timestamp()}.json'


def stderr_print(message):
    print(message, file=sys.stderr)


def generate_paths_dict():
    return {
        trf.SOURCE_PATH      : cfg.SOURCE,
        trf.RENAME_PATH      : cfg.RENAMES,
        trf.DESTINATION_PATH : cfg.DESTINATION
    }


def colour_print(colour, string):
    return f'{colour}{string}{clr.RESET}'

def highlight(string):
    return colour_print(clr.BLUE, string)


def print_error(message):
    stderr_print(f'[ {clr.RED}error{clr.RESET} ] {message}')


def exit_success(message):
    print(f'[ {colour_print(clr.GREEN, "success")} ] {message}')
    sys.exit(0)