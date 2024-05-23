import shutil
import sys

import config

import helpers.check_and_exit_if as check_and_exit_if
import helpers.colours as colours
import helpers.files as files
import helpers.util as util


def main():
    run_checks()

    TODO_FIX = "mac"
    cfg = config.Config(TODO_FIX)

    files.do_folder_operation(cfg.source, shutil.rmtree)

    joined_path = files.join_folder(cfg.source)
    util.exit_success(f"removed the folder '{colours.highlight(joined_path)}'")


def run_checks():
    check_and_exit_if.no_args(sys.argv)
    check_and_exit_if.files_remaining()
    check_and_exit_if.no_source_folder()


if __name__ == '__main__':
    main()
