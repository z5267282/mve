import os
import re
import requests
import subprocess
import sys

import constants.video_editing as video_editing
import constants.treatment_format as treatment_format
import constants.commands as commands
import constants.colours as colours

import helpers.util as util
import helpers.time_handlers as time_handlers
import helpers.video_paths as video_paths
import helpers.files as files
import helpers.colouring as colouring


def run_loop(
    remaining: list[str],
    edits: list[dict], renames: dict[str, str], deletions: list[str],
    paths: video_paths.VideoPaths, testing: bool
):
    padding = len(
        str(
            len(remaining)
        )
    )

    while remaining:
        base_name = remaining[0]
        view_video(base_name, testing, paths)

        go_to_next_file = False
        command, raw_tokens = prompt(
            base_name, padding, len(remaining)
        )
        match command:
            case commands.QUIT:
                break
            case commands.CONTINUE:
                do_continue(remaining, base_name)
            case commands.HELP:
                do_help()
            case commands.END:
                go_to_next_file = do_end(base_name, raw_tokens, edits, paths)
            case commands.START:
                go_to_next_file = do_start(base_name, raw_tokens, edits, paths)
            case commands.MIDDLE:
                go_to_next_file = do_middle(
                    base_name, raw_tokens, edits, paths)
            case commands.WHOLE:
                go_to_next_file = do_whole(base_name, raw_tokens, edits, paths)
            case commands.RENAME:
                go_to_next_file = do_rename(
                    base_name, raw_tokens, renames, paths)
            case commands.DELETE:
                go_to_next_file = do_delete(base_name, deletions)
            case _:
                util.print_error(
                    'invalid command \'{}\' - press {} for a list of commands'.format(
                        colouring.highlight(command), commands.HELP
                    )
                )

        if go_to_next_file:
            remaining.pop(0)

    return len(remaining)


def view_video(base_name, testing: bool, paths: video_paths.VideoPaths):
    if testing:
        return

    joined_path = files.get_joined_path(paths.source, base_name)
    system = sys.platform
    if system.startswith('win'):
        os.startfile(joined_path)
    if system.startswith('linux'):
        requests.get('http://localhost:4400/message', params={'v': base_name})
    elif system.startswith('darwin'):
        subprocess.run(['open', joined_path])


def prompt(base_name, padding, number_remaining):
    coloured_remaining = colouring.colour_box(
        colours.CYAN, f'{number_remaining:^{padding}}')
    args = input(f'{coloured_remaining} - {base_name} : ').split(' ', 1)
    command = args.pop(0)
    raw_tokens = args.pop() if args else str()
    return command, raw_tokens


def do_continue(remaining, base_name):
    remaining.insert(0, base_name)


def do_help():
    print(
        highlight_all_commands(commands.HELP_MESSAGE)
    )


def highlight_all_commands(string):
    def repl(match): return '[{}]'.format(
        highlight_command(
            match.group(1)
        )
    )
    return re.sub(r'\[(.)\]', repl, string)


def highlight_command(command):
    return colouring.colour_format(colours.PURPLE, command)


def do_end(base_name, raw_tokens, edits, paths: video_paths.VideoPaths):
    return do_edit(
        commands.END, base_name, raw_tokens, edits,
        lambda tokens: (tokens[0], None, tokens[1]), paths,
        integer=True
    )


def do_edit(command, base_name, raw_tokens, edits, start_end_name_unpacker, paths: video_paths.VideoPaths, integer=False):
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

    if not check_times(base_name, start, end, paths):
        return False

    edit_name = handle_new_name(edit_name, paths.edits)
    if edit_name is None:
        return False

    log_edit(base_name, edit_name, edits, start, end)
    return True


def parse_tokens(raw_tokens, command):
    tokens = split_tokens(raw_tokens, command)
    if not tokens:
        no_double_spaces = re.sub(r' {2,}', r' ', commands.USAGE_MSGS[command])
        print_usage_error(
            highlight_all_commands(no_double_spaces)
        )
        return None

    return tokens


