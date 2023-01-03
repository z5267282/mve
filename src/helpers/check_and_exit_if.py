import os
import sys

import config as cfg

import constants.error as err
import constants.file_structure as fst

import helpers.files as files
import helpers.json_handlers as json_handlers
import helpers.util as util


# Command line args checking

def bad_args(argv):
    program_name, args = argv[0], argv[1:]
    if args:
        util.stderr_print(f'usage: python3 {os.path.basename(program_name)}')
        sys.exit(err.BAD_COMMAND_LINE_ARGS)


# Folder checking

def no_folder(folder_paths, folder_desc, exit_code):
    if not files.folder_exists(folder_paths):
        util.stderr_print(f"{folder_desc} folder '{folder_paths}' does not exist")
        sys.exit(exit_code)

def no_source_folder():
    no_folder(cfg.SOURCE, 'source', err.NO_SOURCE_FOLDER)

def no_queue():
    no_folder(fst.QUEUE, 'queue', err.NO_QUEUE)

def one_of_config_folders_missing():
    for folder, desc, code in zip(
        [cfg.SOURCE, cfg.RENAMES, cfg.DESTINATION],
        ['source', 'renames', 'destination'],
        [err.NO_SOURCE_FOLDER, err.NO_RENAMES_FOLDER, err.NO_DESTINATION_FOLDER]
    ):
        no_folder(folder, desc, code)


# Remaining related

def files_remaining():
    if json_handlers.load_remaining():
        util.stderr_print(f"there are files yet to be treated in '{fst.REMAINING}'")
        sys.exit(err.FILES_REMAINING)
