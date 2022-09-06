import os
import re
import subprocess
import sys

import config as cfg

import constants.colour as clr
import constants.commands as cmd
import constants.error as err
import constants.file_structure as fst
import constants.treatment_format as trf
import constants.video_editing as vde

import helpers.check_and_exit_if as check_and_exit_if
import helpers.files as files
import helpers.util as util


def main():
    run_checks()

    edits, renames, deletions = list(), dict(), list()
    num_remaining = run_loop(edits, renames, deletions)

    if edits or renames or deletions:
        log_to_file(edits, renames, deletions)

    util.exit_success(f'exited with {util.colour_format(clr.CYAN, num_remaining)} file{"" if num_remaining == 1 else "s"} remaining')


def run_checks():
    check_and_exit_if.bad_args(sys.argv)
    check_no_remaining()
    check_and_exit_if.no_source_folder()
    check_and_exit_if.no_queue()

def check_no_remaining():
    if not os.path.exists(fst.REMAINING):
        util.stderr_print(f"the remaining file '{util.highlight(fst.REMAINING)}' doesn't exist")
        sys.exit(err.MISSING_REMAINING)


def run_loop(edits, renames, deletions):
    remaining = util.load_remaining()
    padding = len(
        str(
            len(remaining)
        )
    )

    while remaining:
        base_name = remaining[0]
        view_video(base_name)
        
        go_to_next_file = False
        command, raw_tokens = prompt(base_name, padding, len(remaining))
        match command:
            case cmd.QUIT:
                break
            case cmd.CONTINUE:
                do_continue(remaining, base_name)
            case cmd.HELP:
                do_help()
            case cmd.END:
                go_to_next_file = do_end(base_name, raw_tokens, edits)
            case cmd.MIDDLE:
                go_to_next_file = do_middle(base_name, raw_tokens, edits)
            case cmd.RENAME:
                go_to_next_file = do_rename(base_name, raw_tokens, renames)
            case cmd.DELETE:
                go_to_next_file = do_delete(base_name, deletions)
            case _:
                util.print_error(f"invalid command '{util.highlight(command)}' - press {cmd.HELP} for a list of commands")

        if go_to_next_file:
            remaining.pop(0)
    
    util.write_remaining(remaining)
    return len(remaining)

def view_video(base_name):
    if cfg.TESTING:
        return

    joined_path = files.get_joined_path(cfg.SOURCE, base_name)

    system = sys.platform
    if system.startswith('win'):
        os.startfile(joined_path)
    elif system.startswith('darwin'):
        subprocess.run(['open', joined_path])

def prompt(base_name, padding, number_remaining):
    coloured_remaining = util.colour_box(clr.CYAN, f'{number_remaining:^{padding}}')
    args = input(f'{coloured_remaining} - {base_name} : ').split(' ', 1)
    command = args[0]
    raw_tokens = args[1] if len(args) == 2 else str()
    return command, raw_tokens

def do_continue(remaining, base_name):
    remaining.insert(0, base_name)

def do_help():
    print(cmd.MESSAGE)

def do_end(base_name, raw_tokens, edits):
    tokens = parse_tokens(raw_tokens, cmd.END)
    if not tokens:
        print_usage_error(f'[{highlight_command("e")}]nd | [ time ] [ name ]')
        return False

    raw_time, edit_name = tokens
    time = None
    if re.fullmatch(r'-?[0-9]+', raw_time):
        time = raw_time
    else:
        time = parse_timestamp(raw_time)

    if time is None:
        print_time_format('end', '[ integer | timestamp in form <[hour]-min-sec> ]')
        return False 
    
    if not in_duration_bounds(base_name, time):
        print_duration_error(time, base_name)
        return False 

    if not correct_name_format(edit_name):
        print_name_format()
        return False
    
    edit_name = handle_leading_number(edit_name)
    if edit_name is None:
        return False
    
    edit_name = add_suffix(edit_name)
    if check_file_exists(edit_name, cfg.DESTINATION):
        return False

    log_edit(base_name, edit_name, [time], edits)
    return True

def parse_tokens(raw_tokens, command):
    if not raw_tokens:
        return []

    n_tokens = cmd.NUM_TOKENS[command]
    tokens = tokenise(raw_tokens, n_tokens - 1)
    return tokens if len(tokens) == n_tokens else []

def tokenise(raw_tokens, splits):
    return raw_tokens.split(' ', splits)

def print_usage_error(format):
    util.print_error(f'usage: {format}')

def highlight_command(command):
    return util.colour_format(clr.PURPLE, command)

