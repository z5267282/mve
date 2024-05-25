'''Make a new config folder. When prompted, enter absolute paths for the :
source, renames and destination paths. The config name must only contain [a-z-]
letters. The config is generated with default settings. A config will only
be made if one does not exist at present.'''

import os
import pathlib
import re
import sys

import config

import constants.error as error

import helpers.args as args
import helpers.files as files
import helpers.json_handlers as json_handlers
import helpers.util as util


def main():
    name = args.expect_config_name(sys.argv)

    # verify name
    if not re.fullmatch(r'[a-z-]+', name):
        util.print_error('config must contain only a-z or - characters')
        sys.exit(error.BAD_CONFIG_NAME)

    # ensure non-existent
    configs_folder = config.Stateful.locate_configs_folder()
    new_config = configs_folder + [name]
    if files.folder_exists(new_config):
        util.print_error(f'the config \'{name}\' already exists')
        sys.exit(error.EXISTING_CONFIG)

    # create config folder structure
    files.do_folder_operation(configs_folder, os.mkdir)

    for folder in config.Stateful.locate_folders():
        files.do_folder_operation(new_config, os.mkdir)

    config_file, remaining = config.Stateful.locate_files()
    # write an empty list of remaining videos
    json_handlers.write_to_json(list(), remaining)
    # create a config with default options
    cfg = config.Config()
    cfg.write_config_to_file(config_file)


def make_config_contents() -> tuple[list[str], list[str], list[str]]:
    print('enter these folders')
    source = stringify_path('source')
    renames = stringify_path('renames')
    edits = stringify_path('destination')
    return source, renames, edits


def stringify_path(display: str) -> str:
    folder = input(f'{display}: ')
    return list(
        pathlib.Path(folder).parts
    )


if __name__ == '__main__':
    main()
