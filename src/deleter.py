import os
import sys

import config as cfg

import helpers.check_and_exit_if as check_and_exit_if
import helpers.files as files

def run_checks():
    check_and_exit_if.bad_args(sys.argv)
    check_and_exit_if.files_remaining()
    check_and_exit_if.no_source_folder()

def main():
    run_checks()

    files.do_folder_operation(cfg.SOURCE, os.remove)

if __name__ == '__main__':
    main()
