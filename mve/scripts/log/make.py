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

from mve.src.config import Config, Stateful

import mve.src.constants.error as error
import mve.src.constants.defaults as defaults
import mve.src.constants.version_control as version_control

import mve.src.helpers.colouring as colouring
import mve.src.helpers.files as files
import mve.src.helpers.json_handlers as json_handlers
import mve.src.helpers.util as util
from mve.src.helpers.video_paths import VideoPaths

from mve.scripts.script import Script
from mve.scripts.script_option import ScriptOption


class Make(Script):
    '''Create a new stateful configuration from the command line.'''

    def __init__(self):
        super().__init__(str(ScriptOption.MAKE))

    def main(self, argv: list[str]) -> None:
        args = self.handle_args(argv)
        name = args.config
        self.verify_name(name)

        configs_folder = Stateful.locate_configs_folder()
        new_config = configs_folder + [name]
        self.check_config_exists(new_config, name)
        self.make_config_folder(new_config)
        opts = self.make_config_options_from_flags(args)
        self.write_config_to_file(
            new_config, args.source, args.edits, args.renames, opts)

        util.print_success(
            f'created config: {colouring.highlight(name, defaults.BOLD)}',
            defaults.BOLD)

    def handle_args(self, argv: list[str]) -> argparse.Namespace:
        parser = argparse.ArgumentParser()
        parser.add_argument('config', type=str)

        # path flags
        parser.add_argument('--source', type=str)
        parser.add_argument('--renames', type=str)
        parser.add_argument('--edits', type=str)

        self.handle_options(parser)

        return parser.parse_args(argv)

    def handle_options(self, parser: argparse.ArgumentParser) -> None:
        '''Note that all flags will be converted into snake_case by
        argparse.'''

        # file-order generation
        parser.add_argument('--recent', action='store_true',
                            default=defaults.RECENT)

        # multiprocessing
        parser.add_argument('--num-processes', type=int,
                            default=defaults.NUM_PROCESSES)

        # moviepy
        parser.add_argument('--use-moviepy', action='store_true',
                            default=defaults.USE_MOVIEPY)
        parser.add_argument('--moviepy-threads', type=int,
                            default=defaults.MOVIEPY_THREADS)

        # testing
        parser.add_argument('--testing', action='store_true',
                            default=defaults.TESTING)

        # colours
        parser.add_argument('--bold', action='store_true',
                            default=defaults.BOLD)

        # double-check name was not mistaken for a command
        parser.add_argument('--verify-name', action='store_true',
                            default=defaults.VERIFY_NAME)

    def make_config_options_from_flags(self,
                                       arguments: argparse.Namespace) -> dict:
        name = {'config'}
        folders = {'source', 'renames', 'edits'}
        unwanted = folders | name
        # converting namespace into dict is supported in pydocs:
        # https://docs.python.org/3/library/argparse.html#the-namespace-object
        return {k: v for k, v in vars(arguments).items() if not k in unwanted}

    def verify_name(self, name: str):
        if not re.fullmatch(r'[a-z0-9-]+', name):
            util.print_error(
                'config must contain only a-z, 0-9 or - characters',
                defaults.BOLD)
            sys.exit(error.BAD_CONFIG_NAME)

    def check_config_exists(self, new_config: list[str], name: str):
        if files.folder_exists(new_config):
            util.print_error(
                f'the config \'{name}\' already exists', defaults.BOLD)
            sys.exit(error.EXISTING_CONFIG)

    def make_config_folder(self, new_config: list[str]):
        files.do_folder_operation(new_config, os.mkdir)

    def add_folder_to_version_history(self, config_folder: list[str]):
        with open(
                files.get_joined_path(
                    config_folder, version_control.KEEP_FILE),
                'w') as _:
            pass

    def write_config_to_file(self, new_config: list[str], source: None | str,
                             edits: None | str, renames: None | str,
                             opts: dict):
        for folder in Stateful.locate_folders(new_config):
            files.do_folder_operation(folder, os.mkdir)
            self.add_folder_to_version_history(folder)

        config_file, remaining = Stateful.locate_files(new_config)
        # write an empty list of remaining videos
        json_handlers.write_to_json(list(), remaining)
        folders = VideoPaths.make_all_paths_from_defaults(source,
                                                          edits,
                                                          renames)
        # the config will be created with default options
        cfg = Config(folders, **opts)
        cfg.write_config_to_file(config_file)
