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
import helpers.colours as colours
import helpers.files as files
import helpers.json_handlers as json_handlers
import helpers.time_handlers as time_handlers
import helpers.timestamps as timestamps
import helpers.util as util


def main():
    run_checks()

    edits, renames, deletions = list(), dict(), list()
    num_remaining = run_loop(edits, renames, deletions)

    if edits or renames or deletions:
        log_to_file(edits, renames, deletions)

    util.exit_success(f'exited with {colours.colour_format(clr.CYAN, num_remaining)} file{str() if num_remaining == 1 else "s"} remaining')


def run_checks():
    check_and_exit_if.bad_args(sys.argv)
    check_no_remaining()
    check_and_exit_if.no_source_folder()
    check_and_exit_if.no_queue()

def check_no_remaining():
    if not os.path.exists(fst.REMAINING):
        util.stderr_print(f"the remaining file '{colours.highlight(fst.REMAINING)}' doesn't exist")
        sys.exit(err.MISSING_REMAINING)


def run_loop(edits, renames, deletions):
    remaining = json_handlers.load_remaining()
    padding = len(
        str(
            len(remaining)
        )
    )

    while remaining:
        base_name = remaining[0]
        view_video(base_name)

        go_to_next_file = False
        command, raw_tokens = prompt(
            base_name, padding, len(remaining)
        )
        match command:
            case cmd.QUIT:
                break
            case cmd.CONTINUE:
                do_continue(remaining, base_name)
            case cmd.HELP:
                do_help()
            case cmd.END:
                go_to_next_file = do_end(base_name, raw_tokens, edits)
            case cmd.START:
                go_to_next_file = do_start(base_name, raw_tokens, edits)
            case cmd.MIDDLE:
                go_to_next_file = do_middle(base_name, raw_tokens, edits)
            case cmd.WHOLE:
                go_to_next_file = do_whole(base_name, raw_tokens, edits)
            case cmd.RENAME:
                go_to_next_file = do_rename(base_name, raw_tokens, renames)
            case cmd.DELETE:
                go_to_next_file = do_delete(base_name, deletions)
            case _:
                util.print_error(f"invalid command '{colours.highlight(command)}' - press {cmd.HELP} for a list of commands")

        if go_to_next_file:
            remaining.pop(0)

    json_handlers.write_remaining(remaining)
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
    coloured_remaining = colours.colour_box(clr.CYAN, f'{number_remaining:^{padding}}')
    args = input(f'{coloured_remaining} - {base_name} : ').split(' ', 1)
    command = args.pop(0)
    raw_tokens = args.pop() if args else str()
    return command, raw_tokens

def do_continue(remaining, base_name):
    remaining.insert(0, base_name)

def do_help():
    print(
        highlight_all_commands(cmd.HELP_MESSAGE)
    )

def highlight_all_commands(string):
    repl = lambda match: '[{}]'.format(
        highlight_command(
            match.group(1)
        )
    )
    return re.sub(r'\[(.)\]', repl, string)

def highlight_command(command):
    return colours.colour_format(clr.PURPLE, command)

def do_end(base_name, raw_tokens, edits):
    return do_edit(
        cmd.END, base_name, raw_tokens, edits,
        lambda tokens: (tokens[0], None, tokens[1]),
        integer=True
    )

def do_edit(command, base_name, raw_tokens, edits, start_end_name_unpacker, integer=False):
    tokens = parse_tokens(raw_tokens, command)
    if tokens is None:
        return False

    start, end, edit_name = start_end_name_unpacker(tokens)
    regex, format = r'[0-9]+', '[ natural number | timestamp in form <[hour]-min-sec> ]'
    if integer:
        regex, format = r'-?[0-9]+', '[ integer | timestamp in form <[hour]-min-sec> ]'

    if not start is None:
        start = parse_time(start, regex, True, format)
        if start is None:
            return False

    if not end is None:
        end = parse_time(end, regex, False, format)
        if end is None:
            return False

    if not check_times(base_name, start, end):
        return False

    edit_name = handle_new_name(edit_name, cfg.DESTINATION)
    if edit_name is None:
        return False

    log_edit(base_name, edit_name, edits, start, end)
    return True

def parse_tokens(raw_tokens, command):
    tokens = split_tokens(raw_tokens, command)
    if not tokens:
        no_double_spaces = re.sub(r' {2,}', r' ', cmd.USAGE_MSGS[command])
        print_usage_error(
            highlight_all_commands(no_double_spaces)
        )
        return None

    return tokens

def split_tokens(raw_tokens, command):
    if not raw_tokens:
        return []

    n_tokens = cmd.NUM_TOKENS[command]
    tokens = tokenise(raw_tokens, n_tokens - 1)
    return tokens if len(tokens) == n_tokens else []

def tokenise(raw_tokens, splits):
    return raw_tokens.split(' ', splits)

def print_usage_error(format):
    util.print_error(f'usage: {format}')

def parse_time(raw_time, regex, is_start, format):
    time = raw_time
    if re.fullmatch(regex, time):
        time = raw_time
    else:
        time = parse_timestamp(raw_time)

    if time is None:
        print_time_format(is_start, format)

    return time

