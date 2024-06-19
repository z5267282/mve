'''Run the mve project as a one-off command-line video editor without history.
Absolute paths must be entered in place of a loaded configuration file.'''

import argparse
import json
import pathlib
import sys
import typing

import config

import constants.error as error
import constants.json_settings as json_settings

import helpers.files as files
import helpers.video_paths as video_paths
import helpers.util as util

import lib.view as view
import lib.edit as edit


def main():
    paths = gen_paths()
    cfg = config.Config(paths.source, paths.renames, paths.edits)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--testing', help='turn on testing mode', action='store_true')
    args = parser.parse_args()

    cfg.recent = False
    cfg.testing = args.testing

    remaining, errors = gen_remaining(paths, cfg.recent), list()
    edits, renames, deletions = list(), dict(), list()
    num_remaining = view.run_loop(remaining, edits, renames,
                                  deletions, paths, cfg.testing)
    data = view.wrap_session(edits, renames, deletions)
    print(
        util.format_remaining(num_remaining)
    )

    edit.treat_all(data, cfg.use_moviepy, cfg.moviepy_threads,
                   cfg.num_processes, remaining, errors, paths)
    handle_errors(errors)
    util.exit_treat_all_good()


def gen_paths() -> video_paths.VideoPaths:
    print('enter absolute paths for the following folders')
    source = input('source : ')
    edits = input('edits : ')
    return video_paths.VideoPaths(
        decompose_path_into_folders(source),
        decompose_path_into_folders(edits),
        decompose_path_into_folders(edits)
    )


def gen_remaining(paths: video_paths.VideoPaths, recent: bool) -> list[str]:
    return files.ls(paths.source, recent=recent)


def decompose_path_into_folders(abs_path: str) -> list[str]:
    path: pathlib.Path = pathlib.Path(abs_path)
    return list(path.parts)


def handle_errors(errors: dict[str, typing.Any]):
    if errors:
        util.print_error(
            json.dumps(errors, indent=json_settings.INDENT_SPACES)
        )
        sys.exit(error.TREATMENT_ERROR)


if __name__ == '__main__':
    main()
