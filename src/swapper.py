import json
import os
import sys
import tempfile

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
    
    new_d, cwd = [
        get_dir_fd(dir_paths) for dir_paths in [
            new_paths, ['.']
        ]
    ]

    old_d = None if old == new else get_dir_fd(
        get_cfg_paths(old)
    )

    with tempfile.TemporaryDirectory() as t:
        tmp_d = open_folder(t)
        
        move_pair(cwd, tmp_d)
        move_pair(new_d, cwd)

        real_old_d = new_d if old_d is None else old_d
        move_pair(tmp_d, real_old_d)

        os.close(tmp_d)
    
    for dir in [new_d, cwd]:
        os.close(dir)

    if not old is None:
        os.close(old_d)
    

def get_cfg_paths(title):
    return fst.CONFIGS + [title]

def open_folder(path):
    return os.open(path, os.O_RDONLY)

def get_dir_fd(dir_paths):
    return open_folder(
        files.join_folder(dir_paths),
    )


def move_pair(src_fd, dst_fd):
    for item in [fst.REMAINING, fst.CONFIG]:
        os.rename(item, item, src_dir_fd=src_fd, dst_dir_fd=dst_fd)


if __name__ == '__main__':
    main()
