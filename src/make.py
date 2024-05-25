'''Make a new config folder. When prompted, enter absolute paths for the :
source, renames and destination paths. The config name must only contain [a-z-]
letters. The config is generated with default settings. A config will only
be made if one does not exist at present.'''

import pathlib
import re
import sys

import config

import constants.error as error

import helpers.args as args
import helpers.util as util


def main():
    name = args.expect_config_name(sys.argv)

    if not re.fullmatch(r"[a-z-]+", name):
        util.print_error("config must contain only a-z or - characters")
        sys.exit(error.BAD_CONFIG_NAME)


def make_config_contents() -> tuple[list[str], list[str], list[str]]:
    print("enter these folders")

    source = stringify_path("source")
    renames = stringify_path("renames")
    edits = stringify_path("destination")
    return source, renames, edits


def stringify_path(display: str) -> str:
    folder = input(f"{display}: ")
    return list(
        pathlib.Path(folder).parts
    )


if __name__ == "__main__":
    main()
