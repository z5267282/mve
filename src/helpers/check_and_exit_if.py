import os
import sys

import config as cfg

import constants.err as err
import constants.fst as fst

import helpers.files as files
import helpers.util as util

def stderr_print(message):
    print(message, file=sys.stderr)

def bad_args(argv):
    program_name, args = argv[0], argv[1:]
    if args:
        stderr_print(f'usage: python3 {os.path.basename(program_name)}')
        sys.exit(err.BAD_COMMAND_LINE_ARGS)


def no_folder(folder_paths, folder_desc, exit_code):
    if not files.folder_exists(folder_paths):
        stderr_print(f"{folder_desc} folder '{folder_paths}' does not exist")
        sys.exit(exit_code)

def no_source_folder():
    no_folder(cfg.SOURCE, 'source', err.NO_SOURCE_FOLDER)


def files_remaining():
    if util.read_from_json(fst.REMAINING):
        stderr_print(f"there are files yet to be treated in '{fst.REMAINING}'")
        sys.exit(err.FILES_REMAINING)
