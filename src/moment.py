from json import dumps
import sys

import constants.error as err
import constants.json_settings as jsn

import helpers.util as util

from treater import treat_all
from viewer import run_loop, wrap_session

def main():
    remaining, errors = gen_remaining(), []
    edits, renames, deletions = list(), dict(), list()
    run_loop(edits, renames, deletions)
    data = wrap_session(edits, renames, deletions)
    treat_all(data, remaining, errors)
    handle_errors(errors)
    util.exit_treat_all_good()


def gen_remaining():
    source = input("enter source folder : ")
    edits = input("enter ")


def handle_errors(errors):
    if errors:
        util.print_error(
            dumps(errors, indent=jsn.INDENT_SPACES)
        )
        sys.exit(err.TREATMENT_ERROR)
