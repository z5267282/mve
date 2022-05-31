import os
import re
import sys

import constants.cmd as cmd
import constants.err as err
import constants.fst as fst

import helpers.check_and_exit_if as check_and_exit_if
import helpers.util as util

def no_remaining():
    if not os.path.exists(fst.REMAINING):
        util.stderr_print(f"the remaining file '{fst.REMAINING}' doesn't exist")
        sys.exit(err.MISSING_REMAINING)

def run_checks():
    check_and_exit_if.bad_args(sys.argv)
    no_remaining()
    check_and_exit_if.no_source_folder()


def correct_name_format(name):
    return re.fullmatch(r'[a-zA-Z ]', name)

def log_edit(name, edit_name, times, edits):
    pass

def do_end(tokens, edits):
    if len(tokens) != 2:
        print('[e]nd | [ time ] [ name ]')
        return

    raw_time, edit_name = tokens
    time = None
    if re.fullmatch(r'[0-9]+', raw_time):
        time = raw_time
    elif re.fullmatch(r'[0-9]?[0-9]-[0-9]?[0-9]'):
        time = raw_time.replace('-', ':')

    if time is None:
        print('the time is in the form [ 1 integer | timestamp in form <min-sec>) ]')
        return

    if not correct_name_format(edit_name):
        print('the name can only contain upper and lowercase letters, digits and spacebars')
        return


def main():
    run_checks()

if __name__ == '__main__':
    main()
