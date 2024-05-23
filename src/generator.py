import os
import sys

import config

import constants.file_structure as fst

import helpers.check_and_exit_if as check_and_exit_if
import helpers.colours as colours
import helpers.json_handlers as json_handlers
import helpers.files as files
import helpers.util as util


def main():
    run_checks()

    TODO_FIX_0 = "mac"
    cfg = config.Stateful(TODO_FIX_0)

    TODO_FIX = True

    new_files = files.ls(cfg.source, TODO_FIX)
    json_handlers.write_to_json(new_files, fst.REMAINING)

    joined_path = files.join_folder(cfg.source)
    util.exit_success(
        f"placed file names from the folder '{colours.highlight(joined_path)}' in {fst.REMAINING}")


def run_checks():
    check_and_exit_if.no_args(sys.argv)
    check_and_exit_if.no_source_folder()
    if os.path.exists(fst.REMAINING):
        check_and_exit_if.files_remaining()


if __name__ == '__main__':
    main()
