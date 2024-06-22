import os
import re
import sys

import constants.colours as colours

import helpers.colouring as colouring


def stderr_print(message: str):
    print(message, file=sys.stderr)


def print_error(message: str, bold: bool):
    stderr_print(
        '{} {}'.format(
            colouring.colour_box(colours.RED, 'error', bold), message
        )
    )


def print_success(message: str, bold: bool):
    base_name = re.sub(
        r'\.py$', r'',
        os.path.basename(sys.argv[0])
    )
    print(
        '{} {} {}'.format(
            colouring.colour_box(colours.GREEN, 'success', bold), base_name,
            message, bold)
    )


def format_remaining(num_remaining: int, bold: bool) -> str:
    coloured_remaining = colouring.colour_format(
        colours.CYAN, str(num_remaining), bold)
    plural = '' if num_remaining == 1 else 's'
    return 'exited with {} file{} remaining'.format(
        coloured_remaining, plural)


def exit_success(message: str, bold: bool):
    print_success(message, bold)
    sys.exit(0)


def exit_treat_all_good(bold: bool):
    exit_success('successfully treated all files', bold)
