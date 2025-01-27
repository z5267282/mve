import argparse
import json
import os
import pathlib
import sys

from mve.src.config import Config

import mve.src.constants.error as error
import mve.src.constants.json_settings as json_settings

import mve.src.helpers.files as files
from mve.src.helpers.video_paths import VideoPaths
import mve.src.helpers.util as util

import mve.src.lib.view as view
import mve.src.lib.edit as edit


from mve.scripts.script import Script
from mve.scripts.script_option import ScriptOption


class Moment(Script):
    def __init__(self):
        super().__init__(str(ScriptOption.MOMENT))

    def main(self, argv: list[str]) -> None:
        args, opts = self.handle_args(argv)
        source, dest = self.get_paths_from_args(args)

        folders = VideoPaths.make_merged_dest_from_defaults(
            source, dest)
        cfg = Config(folders, **opts)

        remaining, errors = self.gen_remaining(folders, cfg.recent), list()
        edits, renames, deletions = list(), dict(), list()
        num_remaining = view.run_loop(remaining, edits, renames,
                                      deletions, folders, cfg.testing, cfg.bold,
                                      cfg.verify_name)
        data = view.wrap_session(edits, renames, deletions)
        print(
            util.format_remaining(num_remaining, cfg.bold)
        )

        edit.treat_all(data, cfg.use_moviepy, cfg.moviepy_threads,
                       cfg.num_processes, remaining, errors, folders)
        self.handle_errors(errors, cfg.bold)
        util.exit_treat_all_good(cfg.bold)

    def handle_args(self,
                    argv: list[str]) -> tuple[argparse.Namespace, dict]:
        parser = argparse.ArgumentParser()

        source_args = parser.add_mutually_exclusive_group()
        source_args.add_argument('--source', type=str,
                                 help='the source folder')
        source_args.add_argument('--desktop', action='store_true',
                                 help='set the source folder as Desktop')

        dest_args = parser.add_mutually_exclusive_group()
        dest_args.add_argument('--dest', type=str,
                               help='the location of edits and renames')
        dest_args.add_argument('--downloads', action='store_true',
                               help='set the destination folder as Downloads')

        Config.add_options_subparser(parser)
        args = parser.parse_args(argv)
        opts = {k: v for k, v in vars(args).items() if not k in {
            'source', 'desktop', 'dest', 'downloads'}}

        return args, opts

    def get_paths_from_args(
            self, args: argparse.Namespace) -> tuple[None | str, None | str]:

        source = args.source
        if args.desktop:
            source = os.path.join(os.path.expanduser('~'), 'Desktop')

        dest = args.dest
        if args.downloads:
            dest = os.path.join(os.path.expanduser('~'), 'Downloads')

        return source, dest

    def gen_remaining(
            self, paths: VideoPaths, recent: bool) -> list[str]:
        return files.ls(paths.source, recent=recent)

    def decompose_path_into_folders(self, abs_path: str) -> list[str]:
        path: pathlib.Path = pathlib.Path(abs_path)
        return list(path.parts)

    def handle_errors(self, errors: list[dict], bold: bool):
        if errors:
            util.print_error(
                json.dumps(errors, indent=json_settings.INDENT_SPACES), bold
            )
            sys.exit(error.TREATMENT_ERROR)
