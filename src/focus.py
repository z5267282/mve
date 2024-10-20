'''Edit one video on a loop.'''

import argparse
import json
import os
import pathlib
import shlex
import sys
import typing

import config as config

import constants.commands as commands
import constants.defaults as defaults
import constants.json_settings as json_settings
import constants.timestamp_format as timestamp_format

import helpers.video_paths as video_paths

import lib.edit as edit
import lib.view as view


class Commander(argparse.ArgumentParser):
    def exit(self, status=0, message=None) -> typing.NoReturn:
        print('bob')


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

    # edit information
    cfg = config.Config(paths.source, paths.renames, paths.edits)
    edits: list[dict] = []
    errors: list[dict] = []
    bold: bool = defaults.BOLD

    commander: argparse.ArgumentParser = argparse.ArgumentParser()
    commander.add_argument('-n', '--name', type=str)
    commander.add_argument('start', type=str)
    commander.add_argument('end', type=str)

    while True:
        raw: str = input('> ')
        if raw == 'q':
            break

        # don't crash program if bad args are split
        tokens: argparse.Namespace = commander.parse_args(
            shlex.split(raw)
        )

        # check start
        # check end
        # check name
        # do edit
        view.do_edit('', base_name, '', edits,
                     lambda _: (tokens.start, tokens.end, f'{tokens.start} {tokens.end}'), paths, bold, False)

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
