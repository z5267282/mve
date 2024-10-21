'''Edit one video on a loop.'''

import argparse
import json
import os
import pathlib
import sys

import config as config

import constants.colours as colours
import constants.defaults as defaults
import constants.error as error
import constants.json_settings as json_settings

import helpers.colouring as colouring
import helpers.util as util
import helpers.video_paths as video_paths

import lib.edit as edit
import lib.view as view


def main():
    bold: bool = defaults.BOLD
    source, paths = make_source_and_paths(bold)

    # edit information
    cfg = config.Config(paths.source, paths.renames, paths.edits)
    edits, errors = [], []

    while True:
        # up to 2 splits required:
        # <start> <end> [rest is name]
        tokens: str = input('> ')
        if tokens == 'q':
            break

        try:
            start, end, name = parse_and_validate_tokens(
                tokens, bold, paths.edits)
            view.log_edit(source, name, edits, start, end)
        except BadTokenException:
            continue

    finish_program(edits, errors, cfg, paths, bold)


def make_source_and_paths(bold: bool) -> tuple[str, video_paths.VideoPaths]:
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('source', type=str)
    parser.add_argument(
        '--destination', type=str, default=os.path.join(
            os.path.expanduser('~'), 'Downloads')
    )
    args: argparse.Namespace = parser.parse_args()

    source: str = args.source
    if not os.path.exists(source):
        util.print_error(
            f'cannot open file "{colouring.colour_format(colours.CYAN, source, bold)}"',
            bold)
        sys.exit(error.NO_SOURCE_FILE)

    source_path: pathlib.Path = pathlib.Path(source)
    source_folder: list[str] = list(source_path.parent.parts)
    destination_folder: list[str] = list(
        pathlib.Path(args.destination).parts)
    return source_path.name, video_paths.VideoPaths(source_folder,
                                                    destination_folder,
                                                    destination_folder)


class BadTokenException(Exception):
    pass


def parse_and_validate_tokens(
        raw_tokens: str, bold: bool, destination: list[str]
) -> tuple[str, str, str]:
    unpacked = parse_start_end_name(raw_tokens)
    if unpacked is None:
        raise BadTokenException()

    start, end, name = unpacked
    return validate_start_end_name(start, end, name, bold, destination)


def parse_start_end_name(raw_tokens: str) -> tuple[str, str, str] | None:
    tokens: list[str] = raw_tokens.split(' ', 2)
    if len(tokens) < 2:
        print('<start> <end> [name]')
        return None

    start: str = tokens.pop(0)
    end: str = tokens.pop(0)
    name: str = tokens.pop(0) if tokens else f'{start} {end}'

    return start, end, name


def validate_start_end_name(start: str, end: str, name: str,
                            bold: bool, destination: list[str]
                            ) -> tuple[str, str, str]:
    regex, format = r'-?[0-9]+', '[ integer | timestamp in form <[hour]-min-sec> ]'

    start_seconds: str | None = view.parse_time(
        start, regex, True, format, bold)
    if start_seconds is None:
        raise BadTokenException()

    end_seconds: str | None = view.parse_time(end, regex, False, format, bold)
    if end_seconds is None:
        raise BadTokenException()

    if name.isspace():
        print('name is all whitespace, enter a new name')
        raise BadTokenException()

    edit_name: str | None = view.handle_new_name(
        name, destination, bold, False)
    if edit_name is None:
        raise BadTokenException()

    return start_seconds, end_seconds, edit_name


def finish_program(edits: list, errors: list, cfg: config.Config,
                   paths: video_paths.VideoPaths, bold: bool):
    print_number_edits(
        len(edits), bold
    )
    edit_files(edits, errors, cfg, paths)
    print('focus.py complete')


def print_number_edits(num_edits: int, bold: bool):
    print(
        'successfully logged {} file{}'.format(
            colouring.colour_format(colours.PURPLE, str(num_edits), bold),
            util.plural(num_edits)
        )
    )


def edit_files(edits: list, errors: list, cfg: config.Config, paths: video_paths.VideoPaths):
    # Queue stored in memory, not written to disk
    # Then when you quit, edits are performed.
    data = view.wrap_session(edits, {}, [])
    edit.treat_all(data, cfg.use_moviepy, cfg.moviepy_threads,
                   cfg.num_processes, [], errors, paths)
    if errors:
        print('ignoring these files due to errors')
        print(
            json.dumps(errors, indent=json_settings.INDENT_SPACES)
        )


if __name__ == '__main__':
    main()
