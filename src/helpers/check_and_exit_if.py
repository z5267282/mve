import os
import sys

import constants.error as error

import helpers.colouring as colouring
import helpers.files as files
import helpers.util as util


def bad_args(argv: list[str], length: int, usage_message: str = ''):
    program_name, args = argv[0], argv[1:]

    if len(args) == length:
        return

    util.stderr_print(
        'usage: python3 {}{}{}'.format(
            os.path.basename(program_name),
            ' ' if usage_message else '',
            usage_message
        )
    )
    sys.exit(error.BAD_COMMAND_LINE_ARGS)


def no_file(joined_path, desc, code):
    if not os.path.exists(joined_path):
        util.stderr_print(
            f"the {desc} file '{colouring.highlight(joined_path)}' does not exist")
        sys.exit(code)


def no_folder(folder_paths: list[str], folder_desc: str, exit_code: int):
    if not files.folder_exists(folder_paths):
        util.stderr_print(
            f"{folder_desc} folder '{folder_paths}' does not exist")
        sys.exit(exit_code)
