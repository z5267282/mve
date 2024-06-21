import os
import re
import sys

import constants.colours as colours

import helpers.colouring as colouring


def stderr_print(message: str):
    print(message, file=sys.stderr)


def print_error(message: str):
    stderr_print('{} {}'.format(
        colouring.colour_box(colours.RED, 'error'), message
    ))


def print_success(message: str):
    base_name = re.sub(
        r'\.py$', r'',
        os.path.basename(sys.argv[0])
    )
    print(
        '{} {} {}'.format(
            colouring.colour_box(colours.GREEN, 'success'), base_name, message
        )
    )


def format_remaining(num_remaining: int, bold: bool) -> str:
    return 'exited with {} file{} remaining'.format(
        colouring.colour_format(colours.CYAN, num_remaining, bold),
        str() if num_remaining == 1 else 's'
    )


def exit_success(message: str):
    print_success(message)
    sys.exit(0)


def exit_treat_all_good():
    exit_success('successfully treated all files')
