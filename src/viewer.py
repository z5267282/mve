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
    return timestamp.replace('-', ':') if re.fullmatch(r'([0-9]?[0-9]-)?[0-9]?[0-9]-[0-9]?[0-9]', timestamp) else None

def print_name_format():
    print('the name can only contain upper and lowercase letters, digits and spacebars')

def correct_name_format(name):
    return re.fullmatch(r'[a-zA-Z0-9 ]+', name)

def bad_name_format(name):
    if not correct_name_format(name):
        print_name_format()
        return True

    return False


def do_continue(remaining, name):
    remaining.insert(0, name)

def do_help():
    print(cmd.MESSAGE)


def tokenise(raw_tokens, splits):
    return raw_tokens.split(' ', splits)

def parse_tokens(raw_tokens, command):
    n_tokens = cmd.NUM_TOKENS[command]
    tokens = tokenise(raw_tokens, n_tokens - 1)
    return tokens if len(tokens) == n_tokens else []


def log_edit(name, edit_name, times, edits):
    new_edit = {
        trf.EDIT_ORIGINAL : name,
        trf.EDIT_NAME     : edit_name,
        trf.EDIT_TIMES    : times
    }
    edits.append(new_edit)

def reprompt_name(current_name):
    print(f"the name '{current_name}' starts with a number are you sure you haven't misentered the [m]iddle command?")
    change_name = input("type 'y' if you want to re-enter this command : ")
    return None if change_name == 'y' else current_name

def do_end(name, raw_tokens, edits):
    tokens = parse_tokens(raw_tokens, cmd.END)
    if not tokens:
        print('[e]nd | [ time ] [ name ]')
        return False

    raw_time, edit_name = tokens
    time = None
    if re.fullmatch(r'-?[0-9]+', raw_time):
        time = raw_time
    else:
        time = parse_timestamp(raw_time)

    if time is None:
        print_time_format('', '[ integer | timestamp in form <[hour]-min-sec> ]')
        return False 

    if bad_name_format(edit_name):
        return False
    
    if re.match(r'[0-9]+', edit_name):
        edit_name = reprompt_name(edit_name)

    if edit_name is None:
        return False

    log_edit(name, edit_name, [time], edits)
    return True

def do_middle(name, raw_tokens, edits):
    tokens = parse_tokens(raw_tokens, cmd.MIDDLE)
    if not tokens:
        print('[m]iddle | [ start ] [ end ] [ name ]')
        return False

    start, end, edit_name = tokens
    times = []
    for value, description in zip([start, end], ['start', 'end']):
        if re.fullmatch(r'[0-9]+', value):
            times.append(value)
            continue 

        time = parse_timestamp(value)
        if time is None:
            print_time_format(description, '[ natural number | timestamp in form <[hour]-min-sec> ]')
            return False

        times.append(time)
    
    if bad_name_format(edit_name):
        return False

    log_edit(name, edit_name, times, edits)
    return True

def log_rename(name, new_name, renames):
    renames[name] = new_name

def do_rename(name, raw_tokens, renames):
    tokens = parse_tokens(raw_tokens, cmd.RENAME)
    if not tokens:
        print('[r]ename | [ name ]')
        return False
    
    new_name, = tokens
    if bad_name_format(new_name):
        return False
    
    log_rename(name, new_name, renames)
    return True

def log_delete(name, deletions):
    deletions.append(name)

def do_delete(name, deletions):
    log_delete(name, deletions)
    return True

def view_video(name):
    joined_path = files.get_joined_path(cfg.SOURCE, name)
    os.startfile(joined_path)

def prompt(name, padding, number_remaining):
    args = input(f'{number_remaining:>{padding}} - {name} : ').split(' ', 1)
    command = args[0]
    raw_tokens = args[1] if len(args) == 2 else str()
    return command, raw_tokens

def run_loop(edits, renames, deletions):
    remaining = util.load_remaining()
    padding = len(
        str(
            len(remaining)
        )
    )

    while remaining:
        name = remaining[0]
        view_video(name)
        
        go_to_next_file = False
        command, raw_tokens = prompt(name, padding, len(remaining))
        match command:
            case cmd.QUIT:
                break
            case cmd.CONTINUE:
                do_continue(remaining, name)
            case cmd.HELP:
                do_help()
            case cmd.END:
                go_to_next_file = do_end(name, raw_tokens, edits)
            case cmd.MIDDLE:
                go_to_next_file = do_middle(name, raw_tokens, edits)
            case cmd.RENAME:
                go_to_next_file = do_rename(name, raw_tokens, renames)
            case cmd.DELETE:
                go_to_next_file = do_delete(name, deletions)
            case _:
                print(f"invalid command '{command}' - press {cmd.HELP} for a list of commands")

        if go_to_next_file:
            remaining.pop(0)
    
    util.write_remaining(remaining)

def log_to_file(edits, renames, deletions):
    treatment_name = util.generate_timestamped_file_name()
    joined_treatment_name = files.get_joined_path(fst.QUEUE, treatment_name)
    data = {
        trf.EDITS     : edits,
        trf.RENAMES   : renames,
        trf.DELETIONS : deletions,
    }
    data[trf.PATHS] = util.generate_paths_dict()
    util.write_to_json(data, joined_treatment_name) 

def main():
    run_checks()

    edits, renames, deletions = list(), dict(), list()
    run_loop(edits, renames, deletions)

    if not (edits or renames or deletions):
        return

    log_to_file(edits, renames, deletions)

if __name__ == '__main__':
    main()
