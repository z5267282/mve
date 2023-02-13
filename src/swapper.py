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
    new_paths = get_cfg_paths(new)
    check_and_exit_if.no_folder(new_paths, f"the '{new}' config", err.NO_CONFIG)

    old_cfg_file = files.get_joined_path(fst.CONFIGS, fst.CURRENT_CONFIG)
    check_and_exit_if.no_file(old_cfg_file, 'current config', err.NO_CURRENT_CONFIG)
    old = ''
    with open(old_cfg_file, 'r') as f:
        old = json.load(f)
        old_paths = get_cfg_paths(old)
    
    new_dir, old_dir, cfg_dir, src_dir = [ files.join_folder(dir_paths) for dir_paths in [
        new_paths, old_paths, fst.CONFIGS, ['.']
        ]
    ]
    with \
        os.open(new_dir, os.O_RDWR) as nd, \
        os.open(old_dir, os.O_RDWR) as od, \
        os.open(cfg_dir, os.O_RDWR) as cd, \
        os.open(src_dir, os.O_RDWR) as sd:

        print(nd)
    

def get_cfg_paths(title):
    return fst.CONFIGS + [title]

if __name__ == '__main__':
    main()
