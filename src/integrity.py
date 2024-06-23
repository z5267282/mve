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

    check_all_configs(configs, dirty)


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


def check_all_configs(configs: list[str], dirty: bool):
    n = len(configs)
    print(
        'verifying the integrity of {} config{}'.format(
            len(configs), util.plural(n)
        )
    )
    for i, config in enumerate(configs):
        print(f'--- config {i + 1} ---')
        check_one_config(config, dirty)


def check_one_config(name: str, dirty: bool):
    state = config.Stateful(name)
    bold = state.cfg.bold
    if not dirty:
        print(
            visualise(name)
        )
    util.print_success(
        'the integrity of config \'{}\' has been verified'.format(
            colouring.colour_format(colours.PURPLE, name, defaults.BOLD)
        ),
        bold)


def visualise(name: str) -> str:
    def display_configs_folder(fail: bool) -> str: return '{} {}/'.format(
        indicate(fail), display_env_key()
    )
    # TODO: modularise the banner
    # TODO: expand the environment variable
    config_paths = load_env.get_config_paths_from_environment()
    if config_paths is None or not files.do_folder_operation(config_paths, os.path.exists):
        return display_configs_folder(True)

    message = [display_configs_folder(False)]
    def display_message(): return '\n'.join(message)

    current_config = config_paths + [name]

    # TODO: generalise the formatting based on file existence
    # TODO: paramaterise the depth
    def display_current_config(fail: bool) -> str: return '{}   {}/'.format(
        indicate(fail), name
    )
    current_non_existent = not files.do_folder_operation(
        current_config, os.path.exists)
    message.append(
        display_current_config(current_non_existent)
    )
    if current_non_existent:
        return display_message()

    def display_config_folder(base: str, fail: bool) -> str:
        return '{}     {}/'.format(indicate(fail), base)

    for folder in config.Stateful.locate_folders(current_config):
        folder_non_existent = not files.do_folder_operation(
            folder, os.path.exists)
        message.append(
            display_config_folder(folder[-1], folder_non_existent)
        )
        if folder_non_existent:
            return display_message()

    def display_config_file(base: str, fail: bool) -> str:
        return '{}     + {}'.format(indicate(fail), base)

    for file in config.Stateful.locate_files(current_config):
        file_non_existent = not os.path.exists(file)
        message.append(
            display_config_file(os.path.basename(file), file_non_existent)
        )
        if file_non_existent:
            return display_message()

    return display_message()


def indicate(fail: bool) -> str:
    status = indicate_fail() if fail else indicate_pass()
    return f'[{status}]'


def indicate_pass() -> str:
    return colouring.colour_format(colours.GREEN, status.PASS, defaults.BOLD)


def indicate_fail() -> str:
    return colouring.colour_format(colours.RED, status.FAIL, defaults.BOLD)


if __name__ == '__main__':
    main()
