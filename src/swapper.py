import json
import os
import sys

import constants.error as err
import constants.file_structure as fst

import helpers.check_and_exit_if as check_and_exit_if
import helpers.colours as colours
import helpers.files as files
import helpers.util as util


def main():
    check_and_exit_if.bad_args(sys.argv, 1, '[config name]')

    check_and_exit_if.no_folder(fst.CONFIGS, 'configs', err.NO_CONFIGS_FOLDER)

    config, = sys.argv[1:]
    config_paths = fst.CONFIGS + [config]
    check_and_exit_if.no_folder(config_paths, f"the '{config}' config", err.NO_CONFIG)


    current_cfg_file = os.path.join(*fst.CURRENT_CONFIG)
    check_and_exit_if.no_file(current_cfg_file, 'current config', err.NO_CURRENT_CONFIG)

    current = ''
    with open(current_cfg_file, 'r') as f:
        current = json.load(f)

    if config == current:
        warn = colours.warning()
        print(f"{warn} do you want to overwrite the existing config for {config}?")
        confirm = input(f"{warn} type 'y' if so : ")
        if confirm != 'y':
            sys.exit(0)

    remaining, cfg_file = [ files.get_joined_path(fst.CONFIGS + [config], file) for file in [fst.REMAINING, 'config.py'] ]

    print(remaining, cfg_file)

if __name__ == '__main__':
    main()
