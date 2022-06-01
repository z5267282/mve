import os
import re
import sys

import config as cfg

import constants.commands as cmd
import constants.error as err
import constants.file_structure as fst
import constants.treatment_format as trf

import helpers.check_and_exit_if as check_and_exit_if
import helpers.files as files
import helpers.util as util

def no_remaining():
    if not os.path.exists(fst.REMAINING):
        util.stderr_print(f"the remaining file '{fst.REMAINING}' doesn't exist")
        sys.exit(err.MISSING_REMAINING)

def run_checks():
    check_and_exit_if.bad_args(sys.argv)
    no_remaining()
    check_and_exit_if.no_source_folder()


def print_time_format(name, form):
    print(f'the {name} time must be in the form {form}')

def parse_timestamp(timestamp):
    return timestamp.replace('-', ':') if re.fullmatch(r'[0-9]?[0-9]-[0-9]?[0-9]', timestamp) else None

def print_name_format():
    print('the name can only contain upper and lowercase letters, digits and spacebars')

def correct_name_format(name):
    return re.fullmatch(r'[a-zA-Z ]', name)

def bad_name_format(name):
    if not correct_name_format(name):
        print_name_format()
        return True

    return False


def tokenise(raw_tokens, splits):
    return raw_tokens.split(' ', splits)

def parse_tokens(raw_tokens, command):
    n_tokens = cmd.NUM_TOKENS[command]
    tokens = tokenise(raw_tokens, n_tokens - 1)
    return tokens if len(tokens) == tokens else []


def log_edit(name, edit_name, times, edits):
    edits[name] = {
        trf.EDIT_NAME  : edit_name,
        trf.EDIT_TIMES : times
    }

def do_end(name, raw_tokens, edits):
    tokens = parse_tokens(raw_tokens, cmd.END)
    if not tokens:
        print('[e]nd | [ time ] [ name ]')
        return

    raw_time, edit_name = tokens
    time = None
    if re.fullmatch(r'-?[0-9]+', raw_time):
        time = raw_time
    else:
        time = parse_timestamp(raw_time)
    if time is None:
        print_time_format('', '[ integer | timestamp in form <min-sec>) ]')
        return

    if bad_name_format(edit_name):
        return

    log_edit(name, edit_name, [time], edits)

def do_middle(name, raw_tokens, edits):
    tokens = parse_tokens(raw_tokens, cmd.MIDDLE)
    if not tokens:
        print('[m]iddle | [ start ] [ end ] [ name ]')
        return

    start, end, edit_name = tokens
    times = []
    for value, description in enumerate([start, end], ['start', 'end']):
        if re.fullmatch(r'[0-9]+', value):
            times.append(value)
            continue

        time = parse_timestamp(value)
        if time is None:
            print_time_format(description, '[ natural number | timestamp in form <min-sec>) ]')
            return

        times.append(time)
    
    if bad_name_format(edit_name):
        return

    log_edit(name, edit_name, times, edits)

def log_rename(name, new_name, renames):
    renames[name] = new_name

def do_rename(name, raw_tokens, renames):
    tokens = parse_tokens(raw_tokens, cmd.RENAME)
    if not tokens:
        print('[r]ename | [ name ]')
        return
    
    new_name, = tokens
    if bad_name_format(new_name):
        return
    
    log_rename(name, new_name, renames)

def log_delete(name, deletions):
    deletions.append(name)

def view_video(name):
    joined_path = files.get_joined_path(cfg.SOURCE, name)
    # TODO: load video
    print(joined_path)

def run_loop(remaining, edits, renames, deletions):
    while remaining:
        name = remaining[0]
        view_video(name)

        args = input(f'{name}: ')
        command = args.split(' ', 1)
        match command:
            case cmd.QUIT:
                break
            case cmd.CONTINUE:
                remaining.insert(0, name)
                break
            case cmd.HELP:
                print(cmd.MESSAGE)
                break
            


def log_to_file():
    pass


def main():
    run_checks()

    run_loop()
    log_to_file()

if __name__ == '__main__':
    main()
