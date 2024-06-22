import sys

import config

import helpers.colouring as colouring
import helpers.util as util


def main():
    # don't use argparse
    # it doesn't handle the concept of optionals well
    # just match on the number of command line arguments
    match len(sys.argv[1:]):
        case 0:
            pass
        case 1:
            check_one_config(sys.argv[1])
        case _:
            pass

    pass


def check_one_config(name: str):
    state = config.Stateful(name)
    bold = state.cfg.bold
    util.print_success(
        f'the integrity of config \'{colouring.highlight(name, bold)}\' has been verified',
        bold)


if __name__ == '__main__':
    main()
