import json
import sys

import constants.error as err
import constants.file_structure as fst

import helpers.check_and_exit_if as check_and_exit_if
import helpers.files as files


def main():
    check_and_exit_if.no_args(sys.argv)

    current_path = handle_current_path()
    print_current(current_path)


def handle_current_path():
    current_path = files.get_joined_path(fst.CONFIGS, fst.CURRENT_CONFIG)
    check_and_exit_if.no_file(current_path, 'current config', err.NO_CURRENT_CONFIG)
    return current_path


def print_current(current_path):
    with open(current_path, 'r') as f:
        current = json.load(f)
        print(f"currently in use: '{current}'")


if __name__ == '__main__':
    main()
