import json
import os
import sys

import constants.file_structure as fst

import helpers.check_and_exit_if as check_and_exit_if
import helpers.files as files
import helpers.util as util


def main():
    check_and_exit_if.bad_args(sys.argv, 1, '[config name]')

    # TODO: make a code
    check_and_exit_if.no_folder(fst.CONFIGS, 'configs', 1)

    config, = sys.argv[1:]
    config_paths = fst.CONFIGS + [config]
    check_and_exit_if.no_folder(config_paths, f"the '{config}' config", 1)

    current = ''
    with open(fst.CURRENT_CONFIG, 'r') as f:
        current = json.load(f)

    if config == current:
        pass


if __name__ == '__main__':
    main()
