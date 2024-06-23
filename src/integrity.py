import os
import sys

import config

import constants.colours as colours
import constants.defaults as defaults
import constants.environment as environment
import constants.error as error

import helpers.colouring as colouring
import helpers.util as util


def main():
    # don't use argparse
    # it doesn't handle the concept of optionals well
    # just match on the number of command line arguments
    match len(sys.argv[1:]):
        case 0:
            check_all_configs()
        case 1:
            check_one_config(sys.argv[1])
        case _:
            pass
    pass


def check_all_configs():
    '''Check the integrity of all configs from the MVE_CONFIGS environment
    variable'''
    configs_folder = os.getenv(environment.CONFIGS)
    if configs_folder is None:
        coloured_env_key = colouring.colour_format(
            colours.RED, environment.CONFIGS, defaults.BOLD)
        util.print_error(
            f'the environment variable ${coloured_env_key} has not been set',
            defaults.BOLD)
        sys.exit(error.CONFIGS_ENVIRONMENT_NOT_SET)

    # TODO: modurlaise this
    configs = os.listdir(configs_folder)
    n = len(configs)
    print(
        'verifying the integrity of {} config{} in {}'.format(
            len(configs), util.plural(n), colouring.highlight(
                configs_folder, defaults.BOLD)
        )
    )
    for i, config in enumerate(configs):
        print(f'{i + 1}', end=' : ')
        check_one_config(config)


def check_one_config(name: str):
    state = config.Stateful(name)
    bold = state.cfg.bold
    util.print_success(
        f'the integrity of config \'{colouring.colour_format(
            colours.PURPLE, name, defaults.BOLD)}\' has been verified',
        bold)


if __name__ == '__main__':
    main()
