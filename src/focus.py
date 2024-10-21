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
    base_name, dst_folder = obtain_source_name_and_parent_from_command_line(
        bold)
    paths: pathlib.Path = create_paths()

    # edit information
    cfg = config.Config(paths.source, paths.renames, paths.edits)
    edits: list[dict] = []
    errors: list[dict] = []

    while True:
        # up to 2 splits required:
        # <start> <end> [rest is name]
        tokens: list[str] = input('> ').split(' ', 2)
        if tokens[0] == 'q':
            break

        regex, format = r'-?[0-9]+', '[ integer | timestamp in form <[hour]-min-sec> ]'

        match len(tokens):
            case 3:
                start, end, name = tokens
            case 2:
                start, end = tokens
                name = f'{start} {end}'
            case _:
                print('<start> <end> [name]')
                continue

        start = view.parse_time(start, regex, True, format, bold)
        if start is None:
            continue

        end = view.parse_time(end, regex, False, format, bold)
        if end is None:
            continue

        if name.isspace():
            print('name is all whitespace, enter a new name')
            continue

        edit_name: str | None = view.handle_new_name(
            name, dst_folder, bold, False)
        if edit_name is None:
            continue

        view.log_edit(base_name, edit_name, edits, start, end)

    print(
        'successfully logged {} file{}'.format(
            colouring.colour_format(
                colours.PURPLE,
                str(
                    len(edits)
                ),
                bold
            ),
            util.plural(
                len(edits)
            )
        )
    )

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

    print('focus.py complete')


def obtain_source_name_and_parent_from_command_line(
        bold: bool) -> tuple[str, list[str]]:
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('source', type=str)
    args: argparse.Namespace = parser.parse_args()

    source: str = args.source
    if not os.path.exists(source):
        util.print_error(
            f'cannot open file "{colouring.colour_format(colours.CYAN, source, bold)}"',
            bold)
        sys.exit(error.MISSING_SOURCE)

    source_path: pathlib.Path = pathlib.Path(source)
    return source_path.name, list(source_path.parent.parts)


def create_paths(source_parent: list[str]) -> video_paths.VideoPaths:
    destination: list[str] = locate_destination_folder()
    return video_paths.VideoPaths(
        source_parent, destination, destination)


def locate_destination_folder() -> list[str]:
    return list(
        pathlib.Path(
            os.path.join(os.path.expanduser('~'), 'Downloads')
        ).parts
    )


if __name__ == '__main__':
    main()
