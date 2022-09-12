import datetime as dt
import json
import os
import re
import sys

import config as cfg

import constants.colour as clr
import constants.treatment_format as trf


# Timestamping

def get_timestamp():
    right_now = dt.datetime.now()
    return right_now.strftime('%d.%m.%Y - %H%M')

def generate_timestamped_file_name():
    return f'{get_timestamp()}.json'


# Stderr

def stderr_print(message):
    print(message, file=sys.stderr)


# Treatment format

def generate_paths_dict():
    return {
        trf.SOURCE_PATH      : cfg.SOURCE,
        trf.RENAME_PATH      : cfg.RENAMES,
        trf.DESTINATION_PATH : cfg.DESTINATION
    }


# Colours

def colour_format(colour, string):
    return f'{colour}{string}{clr.RESET}'

def highlight(string):
    return colour_format(clr.BLUE, string)

def colour_box(colour, message):
    return f'[ {colour_format(colour, message)} ]'


# Errors

def print_error(message):
    stderr_print(f'{colour_box(clr.RED, "error")} {message}')


# Success

def exit_success(message):
    base_name = re.sub(
        r'\.py$', '',
        os.path.basename(sys.argv[0])
    )
    print(f'{colour_box(clr.GREEN, "success")} {base_name} {message}')
    sys.exit(0)
