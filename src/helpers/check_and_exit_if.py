import os
import sys

import config as cfg

import constants.error as err
import constants.file_structure as fst

import helpers.colours as colours
import helpers.files as files
import helpers.util as util


# Command line args checking

def bad_args(argv, length, usage_message):
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
    sys.exit(err.BAD_COMMAND_LINE_ARGS)


def no_args(argv):
    bad_args(argv, 0, '')


# File checking

def no_file(joined_path, desc, code):
    if not os.path.exists(joined_path):
        util.stderr_print(
            f"the {desc} file '{colours.highlight(joined_path)}' does not exist")
        sys.exit(code)


# Folder checking

def no_folder(folder_paths: list[str], folder_desc: str, exit_code: int):
    if not files.folder_exists(folder_paths):
        util.stderr_print(
            f"{folder_desc} folder '{folder_paths}' does not exist")
        sys.exit(exit_code)
