'''Make a new config folder. Note that this script must be run on the host
machine to ensure the correct file path convention is used. When prompted,
enter absolute paths for the source, renames and destination paths.
Paths can be provided on the command line to allow for Shell expansions. The
config name must only contain [a-z-] letters. The config is generated with
default settings. A config will only be made if one does not exist at
present.'''

import argparse
import os
import re
import sys

import config

import constants.error as error
import constants.defaults as defaults
import constants.version_control as version_control

import helpers.colouring as colouring
import helpers.files as files
import helpers.json_handlers as json_handlers
import helpers.util as util
import helpers.video_paths as video_paths


def main():
    args = handle_args()
    name = args.config
    verify_name(name)

    configs_folder = config.Stateful.locate_configs_folder()
    new_config = configs_folder + [name]
    check_config_exists(new_config, name)
    make_config_folder(new_config)
    write_config_to_file(new_config, args.source, args.edits, args.renames)

    util.print_success(
        f'created config: {colouring.highlight(name, defaults.BOLD)}',
        defaults.BOLD)


def handle_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('config', type=str)
    # path flags
    parser.add_argument('--source', type=str)
    parser.add_argument('--renames', type=str)
    parser.add_argument('--edits', type=str)
    return parser.parse_args()


def verify_name(name: str):
    if not re.fullmatch(r'[a-z0-9-]+', name):
        util.print_error(
            'config must contain only a-z, 0-9 or - characters', defaults.BOLD)
        sys.exit(error.BAD_CONFIG_NAME)


def check_config_exists(new_config: list[str], name: str):
    if files.folder_exists(new_config):
        util.print_error(
            f'the config \'{name}\' already exists', defaults.BOLD)
        sys.exit(error.EXISTING_CONFIG)


def make_config_folder(new_config: list[str]):
    files.do_folder_operation(new_config, os.mkdir)


def add_folder_to_version_history(config_folder: list[str]):
    with open(
            files.get_joined_path(config_folder, version_control.KEEP_FILE),
            'w') as _:
        pass


def write_config_to_file(new_config: list[str], source: None | str,
                         edits: None | str, renames: None | str):
    for folder in config.Stateful.locate_folders(new_config):
        files.do_folder_operation(folder, os.mkdir)
        add_folder_to_version_history(folder)

    config_file, remaining = config.Stateful.locate_files(new_config)
    # write an empty list of remaining videos
    json_handlers.write_to_json(list(), remaining)
    videos = video_paths.VideoPaths.make_all_paths_from_defaults(source, edits,
                                                                 renames)
    # the config will be created with default options
    cfg = config.Config(videos.source, videos.renames, videos.edits)
    cfg.write_config_to_file(config_file)


if __name__ == '__main__':
    main()
