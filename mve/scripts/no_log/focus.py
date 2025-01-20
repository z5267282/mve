import argparse
import json
import os
import pathlib
import sys

from mve.src.config import Config

import mve.src.constants.colours as colours
import mve.src.constants.defaults as defaults
import mve.src.constants.error as error
import mve.src.constants.json_settings as json_settings

import mve.src.helpers.colouring as colouring
import mve.src.helpers.util as util
from mve.src.helpers.video_paths import VideoPaths

import mve.src.lib.edit as edit
import mve.src.lib.view as view


from mve.scripts.script import Script
from mve.scripts.script_option import ScriptOption


class Focus(Script):
    def __init__(self):
        super().__init__(str(ScriptOption.FOCUS))

    def main(self, argv: list[str]) -> None:
        source, folders, opts = self.make_source_paths_opts(
            argv, defaults.BOLD)

        # edit information
        cfg = Config(folders, **opts)
        edits, errors = [], []

        while True:
            # up to 2 splits required:
            # <start> <end> [rest is name]
            tokens: str = input('> ')
            if tokens == 'q':
                break

            try:
                start, end, name = self.parse_and_validate_tokens(
                    tokens, cfg.bold, folders.edits)
                view.log_edit(source, name, edits, start, end)
            except self.BadTokenException:
                print('format: [q]uit, or <start> <end> [name]')
                continue

        self.finish_program(edits, errors, cfg, folders, cfg.bold)

    def make_source_paths_opts(self, argv: list[str],
                               bold: bool) -> tuple[str, VideoPaths, dict]:
        parser: argparse.ArgumentParser = argparse.ArgumentParser()
        parser.add_argument('source', type=str)
        parser.add_argument(
            '--destination', type=str, default=os.path.join(
                os.path.expanduser('~'), 'Downloads')
        )
        args, opt_argv = parser.parse_known_args(argv)
        opts = Config.create_options_dict_from_args(opt_argv)

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

        return source_path.name, VideoPaths(source_folder, destination_folder, destination_folder), opts

    class BadTokenException(Exception):
        pass

    def parse_and_validate_tokens(self,
                                  raw_tokens: str, bold: bool, destination: list[str]
                                  ) -> tuple[str, str, str]:
        unpacked = self.parse_start_end_name(raw_tokens)
        if unpacked is None:
            raise self.BadTokenException()

        start, end, name = unpacked
        return self.validate_start_end_name(start, end, name, bold, destination)

    def parse_start_end_name(self, raw_tokens: str) -> tuple[str, str, str] | None:
        tokens: list[str] = raw_tokens.split(' ', 2)
        if len(tokens) < 2:
            print('<start> <end> [name]')
            return None

        start: str = tokens.pop(0)
        end: str = tokens.pop(0)
        name: str = tokens.pop(0) if tokens else f'{start} {end}'

        return start, end, name

    def validate_start_end_name(self, start: str, end: str, name: str,
                                bold: bool, destination: list[str]
                                ) -> tuple[str, str, str]:
        regex, format = r'-?[0-9]+', '[ integer | timestamp in form <[hour]-min-sec> ]'

        start_seconds: str | None = view.parse_time(
            start, regex, True, format, bold)
        if start_seconds is None:
            raise self.BadTokenException()

        end_seconds: str | None = view.parse_time(
            end, regex, False, format, bold)
        if end_seconds is None:
            raise self.BadTokenException()

        if name.isspace():
            print('name is all whitespace, enter a new name')
            raise self.BadTokenException()

        edit_name: str | None = view.handle_new_name(
            name, destination, bold, False)
        if edit_name is None:
            raise self.BadTokenException()

        return start_seconds, end_seconds, edit_name

    def finish_program(self, edits: list, errors: list, cfg: Config,
                       paths: VideoPaths, bold: bool):
        self.print_number_edits(
            len(edits), bold
        )
        self.edit_files(edits, errors, cfg, paths)
        print('focus.py complete')

    def print_number_edits(self, num_edits: int, bold: bool):
        print(
            'successfully logged {} file{}'.format(
                colouring.colour_format(colours.PURPLE, str(num_edits), bold),
                util.plural(num_edits)
            )
        )

    def edit_files(self, edits: list, errors: list, cfg: Config,
                   paths: VideoPaths):
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

    def obtain_source_name_and_parent_from_command_line(self,
                                                        bold: bool) -> tuple[str, list[str]]:
        parser: argparse.ArgumentParser = argparse.ArgumentParser()
        parser.add_argument('source', type=str)
        args: argparse.Namespace = parser.parse_args()

        source: str = args.source
        if not os.path.exists(source):
            util.print_error(
                f'cannot open file "{colouring.colour_format(colours.CYAN, source, bold)}"',
                bold)
            sys.exit(error.NO_SOURCE_FILE)

        source_path: pathlib.Path = pathlib.Path(source)
        return source_path.name, list(source_path.parent.parts)

    def create_paths(self, source_parent: list[str]) -> VideoPaths:
        destination: list[str] = self.locate_destination_folder()
        return VideoPaths(
            source_parent, destination, destination)

    def locate_destination_folder(self, ) -> list[str]:
        return list(
            pathlib.Path(
                os.path.join(os.path.expanduser('~'), 'Downloads')
            ).parts
        )
