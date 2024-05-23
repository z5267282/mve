import os
import sys

import config

import constants.file_structure as fst

import helpers.check_and_exit_if as check_and_exit_if
import helpers.colours as colours
import helpers.files as files
import helpers.util as util


def main():
    run_checks()

    TODO_FIX_0 = "mac"
    cfg = config.Stateful(TODO_FIX_0)

    TODO_FIX = True

    new_files = files.ls(cfg.source, TODO_FIX)
    cfg.write_remaining(new_files)

    joined_path = files.join_folder(cfg.source)
    util.exit_success(
        f"placed file names from the folder '{colours.highlight(joined_path)}' in {fst.REMAINING}")


def run_checks(cfg: config.Stateful):
    check_and_exit_if.no_args(sys.argv)
    cfg.no_source_folder()
    cfg.check_files_remaining()


if __name__ == '__main__':
    main()
