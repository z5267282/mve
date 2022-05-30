import os.path
import sys

import constants.commands as commands 
import constants.error_numbers as error_numbers

def command_line_error(argv):
    program_name, args = argv[0], argv[1:]
    if len(args) != commands.COMMAND_LINE_LENGTH:
        print(f'usage: {os.path.basename(program_name)}')
        sys.exit(error_numbers.BAD_COMMAND_LINE_ARGS)
