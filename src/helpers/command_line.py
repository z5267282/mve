import os.path
import sys

import constants.error as err 
import util

def command_line_error(argv):
    program_name, args = argv[0], argv[1:]
    if args:
        util.stderr_print(f'usage: {os.path.basename(program_name)}')
        sys.exit(err.BAD_COMMAND_LINE_ARGS)
