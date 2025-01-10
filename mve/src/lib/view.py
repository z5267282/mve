import os
import re
import requests
import subprocess
import sys
import typing

import mve.src.constants.colours as colours
import mve.src.constants.commands as commands
import mve.src.constants.timestamp_format as timestamp_format
import mve.src.constants.treatment_format as treatment_format
import mve.src.constants.video_editing as video_editing

import mve.src.helpers.util as util
import mve.src.helpers.time_handlers as time_handlers
import mve.src.helpers.video as video
import mve.src.helpers.video_paths as video_paths
import mve.src.helpers.files as files
import mve.src.helpers.colouring as colouring


def run_loop(
        remaining: list[str],
        edits: list[dict], renames: dict[str, str], deletions: list[str],
        paths: video_paths.VideoPaths, testing: bool, bold: bool,
        verify_name: bool) -> int:
    padding = len(
        str(
            len(remaining)
        )
    )

    while remaining:
        base_name = remaining[0]
        view_video(base_name, testing, paths)

        go_to_next_file = False
        command, raw_tokens = prompt(base_name, padding, len(remaining), bold)
        match command:
            case commands.QUIT:
                break
            case commands.CONTINUE:
                do_continue(remaining, base_name)
            case commands.HELP:
                do_help(bold)
            case commands.END:
                go_to_next_file = do_end(
                    base_name, raw_tokens, edits, paths, bold, verify_name)
            case commands.START:
                go_to_next_file = do_start(
                    base_name, raw_tokens, edits, paths, bold, verify_name)
            case commands.MIDDLE:
                go_to_next_file = do_middle(
                    base_name, raw_tokens, edits, paths, bold, verify_name)
            case commands.WHOLE:
                go_to_next_file = do_whole(
                    base_name, raw_tokens, edits, paths, bold, verify_name)
            case commands.RENAME:
                go_to_next_file = do_rename(
                    base_name, raw_tokens, renames, paths, bold)
            case commands.DELETE:
                go_to_next_file = do_delete(base_name, deletions)
            case _:
                util.print_error(
                    'invalid command \'{}\' - press {} for a list of commands'.format(
                        colouring.highlight(command, bold), commands.HELP
                    ), bold
                )

        if go_to_next_file:
            remaining.pop(0)

    return len(remaining)


def view_video(base_name: str, testing: bool, paths: video_paths.VideoPaths):
    if testing:
        return

    joined_path = files.get_joined_path(paths.source, base_name)
    system = sys.platform
    if system.startswith('win'):
        # this function only comes with the Windows os module
        os.startfile(joined_path)  # type: ignore
    if system.startswith('linux'):
        requests.get('http://localhost:4400/message', params={'v': base_name})
    elif system.startswith('darwin'):
        subprocess.run(['open', joined_path])


def prompt(base_name: str, padding: int, number_remaining: int,
           bold: bool) -> tuple[str, str]:
    coloured_remaining = colouring.colour_box(
        colours.CYAN, f'{number_remaining:^{padding}}', bold)
    args = input(f'{coloured_remaining} - {base_name} : ').split(' ', 1)
    command = args.pop(0)
    raw_tokens = args.pop() if args else ''
    return command, raw_tokens


def do_continue(remaining: list[str], base_name: str):
    remaining.insert(0, base_name)


def do_help(bold: bool):
    print(
        highlight_all_commands(commands.HELP_MESSAGE, bold)
    )


def highlight_all_commands(string: str, bold: bool) -> str:
    def repl(match): return '[{}]'.format(
        highlight_command(match.group(1), bold)
    )
    return re.sub(r'\[(.)\]', repl, string)


def highlight_command(command: str, bold: bool) -> str:
    return colouring.colour_format(colours.PURPLE, command, bold)


def do_end(
        base_name: str, raw_tokens: str, edits: list[dict],
        paths: video_paths.VideoPaths, bold: bool, verify_name: bool) -> bool:
    return do_edit(
        commands.END, base_name, raw_tokens, edits,
        lambda tokens: (tokens[0], None, tokens[1]), paths, bold, verify_name)


