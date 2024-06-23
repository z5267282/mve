'''Make a new config folder. Note that this script must be run on the host
machine to ensure the correct file path convention is used. When prompted,
enter absolute paths for the source, renames and destination paths. The config
name must only contain [a-z-] letters. The config is generated with default
settings. A config will only be made if one does not exist at present.'''

import os
import pathlib
import re
import sys

import config

import constants.error as error
import constants.defaults as defaults
import constants.version_control as version_control

import helpers.args as args
import helpers.colouring as colouring
import helpers.files as files
import helpers.json_handlers as json_handlers
import helpers.util as util


def main():
    name = args.expect_config_name(sys.argv)
    verify_name(name)

    configs_folder = config.Stateful.locate_configs_folder()
    new_config = configs_folder + [name]
    check_config_exists(new_config, name)
    make_config_folder(new_config)
    write_config_to_file(name)

    util.print_success(
        f'created config: {colouring.highlight(name, defaults.BOLD)}',
        defaults.BOLD)


def verify_name(name: str):
    if not re.fullmatch(r'[a-z0-9-]+', name):
        util.print_error(
            'config must contain only a-z, 0-9 or - characters', defaults.BOLD)
        sys.exit(error.BAD_CONFIG_NAME)


def make_config_contents() -> tuple[list[str], list[str], list[str]]:
    print('enter these folders')
    source = tokenise_path('source')
    renames = tokenise_path('renames')
    edits = tokenise_path('destination')
    return source, renames, edits


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


def write_config_to_file(name: str):
    for folder in config.Stateful.locate_folders(name):
        files.do_folder_operation(folder, os.mkdir)
        add_folder_to_version_history(folder)

    config_file, remaining = config.Stateful.locate_files(name)
    # write an empty list of remaining videos
    json_handlers.write_to_json(list(), remaining)
    source, renames, edits = make_config_contents()
    # the config will be created with default options
    cfg = config.Config(source, renames, edits)
    cfg.write_config_to_file(config_file)


def tokenise_path(display: str) -> list[str]:
    folder = input(f'{display}: ')
    return list(
        pathlib.Path(folder).parts
    )


if __name__ == '__main__':
    main()
