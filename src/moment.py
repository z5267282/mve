'''Run the mve project as a one-off command-line video editor without history.
Absolute paths must be entered in place of a loaded configuration file.'''

import argparse
import json
import os
import pathlib
import sys

import config

import constants.error as error
import constants.json_settings as json_settings

import helpers.files as files
import helpers.video_paths as video_paths
import helpers.util as util

import lib.view as view
import lib.edit as edit


def main():
    args = handle_args()
    source, dest = get_paths_from_args(args)

    paths = video_paths.VideoPaths.make_merged_dest_from_defaults(source, dest)
    cfg = config.Config(paths.source, paths.renames, paths.edits)

    configure_settings(cfg, args.testing)

    remaining, errors = gen_remaining(paths, cfg.recent), list()
    edits, renames, deletions = list(), dict(), list()
    num_remaining = view.run_loop(remaining, edits, renames,
                                  deletions, paths, cfg.testing, cfg.bold,
                                  cfg.verify_name)
    data = view.wrap_session(edits, renames, deletions)
    print(
        util.format_remaining(num_remaining, cfg.bold)
    )

    edit.treat_all(data, cfg.use_moviepy, cfg.moviepy_threads,
                   cfg.num_processes, remaining, errors, paths)
    handle_errors(errors, cfg.bold)
    util.exit_treat_all_good(cfg.bold)


def handle_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('--testing', help='turn on testing mode',
                        action='store_true')
    source_args = parser.add_mutually_exclusive_group()
    source_args.add_argument('--source', type=str, help='the source folder')
    source_args.add_argument('--desktop', action='store_true',
                             help='set the source folder as Desktop')

    dest_args = parser.add_mutually_exclusive_group()
    dest_args.add_argument('--dest', type=str,
                           help='the location of edits and renames')
    dest_args.add_argument('--downloads', action='store_true',
                           help='set the destination folder as Downloads')

    return parser.parse_args()


def get_paths_from_args(
        args: argparse.Namespace) -> tuple[None | str, None | str]:

    source = args.source
    if args.desktop:
        source = os.path.join(os.path.expanduser('~'), 'Desktop')

    dest = args.dest
    if args.downloads:
        dest = os.path.join(os.path.expanduser('~'), 'Downloads')

    return source, dest


def gen_remaining(paths: video_paths.VideoPaths, recent: bool) -> list[str]:
    return files.ls(paths.source, recent=recent)


def decompose_path_into_folders(abs_path: str) -> list[str]:
    path: pathlib.Path = pathlib.Path(abs_path)
    return list(path.parts)


def configure_settings(cfg: config.Config, testing: bool):
    cfg.recent = False
    cfg.testing = testing
    cfg.verify_name = False


def handle_errors(errors: list[dict], bold: bool):
    if errors:
        util.print_error(
            json.dumps(errors, indent=json_settings.INDENT_SPACES), bold
        )
        sys.exit(error.TREATMENT_ERROR)


if __name__ == '__main__':
    main()
