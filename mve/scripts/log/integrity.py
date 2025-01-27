import argparse
import os
import sys

from mve.src.config import Stateful

import mve.src.constants.colours as colours
import mve.src.constants.defaults as defaults
import mve.src.constants.environment as environment
import mve.src.constants.error as error
import mve.src.constants.status as status

import mve.src.helpers.colouring as colouring
import mve.src.helpers.files as files
import mve.src.helpers.load_env as load_env
import mve.src.helpers.util as util

from mve.scripts.script import LoggedScript
from mve.scripts.script_option import ScriptOption


class Integrity(LoggedScript):
    def __init__(self):
        super().__init__(str(ScriptOption.INTEGRITY))

    def main(self, argv: list[str]) -> None:
        args = self.handle_command_line_args(argv)
        config_names = args.config_names
        dirty = args.dirty

        configs_folder = self.handle_env_not_set()
        configs = config_names \
            if config_names \
            else self.list_configs_from_env(configs_folder)

        self.check_all_configs(configs_folder, configs, dirty)

    def handle_command_line_args(self, argv: list[str]) -> argparse.Namespace:
        parser = argparse.ArgumentParser(prog=self.generate_usage_name())

        parser.add_argument('config_names', nargs='*', type=str,
                            help='name of each config to verify')
        parser.add_argument('--dirty', action='store_true',
                            help='do not visualise each config\'s file structure')
        return parser.parse_args(argv)

    def handle_env_not_set(self) -> list[str]:
        configs_folder = load_env.get_config_paths_from_environment()
        if configs_folder is None:
            util.print_error(
                f'the environment variable {self.display_env_key()} has not been set',
                defaults.BOLD)
            sys.exit(error.CONFIGS_ENVIRONMENT_NOT_SET)

        return configs_folder

    def display_env_key(self) -> str:
        coloured_env_key = colouring.colour_format(
            colours.RED, environment.CONFIGS, defaults.BOLD)
        return f'${coloured_env_key}'

    def list_configs_from_env(self, configs_folder: list[str]) -> list[str]:
        print(f'loading all configs from {self.display_env_key()}')
        return sorted(
            files.ls(configs_folder)
        )

    def check_all_configs(self, config_paths: list[str], configs: list[str],
                          dirty: bool):
        n = len(configs)
        print(
            'verifying the integrity of {} config{}'.format(
                len(configs), util.plural(n)
            )
        )
        print(
            self.display_env_configs_banner(config_paths)
        )
        for i, config in enumerate(configs):
            print(f'--- config {i + 1} ---')
            self.check_one_config(config_paths, config, dirty)

    def display_env_configs_banner(self, configs_folder: list[str]) -> str:
        return '{} {}{}={}'.format(
            self.indicate(False), self.indent(
                status.TOP_LEVEL), self.display_env_key(),
            colouring.highlight_path(
                configs_folder, defaults.BOLD)
        )

    def check_one_config(self, config_paths: list[str], name: str, dirty: bool):
        state = Stateful(name)
        bold = state.cfg.bold
        if not dirty:
            print(
                self.visualise(config_paths, name)
            )
        util.print_success(
            'the integrity of config \'{}\' has been verified'.format(
                self.highlight_config(name)
            ), bold)

    def indent(self, depth: int) -> str:
        return depth * status.INDENT

    def visualise(self, config_paths: list[str], name: str) -> str:
        message = []

        def display_message():
            return '\n'.join(message)

        current_config = config_paths + [name]
        depth = status.TOP_LEVEL + 1

        if self.check_folder(message, current_config,
                             self.highlight_config(name), depth):
            return display_message()

        depth += 1
        for folder in Stateful.locate_folders(current_config):
            if self.check_folder(message, folder, folder[-1], depth):
                return display_message()

        for file in Stateful.locate_files(current_config):
            if self.check_file(message, file, os.path.basename(file), depth):
                return display_message()

        return display_message()

    def check_folder(self, message: list[str], paths: list[str], base: str,
                     depth: int) -> bool:
        '''Verify a given folder exists. Return whether it did not. Log its
        corresponding existence to the message.'''
        folder_non_existent = not files.do_folder_operation(
            paths, os.path.exists)
        message.append(
            '{} {}{}/'.format(self.indicate(folder_non_existent),
                              self.indent(depth), base)
        )
        return folder_non_existent

    def check_file(self, message: list[str], joined_path: str, base: str,
                   depth: int) -> bool:
        file_non_existent = not os.path.exists(joined_path)
        message.append(
            '{} {}+ {}'.format(self.indicate(file_non_existent),
                               self.indent(depth), base)
        )
        return file_non_existent

    def highlight_config(self, name: str):
        return colouring.colour_format(colours.PURPLE, name, defaults.BOLD)

    def indicate(self, fail: bool) -> str:
        status = self.indicate_fail() if fail else self.indicate_pass()
        return f'[{status}]'

    def indicate_pass(self) -> str:
        return colouring.colour_format(colours.GREEN, status.PASS,
                                       defaults.BOLD)

    def indicate_fail(self) -> str:
        return colouring.colour_format(colours.RED, status.FAIL,
                                       defaults.BOLD)