def split_tokens(raw_tokens, command):
    if not raw_tokens:
        return list()

    n_tokens = commands.NUM_TOKENS[command]
    tokens = tokenise(raw_tokens, n_tokens - 1)
    return tokens if len(tokens) == n_tokens else list()


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
    util.print_error(
        f'the {get_start_end_description(is_start)} time must be in the format {format}')


def check_times(base_name, start, end, paths: video_paths.VideoPaths):
    if start is None and end is None:
        return True

    joined_src_path = files.get_joined_path(paths.source, base_name)
    duration = get_duration(joined_src_path)
    if start is None:
        if not check_in_bounds(end, time_handlers.get_seconds(end), duration, base_name, is_start=False):
            return False

        return True

    if end is None:
        if not check_in_bounds(start, time_handlers.get_seconds(start), duration, base_name):
            return False

        return True

    start_seconds, end_seconds = time_handlers.get_seconds(
        start), time_handlers.get_seconds(end)
    for time, seconds, is_start in zip([start, end], [start_seconds, end_seconds], [True, False]):
        if not check_in_bounds(time, seconds, duration, base_name, is_start=is_start):
            return False

    if not end_seconds > start_seconds:
        util.print_error(
            'the end time \'{}\' must be bigger than the start time \'{}\''.format(
                colouring.highlight(end), colouring.highlight(start)
            )
        )
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
    util.print_error(
        'the {} time \'{}\' is not in the bounds of video {}'.format(
            get_start_end_description(is_start),
            colouring.highlight(time), name
        )
    )


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
    util.print_error(
        'the name can only contain upper and lowercase letters, digits and spacebars')


def handle_leading_number(name):
    return reprompt_name(name) if re.match(r'[0-9]+', name) else name


def reprompt_name(current_name):
    warn = colouring.warning()
    print(
        '{} the name \'{}\' starts with a number are you sure you haven\'t misentered the[{}]iddle command?'.format(
            warn, colouring.highlight(
                current_name), highlight_command(commands.MIDDLE)
        )
    )
    change_name = input(
        '{warn} type \'y\' if you want to re-enter this command : ')
    return None if change_name == 'y' else current_name


def add_suffix(name):
    return f'{name}.{video_editing.SUFFIX}'


def check_file_exists(name, folder):
    if os.path.exists(
        files.get_joined_path(folder, name)
    ):
        util.print_error(
            'the file \'{}\' exists in the folder {}'.format(
                colouring.highlight(name), folder
            )
        )
        return True

    return False


def log_edit(base_name, edit_name, edits, start, end):
    new_edit = {
        treatment_format.EDIT_ORIGINAL: base_name,
        treatment_format.EDIT_NAME: edit_name,
        treatment_format.EDIT_TIMES: {
            treatment_format.EDIT_TIMES_START: start,
            treatment_format.EDIT_TIMES_END: end
        }
    }
    edits.append(new_edit)


def do_start(base_name, raw_tokens, edits, paths: video_paths.VideoPaths):
    return do_edit(
        commands.START, base_name, raw_tokens, edits,
        lambda tokens: (None, tokens[0], tokens[1]), paths
    )


def do_middle(base_name, raw_tokens, edits, paths: video_paths.VideoPaths):
    return do_edit(
        commands.MIDDLE, base_name, raw_tokens, edits,
        lambda tokens: tokens, paths
    )


def do_whole(base_name, raw_tokens, edits, paths: video_paths.VideoPaths):
    return do_edit(
        commands.WHOLE, base_name, raw_tokens, edits,
        lambda tokens: (None, None, tokens[0]), paths
    )


def do_rename(base_name, raw_tokens, renames, paths: video_paths.VideoPaths):
    tokens = parse_tokens(raw_tokens, commands.RENAME)
    if not tokens:
        return False

    new_name, = tokens
    new_name = handle_new_name(new_name, paths.renames)
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


def wrap_session(edits, renames, deletions):
    return {
        treatment_format.EDITS: edits,
        treatment_format.RENAMES: renames,
        treatment_format.DELETIONS: deletions,
    }
