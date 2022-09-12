import shutil
import sys

import config as cfg

import helpers.check_and_exit_if as check_and_exit_if
import helpers.colours as colours
import helpers.files as files
import helpers.util as util


def main():
    run_checks()

    files.do_folder_operation(cfg.SOURCE, shutil.rmtree)

    joined_path = files.get_joined_path(cfg.SOURCE, '')
    util.exit_success(f"removed the folder '{colours.highlight(joined_path)}'")


def run_checks():
    check_and_exit_if.bad_args(sys.argv)
    check_and_exit_if.files_remaining()
    check_and_exit_if.no_source_folder()


if __name__ == '__main__':
    main()
