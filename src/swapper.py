import json
import os
import sys

import constants.error as err
import constants.file_structure as fst

import helpers.check_and_exit_if as check_and_exit_if
import helpers.files as files


def main():
    check_and_exit_if.bad_args(sys.argv, 1, '[config name]')

    check_and_exit_if.no_folder(fst.CONFIGS, 'configs', err.NO_CONFIGS_FOLDER)

    new, = sys.argv[1:]
    config_paths = fst.CONFIGS + [new]
    check_and_exit_if.no_folder(config_paths, f"the '{new}' config", err.NO_CONFIG)

    old_cfg_file = os.path.join(*fst.CURRENT_CONFIG)
    check_and_exit_if.no_file(old_cfg_file, 'current config', err.NO_CURRENT_CONFIG)
    old = ''
    with open(old_cfg_file, 'r') as f:
        old = json.load(f)
    
    with 

    new_rem, new_cfg = [ files.get_joined_path(fst.CONFIGS + [new], file) for file in [fst.REMAINING, fst.CONFIG] ]
    old_rem, old_cfg = fst.REMAINING, 


if __name__ == '__main__':
    main()