def parse_timestamp(timestamp):
    return timestamp.replace('-', ':') if re.fullmatch(r'([0-5]?[0-9]-)?[0-5]?[0-9]-[0-5]?[0-9]', timestamp) else None

def print_time_format(name, form):
    util.print_error(f'the {name} time must be in the form {form}')

def in_duration_bounds(base_name, time):
    joined_src_path = files.get_joined_path(cfg.SOURCE, base_name)
    duration = get_duration(joined_src_path)

    seconds = None
    if time.startswith('-'):
        seconds = int(time[1:]) 
    elif ':' in time:
        seconds = get_timestamp_seconds(time)
    else:
        seconds = int(time)

    return seconds >= 0 and seconds <= duration

def get_duration(joined_src_path):
    args = [
        'ffprobe',
        '-i',
        joined_src_path,
        '-v',
        'quiet',
        '-show_entries',
        'format=duration',
        '-hide_banner',
        '-of',
        'default=noprint_wrappers=1:nokey=1'
    ]
    result = subprocess.run(args, capture_output=True, text=True)

    return int(float(result.stdout))

def get_timestamp_seconds(timestamp):
    return sum(
        int(t) * (60 ** i)
            for i, t in enumerate(reversed(timestamp.split(':')))
    )

def print_duration_error(time, name):
    util.print_error(f"time '{util.highlight(time)}' is not in the bounds of video {name}")

def correct_name_format(name):
    return re.fullmatch(r'[a-zA-Z0-9 ]+', name)

def print_name_format():
    util.print_error('the name can only contain upper and lowercase letters, digits and spacebars')

def handle_leading_number(name):
    return reprompt_name(name) if re.match(r'[0-9]+', name) else name

def reprompt_name(current_name):
    warn = util.colour_box(clr.YELLOW, 'warning')
    print(f"{warn} the name '{util.highlight(current_name)}' starts with a number are you sure you haven't misentered the [m]iddle command?")
    change_name = input(f"{warn} type 'y' if you want to re-enter this command : ")
    return None if change_name == 'y' else current_name

def add_suffix(name):
    return f'{name}.{vde.SUFFIX}'

def check_file_exists(name, folder):
    if os.path.exists(
        files.get_joined_path(folder, name)        
    ):
        util.print_error(f"the file '{util.highlight(name)}' exists in the folder {folder}")
        return True
    
    return False

def log_edit(base_name, edit_name, times, edits):
    new_edit = {
        trf.EDIT_ORIGINAL : base_name,
        trf.EDIT_NAME     : edit_name,
        trf.EDIT_TIMES    : times
    }
    edits.append(new_edit)

def do_middle(base_name, raw_tokens, edits):
    tokens = parse_tokens(raw_tokens, cmd.MIDDLE)
    if not tokens:
        print_usage_error(f'[{highlight_command("m")}]iddle | [ start ] [ end ] [ name ]')
        return False

    start, end, edit_name = tokens
    times = []
    for value, description in zip([start, end], ['start', 'end']):
        time = None
        if re.fullmatch(r'[0-9]+', value):
            time = value
        else:
            time = parse_timestamp(value) 

        if time is None:
            print_time_format(description, '[ natural number | timestamp in form <[hour]-min-sec> ]')
            return False
        
        if not in_duration_bounds(base_name, time):
            print_duration_error(time, base_name)
            return False

        times.append(time)
    
    if not correct_name_format(edit_name):
        print_name_format()
        return False
    
    if check_file_exists(edit_name, cfg.DESTINATION):
        return False
    
    edit_name = handle_leading_number(edit_name)
    if edit_name is None:
        return False
    
    edit_name = add_suffix(edit_name)
    if check_file_exists(edit_name, cfg.DESTINATION):
        return False

    log_edit(base_name, edit_name, times, edits)
    return True

def do_rename(base_name, raw_tokens, renames):
    tokens = parse_tokens(raw_tokens, cmd.RENAME)
    if not tokens:
        print_usage_error(f'[{highlight_command("r")}]ename | [ name ]')
        return False
    
    new_name, = tokens
    if not correct_name_format(new_name):
        print_name_format()
        return False

    new_name = handle_leading_number(new_name)

    if new_name is None:
        return False
    
    new_name = add_suffix(new_name)
    if check_file_exists(new_name, cfg.RENAMES):
        return False
    
    log_rename(base_name, new_name, renames)
    return True

def log_rename(old_name, new_name, renames):
    renames[old_name] = new_name

def do_delete(base_name, deletions):
    log_delete(base_name, deletions)
    return True

def log_delete(base_name, deletions):
    deletions.append(base_name)


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


if __name__ == '__main__':
    main()
