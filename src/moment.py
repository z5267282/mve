import json
import importlib 
import sys

import config as cfg

import constants.error as err
import constants.json_settings as jsn

import helpers.util as util

from treater import treat_all
from viewer import run_loop, wrap_session

def main():
    remaining, errors = gen_remaining(), []
    edits, renames, deletions = list(), dict(), list()
    run_loop(remaining, edits, renames, deletions)
    # data = wrap_session(edits, renames, deletions)
    # treat_all(data, remaining, errors)
    # handle_errors(errors)
    util.exit_treat_all_good()


def gen_remaining():
    print("enter absolute paths for the following folders")
    source = input("source : ")
    edits = input("edits : ")
    fix_config("test", "", "")
    return []

def fix_config(source, edits, renames):
    cfg.SOURCE = source
    cfg.DESTINATION = edits
    cfg.RENAMES = renames
    importlib.reload(cfg)


def handle_errors(errors):
    if errors:
        util.print_error(
            json.dumps(errors, indent=jsn.INDENT_SPACES)
        )
        sys.exit(err.TREATMENT_ERROR)


if __name__ == "__main__":
    main()
