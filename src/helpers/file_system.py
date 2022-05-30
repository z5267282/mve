import os
import sys

import constants.error_numbers as error_numbers
import config as cfg

def get_joined_path(paths_list, file_name):
    paths = paths_list + [file_name]
    return os.path.join(*paths)

def do_folder_operation(paths_list, handler):
    path = os.path.join(*paths_list)
    return handler(path)

def ls(paths_list):
    return do_folder_operation(paths_list, os.listdir)

def folder_exists(paths_list):
    return do_folder_operation(paths_list, os.path.exists)

def no_folder_handler(paths_list, message, code):
    if not folder_exists(paths_list):
        print(message, file=stderr)
        sys.exit(code)

def check_no_source_folder():
    no_folder_handler(
        cfg.SOURCE,
        f"the source folder '{cfg.SOURCE} didn't exist"
        error_numbers.NO_SOURCE_FOLDER
    )