def parse_timestamp(timestamp):
    return timestamp.replace('-', ':') if re.fullmatch(r'([0-5]?[0-9]-)?[0-5]?[0-9]-[0-5]?[0-9]', timestamp) else None

def print_time_format(is_start, format):
    util.print_error(f'the {get_start_end_description(is_start)} time must be in the format {format}')

def check_times(base_name, start, end):
    if start is None and end is None:
        return True

    joined_src_path = files.get_joined_path(cfg.SOURCE, base_name)
    duration = get_duration(joined_src_path)
    if start is None:
        if not check_in_bounds(end, time_handlers.get_seconds(end), duration, base_name, is_start=False):
            return False

        return True

    if end is None:
        if not check_in_bounds(start, time_handlers.get_seconds(start), duration, base_name):
            return False

        return True

    start_seconds, end_seconds = time_handlers.get_seconds(start), time_handlers.get_seconds(end)
    for time, seconds, is_start in zip([start, end], [start_seconds, end_seconds], [True, False]):
        if not check_in_bounds(time, seconds, duration, base_name, is_start=is_start):
            return False

    if not end_seconds > start_seconds:
        util.print_error(f"the end time '{colours.highlight(end)}' must be bigger than the start time '{colours.highlight(start)}'")
        return False

    return True

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
    return round_float(result.stdout)

def round_float(float_string):
    match = re.match(r'([(0-9)]+)\.([0-9])', float_string)
    whole_number, tenths = int(match.group(1)), int(match.group(2))
    return whole_number + (tenths >= 5)

def check_in_bounds(time, seconds, duration, base_name, is_start=True):
    if not in_duration_bounds(seconds, duration):
        print_duration_error(time, base_name, is_start)
        return False

    return True

def in_duration_bounds(seconds, duration):
    return seconds >= 0 and seconds <= duration

def print_duration_error(time, name, is_start):
    util.print_error(f"the {get_start_end_description(is_start)} time '{colours.highlight(time)}' is not in the bounds of video {name}")

def get_start_end_description(is_start):
    return 'start' if is_start else 'end'

def handle_new_name(new_name, dst_folder):
    if not correct_name_format(new_name):
        print_name_format()
        return None

    new_name = handle_leading_number(new_name)
    if not new_name is None:
        new_name = add_suffix(new_name)
        if check_file_exists(new_name, dst_folder):
            return None

    return new_name

def correct_name_format(name):
    return re.fullmatch(r'[a-zA-Z0-9 ]+', name)

def print_name_format():
    util.print_error('the name can only contain upper and lowercase letters, digits and spacebars')

def handle_leading_number(name):
    return reprompt_name(name) if re.match(r'[0-9]+', name) else name

def reprompt_name(current_name):
    warn = colours.colour_box(clr.YELLOW, 'warning')
    print(
        "{} the name '{}' starts with a number are you sure you haven't misentered the [{}]iddle command?".format(
            warn, colours.highlight(current_name), highlight_command(cmd.MIDDLE)
        )
    )
    change_name = input(f"{warn} type 'y' if you want to re-enter this command : ")
    return None if change_name == 'y' else current_name

def add_suffix(name):
    return f'{name}.{vde.SUFFIX}'

def check_file_exists(name, folder):
    if os.path.exists(
        files.get_joined_path(folder, name)
    ):
        util.print_error(f"the file '{colours.highlight(name)}' exists in the folder {folder}")
        return True

    return False

def log_edit(base_name, edit_name, edits, start, end):
    new_edit = {
        trf.EDIT_ORIGINAL : base_name,
        trf.EDIT_NAME     : edit_name,
        trf.EDIT_TIMES    : {
            trf.EDIT_TIMES_START : start,
            trf.EDIT_TIMES_END   : end
        }
    }
    edits.append(new_edit)

def do_start(base_name, raw_tokens, edits):
    return do_edit(
        cmd.START, base_name, raw_tokens, edits,
        lambda tokens: (None, tokens[0], tokens[1])
    )

def do_middle(base_name, raw_tokens, edits):
    return do_edit(
        cmd.MIDDLE, base_name, raw_tokens, edits,
        lambda tokens: tokens
    )

def do_whole(base_name, raw_tokens, edits):
    return do_edit(
        cmd.WHOLE, base_name, raw_tokens, edits,
        lambda tokens: (None, None, tokens[0])
    )

def do_rename(base_name, raw_tokens, renames):
    tokens = parse_tokens(raw_tokens, cmd.RENAME)
    if not tokens:
        return False

    new_name, = tokens
    new_name = handle_new_name(new_name, cfg.RENAMES)
    if new_name is None:
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
    treatment_name = timestamps.generate_timestamped_file_name()
    joined_treatment_name = files.get_joined_path(fst.QUEUE, treatment_name)
    data = {
        trf.EDITS     : edits,
        trf.RENAMES   : renames,
        trf.DELETIONS : deletions,
    }
    data[trf.PATHS] = util.generate_paths_dict()
    json_handlers.write_to_json(data, joined_treatment_name)


if __name__ == '__main__':
    main()
