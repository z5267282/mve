'''Edit one video on a loop.'''

import json
import os
import pathlib
import sys

import config as config

import constants.commands as commands
import constants.defaults as defaults
import constants.json_settings as json_settings
import constants.timestamp_format as timestamp_format

import helpers.video_paths as video_paths

import lib.edit as edit
import lib.view as view


def main():
    args = sys.argv[1:]
    if len(args) != 1:
        print('enter a source file')
        sys.exit(1)

    # path information
    source, = args
    source_path = pathlib.Path(source)
    dir_name: list[str] = list(source_path.parent.parts)
    base_name: str = source_path.name
    destination: list[str] = list(
        pathlib.Path(os.path.join(os.path.expanduser('~'), 'Downloads')).parts
    )

    paths: video_paths.VideoPaths = video_paths.VideoPaths(
        dir_name, destination, destination)

    # TODO: make flag for this
    named: bool = False

    # edit information
    cfg = config.Config(paths.source, paths.renames, paths.edits)
    edits: list[dict] = []
    errors: list[dict] = []
    bold: bool = defaults.BOLD
    while True:
        # Can only enter editing commands (ie. s, m, e) and q
        raw_command: str = input('focus.py : ')
        args: list[str] = raw_command.split(' ', 1)
        command: str = args.pop(0)
        raw_tokens: str = args.pop() if args else ''
        # add command as the name if named mode is turned off
        # TODO: make a more lasting solution than this
        compliant_timestamp: str = raw_command.replace(
            timestamp_format.SHORT_HAND, ' ')
        if not named:
            raw_tokens = f"{raw_tokens} {compliant_timestamp}"
        match command:
            case commands.QUIT:
                break
            case commands.HELP:
                print('enter one of [sme]')
            case commands.END:
                view.do_end(base_name, raw_tokens, edits, paths, bold)
            case commands.START:
                view.do_start(base_name, raw_tokens, edits, paths, bold)
            case commands.MIDDLE:
                view.do_middle(base_name, raw_tokens, edits, paths, bold)

    # Queue stored in memory, not written to disk
    # Then when you quit, edits are performed.
    data = view.wrap_session(edits, {}, [])
    edit.treat_all(data, cfg.use_moviepy, cfg.moviepy_threads,
                   cfg.num_processes, [], errors, paths)
    if errors:
        print('ignoring these files due to errors')
        print(json.dumps(errors, indent=json_settings.INDENT_SPACES))

    print('focus.py complete')


if __name__ == '__main__':
    main()
