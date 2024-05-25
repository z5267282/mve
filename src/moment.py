import json
import pathlib
import sys
import typing

import config

import constants.error as error
import constants.json_settings as json_settings

import helpers.files as files
import helpers.paths as paths
import helpers.util as util

import lib.view as view
import lib.edit as edit


def main():
    paths = gen_paths()
    cfg = config.Config(paths.source, paths.renames, paths.edits)
    cfg.recent = False
    cfg.testing = False

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


def gen_paths() -> paths.Paths:
    print('enter absolute paths for the following folders')
    source = input('source : ')
    edits = input('edits : ')
    return paths.Paths(
        decompose_path_into_folders(source),
        decompose_path_into_folders(edits),
        decompose_path_into_folders(edits)
    )


def gen_remaining(paths: paths.Paths, recent: bool) -> list[str]:
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
