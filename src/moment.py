from json import dumps
import os
import sys

import constants.error as err
import constants.json_settings as jsn

import helpers.files as files
import helpers.paths as paths
import helpers.util as util

from treater import treat_all
from viewer import run_loop, wrap_session

def main():
    paths = gen_paths()
    # TODO : MAKE INTO FLAG
    remaining, errors = gen_remaining(paths, False), []
    edits, renames, deletions = list(), dict(), list()
    run_loop(edits, renames, deletions, paths)
    data = wrap_session(edits, renames, deletions)
    treat_all(data, remaining, errors)
    handle_errors(errors)
    util.exit_treat_all_good()


def gen_paths() -> paths.Paths:
    source = input("enter source folder : ")
    edits = input("enter ")
    return paths.Paths(
        decompose_path_into_folders(source),
        decompose_path_into_folders(edits),
        decompose_path_into_folders(edits)
    )


def gen_remaining(paths : paths.Paths, recent : bool) -> list[str]:
    return files.ls(paths.source, recent=recent)


def decompose_path_into_folders(abs_path : str) -> list[str]:
    normalised = os.path.normpath(abs_path)
    return normalised.split(os.path.sep)


def handle_errors(errors):
    if errors:
        util.print_error(
            dumps(errors, indent=jsn.INDENT_SPACES)
        )
        sys.exit(err.TREATMENT_ERROR)


if __name__ == "__main__":
    main()
