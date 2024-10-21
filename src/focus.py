'''Edit one video on a loop.'''

import argparse
import json
import os
import pathlib
import sys

import config as config

import constants.colours as colours
import constants.defaults as defaults
import constants.json_settings as json_settings

import helpers.colouring as colouring
import helpers.util as util
import helpers.video_paths as video_paths

import lib.edit as edit
import lib.view as view


def main():
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('source')
    args: argparse.Namespace = parser.parse_args()

    source_path = pathlib.Path(args.source)
    dir_name: list[str] = list(source_path.parent.parts)
    base_name: str = source_path.name
    dst_folder: list[str] = list(
        pathlib.Path(
            os.path.join(os.path.expanduser('~'), 'Downloads')
        ).parts
    )

    paths: video_paths.VideoPaths = video_paths.VideoPaths(
        dir_name, dst_folder, dst_folder)

    # edit information
    cfg = config.Config(paths.source, paths.renames, paths.edits)
    edits: list[dict] = []
    errors: list[dict] = []
    bold: bool = defaults.BOLD

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


if __name__ == '__main__':
    main()
