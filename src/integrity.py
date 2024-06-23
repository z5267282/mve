import argparse
import os
import sys

import config

import constants.colours as colours
import constants.defaults as defaults
import constants.environment as environment
import constants.error as error
import constants.status as status

import helpers.colouring as colouring
import helpers.files as files
import helpers.load_env as load_env
import helpers.util as util


def main():
    args = handle_command_line_args()
    config_names = args.config_names
    dirty = args.dirty

    configs_folder = handle_env_not_set()
    configs = config_names \
        if config_names \
        else list_configs_from_env(configs_folder)

    check_all_configs(configs_folder, configs, dirty)


def handle_command_line_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('config_names', nargs='*', type=str,
                        help='name of each config to verify')
    parser.add_argument('--dirty', action='store_true',
                        help='do not visualise each config\'s file structure')
    return parser.parse_args()


def handle_env_not_set() -> list[str]:
    configs_folder = load_env.get_config_paths_from_environment()
    if configs_folder is None:
        util.print_error(
            f'the environment variable {display_env_key()} has not been set',
            defaults.BOLD)
        sys.exit(error.CONFIGS_ENVIRONMENT_NOT_SET)

    return configs_folder


def display_env_key() -> str:
    coloured_env_key = colouring.colour_format(
        colours.RED, environment.CONFIGS, defaults.BOLD)
    return f'${coloured_env_key}'


def list_configs_from_env(configs_folder: list[str]) -> list[str]:
    print(f'loading all configs from {display_env_key()}')
    return sorted(
        files.ls(configs_folder)
    )


def check_all_configs(config_paths: list[str], configs: list[str], dirty: bool):
    n = len(configs)
    print(
        'verifying the integrity of {} config{}'.format(
            len(configs), util.plural(n)
        )
    )
    print(
        display_env_configs_banner(config_paths)
    )
    for i, config in enumerate(configs):
        print(f'--- config {i + 1} ---')
        check_one_config(config_paths, config, dirty)


def display_env_configs_banner(configs_folder: list[str]) -> str:
    return '{} {}{}={}'.format(
        indicate(False), indent(0), display_env_key(), colouring.highlight_path(
            configs_folder, defaults.BOLD)
    )


def check_one_config(config_paths: list[str], name: str, dirty: bool):
    state = config.Stateful(name)
    bold = state.cfg.bold
    if not dirty:
        print(
            visualise(config_paths, name)
        )
    util.print_success(
        'the integrity of config \'{}\' has been verified'.format(
            colouring.colour_format(colours.PURPLE, name, defaults.BOLD)
        ),
        bold)


def indent(depth: int) -> str:
    return depth * status.INDENT


def visualise(config_paths: list[str], name: str) -> str:
    message = []
    def display_message(): return '\n'.join(message)

    current_config = config_paths + [name]

    if check_folder(message, current_config, name, 1):
        return display_message()

    for folder in config.Stateful.locate_folders(current_config):
        if check_folder(message, folder, folder[-1], 2):
            return display_message()

    for file in config.Stateful.locate_files(current_config):
        if check_file(message, file, os.path.basename(file), 2):
            return display_message()

    return display_message()


def check_folder(message: list[str], paths: list[str], base: str,
                 depth: int) -> bool:
    '''Verify a given folder exists. Return whether it did not. Log its
    corresponding existence to the message.'''
    folder_non_existent = not files.do_folder_operation(
        paths, os.path.exists)
    message.append(
        '{} {}{}/'.format(indicate(folder_non_existent), indent(depth), base)
    )
    return folder_non_existent


def check_file(message: list[str], joined_path: str, base: str,
               depth: int) -> bool:
    file_non_existent = not os.path.exists(joined_path)
    message.append(
        '{} {}+ {}'.format(indicate(file_non_existent), indent(depth), base)
    )
    return file_non_existent


def indicate(fail: bool) -> str:
    status = indicate_fail() if fail else indicate_pass()
    return f'[{status}]'


def indicate_pass() -> str:
    return colouring.colour_format(colours.GREEN, status.PASS, defaults.BOLD)


def indicate_fail() -> str:
    return colouring.colour_format(colours.RED, status.FAIL, defaults.BOLD)


if __name__ == '__main__':
    main()
