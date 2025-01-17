import os
import re
import sys

import mve.src.constants.colours as colours

import mve.src.helpers.colouring as colouring


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
        # __main__.py [log/no-log] [script name without py]
        os.path.basename(sys.argv[2])
    )
    print(
        '{} {} {}'.format(
            colouring.colour_box(colours.GREEN, 'success', bold), base_name,
            message, bold)
    )


def plural(number: int) -> str:
    return '' if number == 1 else 's'


def format_remaining(num_remaining: int, bold: bool) -> str:
    coloured_remaining = colouring.colour_format(
        colours.CYAN, str(num_remaining), bold)
    return 'exited with {} file{} remaining'.format(
        coloured_remaining, plural(num_remaining)
    )


def exit_success(message: str, bold: bool):
    print_success(message, bold)
    sys.exit(0)


def exit_treat_all_good(bold: bool):
    exit_success('successfully treated all files', bold)