def do_edit(
        command: str, base_name: str, raw_tokens: str, edits: list[dict],
        start_end_name_unpacker: typing.Callable[
            # start and end optional, end mandatory
            [list[str]], tuple[None | str, None | str, str]],
        paths: video_paths.VideoPaths, bold: bool, verify_name: bool
) -> bool:
    tokens = parse_tokens(raw_tokens, command, bold)
    if tokens is None:
        return False

    start, end, edit_name = start_end_name_unpacker(tokens)
    regex, format = r'-?[0-9]+', '[ integer | timestamp in form <[hour]-min-sec> ]'

    if start is not None:
        start = parse_time(start, regex, True, format, bold)
        if start is None:
            return False

    if end is not None:
        end = parse_time(end, regex, False, format, bold)
        if end is None:
            return False

    if start is not None and end is not None:
        if not check_times(base_name, start, end, paths, bold):
            return False

    new_name = handle_new_name(edit_name, paths.edits, bold, verify_name)
    if new_name is None:
        return False

    log_edit(base_name, new_name, edits, start, end)
    return True


def parse_tokens(raw_tokens: str, command: str, bold: bool) -> None | list[str]:
    tokens = split_tokens(raw_tokens, command)
    if not tokens:
        no_double_spaces = re.sub(r' {2,}', r' ', commands.USAGE_MSGS[command])
        print_usage_error(
            highlight_all_commands(no_double_spaces, bold), bold)
        return None

    return tokens


def split_tokens(raw_tokens: str, command: str) -> list[str]:
    if not raw_tokens:
        return list()

    n_tokens = commands.NUM_TOKENS[command]
    tokens = tokenise(raw_tokens, n_tokens - 1)
    return tokens if len(tokens) == n_tokens else list()


def tokenise(raw_tokens: str, splits: int) -> list[str]:
    return raw_tokens.split(' ', splits)


def print_usage_error(format: str, bold: bool):
    util.print_error(f'usage: {format}', bold)


def parse_time(raw_time: str, regex: str, is_start: bool, format: str,
               bold: bool) -> None | str:
    time = raw_time
    if re.fullmatch(regex, time):
        time = raw_time
    else:
        time = parse_timestamp(raw_time)

    if time is None:
        print_time_format(is_start, format, bold)

    return time


def parse_timestamp(timestamp: str) -> None | str:
    return \
        timestamp.replace(
            timestamp_format.SHORT_HAND, timestamp_format.REQUIRED) \
        if re.fullmatch(r'([0-5]?[0-9]-)?[0-5]?[0-9]-[0-5]?[0-9]', timestamp) \
        else None


def print_time_format(is_start: bool, format: str, bold: bool):
    util.print_error(
        'the {} time must be in the format {}'.format(
            get_start_end_description(is_start), format), bold)


def check_times(
        base_name: str, start: str, end: str,
        paths: video_paths.VideoPaths, bold: bool) -> bool:
    if start is None and end is None:
        return True

    joined_src_path = files.get_joined_path(paths.source, base_name)
    duration = video.get_duration(joined_src_path)
    if start is None:
        if not check_in_bounds(
                end, time_handlers.get_seconds(end), duration, base_name, bold,
                is_start=False):
            return False

        return True

    if end is None:
        if not check_in_bounds(start, time_handlers.get_seconds(start),
                               duration, base_name, bold):
            return False

        return True

    start_seconds = video.convert_integer_seconds_to_natural_number(
        start, duration)
    end_seconds = video.convert_integer_seconds_to_natural_number(
        end, duration)

    for time, seconds, is_start in zip(
            [start, end], [start_seconds, end_seconds], [True, False]):
        if not check_in_bounds(
                time, seconds, duration, base_name, bold, is_start=is_start):
            return False

    if not end_seconds > start_seconds:
        util.print_error(
            'the end time \'{}\' must be bigger than the start time \'{}\''.format(
                colouring.highlight(end, bold),
                colouring.highlight(start, bold),
            ), bold
        )
        return False

    return True


def check_in_bounds(
        time: str, seconds: int, duration: int, base_name: str, bold: bool,
        is_start: bool = True) -> bool:
    if not in_duration_bounds(seconds, duration):
        print_duration_error(time, base_name, is_start, bold)
        return False

    return True


def in_duration_bounds(seconds: int, duration: int) -> bool:
    return seconds >= 0 and seconds <= duration


def print_duration_error(time: str, name: str, is_start: bool, bold: bool):
    util.print_error(
        'the {} time \'{}\' is not in the bounds of video {}'.format(
            get_start_end_description(is_start),
            colouring.highlight(time, bold), name
        ), bold
    )


def get_start_end_description(is_start: bool) -> str:
    return 'start' if is_start else 'end'


