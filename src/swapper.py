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
    old_paths = get_cfg_paths(old)

    check_config_files(new_paths)

    swap_files(new_paths, old_paths)

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
    
    with open(old_cfg_file, 'r') as f:
        old = json.load(f)
    return old, old_cfg_file


def check_config_files(new_paths):
    for paths_list in [
        new_paths, ['.']
    ]:
        check_config_pair(paths_list)

def check_config_pair(paths_list):
    for item, desc, code in zip(
        [fst.CONFIG, fst.REMAINING],
        ['config', 'remaining'],
        [err.NO_CONFIG_CONF_FILE, err.NO_CONFIG_REMAINING]
    ):
        joined_path = files.get_joined_path(paths_list, item)
        check_and_exit_if.no_file(joined_path, desc, code)
    

def swap_files(new_paths, old_paths):
    """
        cur -> tmp
        new -> cur
        tmp -> cur
    """

    new_dir, old_dir = [
        os.path.join(*paths_list) for paths_list in
            [new_paths, old_paths]
    ]

    with tempfile.TemporaryDirectory() as t:
        move_pair('.', t)
        move_pair(new_dir, '.')
        move_pair(t, old_dir)
    
def move_pair(src, dst):
    for item in [fst.CONFIG, fst.REMAINING]:
        os.rename(
            os.path.join(src, item),
            os.path.join(dst, item)
        )


if __name__ == '__main__':
    main()
