import json
import os
import sys
import tempfile

import constants.error as err
import constants.file_structure as fst

import helpers.check_and_exit_if as check_and_exit_if
import helpers.files as files
import helpers.json_handlers as json_handlers


def main():
    run_backgound_checks()

    new, = sys.argv[1:]
    new_paths = handle_new_config_paths(new)

    old, old_cfg_file = handle_current_config()
    new_d, old_d, cwd = handle_folder_descriptors(new, new_paths, old)

    swap_files(new_d, old_d, cwd)
    close_folders(new_d, old_d, cwd)

    json_handlers.write_to_json(new, old_cfg_file)


def run_backgound_checks():
    check_and_exit_if.bad_args(sys.argv, 1, '[config name]')
    check_and_exit_if.no_folder(fst.CONFIGS, 'configs', err.NO_CONFIGS_FOLDER)


def handle_new_config_paths(new):
    new_paths = get_cfg_paths(new)
    check_and_exit_if.no_folder(new_paths, f"the '{new}' config", err.NO_CONFIG)
    return new_paths

def get_cfg_paths(title):
    return fst.CONFIGS + [title]


def handle_current_config():
    old_cfg_file = files.get_joined_path(fst.CONFIGS, fst.CURRENT_CONFIG)
    check_and_exit_if.no_file(old_cfg_file, 'current config', err.NO_CURRENT_CONFIG)
    
    old = ''
    with open(old_cfg_file, 'r') as f:
        old = json.load(f)
    return old, old_cfg_file


def handle_folder_descriptors(new, new_paths, old):
    paths_lists = [
        new_paths, ['.']
    ]
    for paths_list in paths_lists:
        check_config_pair(paths_list)

    new_d, cwd = [get_dir_fd(dir_paths) for dir_paths in paths_lists]
    old_d = None if old == new else get_dir_fd(
        get_cfg_paths(old)
    )
    return new_d, old_d, cwd

def check_config_pair(paths_list):
    for item, desc, code in zip(
        [fst.CONFIG, fst.REMAINING],
        ['config', 'remaining'],
        [err.NO_CONFIG_CONF_FILE, err.NO_CONFIG_REMAINING]
    ):
        joined_path = files.get_joined_path(paths_list, item)
        check_and_exit_if.no_file(joined_path, desc, code)
    
def get_dir_fd(dir_paths):
    return open_folder(
        files.join_folder(dir_paths),
    )

def open_folder(path):
    # return os.open(path, os.O_RDONLY)
    return os.open(path, 0x2000)


def swap_files(new_d, old_d, cwd):
    with tempfile.TemporaryDirectory() as t:
        tmp_d = open_folder(t)
        
        move_pair(cwd, tmp_d)
        move_pair(new_d, cwd)

        real_old_d = new_d if old_d is None else old_d
        move_pair(tmp_d, real_old_d)

        close_folder(tmp_d)
    
def move_pair(src_fd, dst_fd):
    for item in [fst.CONFIG, fst.REMAINING]:
        os.rename(item, item, src_dir_fd=src_fd, dst_dir_fd=dst_fd)

def close_folder(dir_fd):
    os.close(dir_fd)
    

def close_folders(new_d, old_d, cwd):
    for dir in [new_d, cwd]:
        close_folder(dir)

    if not old_d is None:
        close_folder(old_d)


if __name__ == '__main__':
    main()