def handle_new_name(
        new_name: str, dst_folder: list[str], bold: bool, validate: bool = True
) -> None | str:
    if validate:
        if not valid_name_format(new_name, bold):
            return None

    new_name = add_suffix(new_name)
    if check_file_exists(new_name, dst_folder, bold):
        return None

    return new_name


def valid_name_format(new_name: str, bold: bool):
    if not correct_name_format(new_name):
        print_name_format(bold)
        return False

    if name_starts_with_number(new_name, bold):
        return False

    return True


def correct_name_format(name: str) -> re.Match[str] | None:
    return re.fullmatch(r'[a-zA-Z0-9 ]+', name)


def print_name_format(bold: bool):
    util.print_error(commands.NAME_FORMAT, bold)


def name_starts_with_number(name: str, bold: bool) -> bool:
    return reprompt_name(name, bold) if re.match(r'[0-9]+', name) else False


def reprompt_name(current_name: str, bold: bool) -> bool:
    '''Given that a name starts with a number, verify whether the user wants
    to re-enter the command by prompting them'''
    warn = colouring.warning(bold)
    print(
        '{} the name \'{}\' starts with a number are you sure you haven\'t misentered the[{}]iddle command?'.format(
            warn, colouring.highlight(current_name, bold),
            highlight_command(commands.MIDDLE, bold)
        )
    )
    change_name = input(
        f'{warn} type \'y\' if you want to re-enter this command : ')
    return change_name == 'y'


def add_suffix(name: str) -> str:
    return f'{name}.{video_editing.SUFFIX}'


def check_file_exists(name: str, folder: list[str], bold: bool) -> bool:
    if os.path.exists(
        files.get_joined_path(folder, name)
    ):
        util.print_error(
            'the file \'{}\' exists in the folder {}'.format(
                colouring.highlight(name, bold), folder
            ), bold
        )
        return True

    return False


def log_edit(
        base_name: str, edit_name: str, edits: list[dict],
        start: None | str, end: None | str):
    new_edit = {
        treatment_format.EDIT_ORIGINAL: base_name,
        treatment_format.EDIT_NAME: edit_name,
        treatment_format.EDIT_TIMES: {
            treatment_format.EDIT_TIMES_START: start,
            treatment_format.EDIT_TIMES_END: end
        }
    }
    edits.append(new_edit)


def do_start(
        base_name: str, raw_tokens: str, edits: list[dict],
        paths: video_paths.VideoPaths, bold: bool, verify_name: bool) -> bool:
    return do_edit(
        commands.START, base_name, raw_tokens, edits,
        lambda tokens: (None, tokens[0], tokens[1]), paths, bold, verify_name)


def do_middle(
        base_name: str, raw_tokens: str, edits: list[dict],
        paths: video_paths.VideoPaths, bold: bool, verify_name: bool) -> bool:
    return do_edit(
        commands.MIDDLE, base_name, raw_tokens, edits,
        lambda tokens: (tokens[0], tokens[1], tokens[2]), paths, bold,
        verify_name)


def do_whole(
        base_name: str, raw_tokens: str, edits: list[dict],
        paths: video_paths.VideoPaths, bold: bool, verify_name: bool) -> bool:
    return do_edit(
        commands.WHOLE, base_name, raw_tokens, edits,
        lambda tokens: (None, None, tokens[0]), paths, bold, verify_name)


def do_rename(
        base_name: str, raw_tokens: str, renames: dict[str, str],
        paths: video_paths.VideoPaths, bold: bool) -> bool:
    tokens = parse_tokens(raw_tokens, commands.RENAME, bold)
    if not tokens:
        return False

    new_name, = tokens
    new_name = handle_new_name(new_name, paths.renames, bold, True)
    if new_name is None:
        return False

    log_rename(base_name, new_name, renames)
    return True


def log_rename(old_name: str, new_name: str, renames: dict[str, str]):
    renames[old_name] = new_name


def do_delete(base_name: str, deletions: list[str]) -> bool:
    log_delete(base_name, deletions)
    return True


def log_delete(base_name: str, deletions: list[str]):
    deletions.append(base_name)


def wrap_session(edits: list[dict], renames: dict[str, str],
                 deletions: list[str]) -> dict:
    return {
        treatment_format.EDITS: edits,
        treatment_format.RENAMES: renames,
        treatment_format.DELETIONS: deletions,
    }
