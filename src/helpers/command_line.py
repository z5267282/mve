from os.path import basename
from sys import exit

from ..constants.command import COMMAND_LINE_LENGTH
from ..constants.error_numbers import BAD_COMMAND_LINE_ARGS

def command_line_error(program_name, args):
    if len(args) != COMMAND_LINE_LENGTH:
        print(f'usage: {basename(program_name)}')
        exit(BAD_COMMAND_LINE_ARGS)
