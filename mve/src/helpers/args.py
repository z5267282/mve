'''For handling command line arguments'''

import mve.src.helpers.check_and_exit_if as check_and_exit_if


def expect_config_name(argv: list[str]) -> str:
    check_and_exit_if.bad_args(argv, 1, '<config>')

    name, = argv[1:]
    return name
