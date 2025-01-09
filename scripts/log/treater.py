'''Edit all videos according to the first enqueued treatment of the given
config. The treatments are performed in the following order: edits, renames and
deletions. Edits are placed in the given config's destination folder. Once the
enqueued treatment has been processed, it is moved into the history of the
given config. Errors if any, are logged in the given config's errors folder.
When an error occurs, the file name of the offending treatment is appended to
the remaining JSON file. After it has been rewatched in the viewer, it can also
be re-treated upon the next viewing session. The program prematurely terminates
if any of the aformentioned folders do not exist.'''

import os
import sys

import src.config as config

import src.constants.error as error
import src.constants.errors_format as errors_format

import src.helpers.args as args
import src.helpers.colouring as colouring
import src.helpers.files as files
import src.helpers.json_handlers as json_handlers
import src.helpers.timestamps as timestamps
import src.helpers.util as util

import lib.edit as edit


def main():
    name = args.expect_config_name(sys.argv)
    state = config.Stateful(name)
    run_checks(state)

    cfg = state.cfg

    remaining, errors = state.load_remaining(), list()
    current_file = dequeue(state)
    joined_current_file = files.get_joined_path(state.queue, current_file)
    data = json_handlers.read_from_json(joined_current_file)
    folders = cfg.create_source_folders()

    edit.treat_all(
        data,
        cfg.use_moviepy, cfg.moviepy_threads,
        cfg.num_processes,
        remaining, errors, folders
    )
    update_history(state, current_file, joined_current_file)

    if errors:
        paths_dict = cfg.generate_paths_dict()
        handle_errors(state, remaining, errors, paths_dict, cfg.bold)

    util.exit_treat_all_good(cfg.bold)


def run_checks(state: config.Stateful):
    check_empty_queue(state)
    state.cfg.one_of_config_folders_missing()


def check_empty_queue(state: config.Stateful):
    if not files.ls(state.queue):
        print(f'there are no files queued in folder \'{state.queue}\'')
        sys.exit(error.EMPTY_QUEUE)


def dequeue(state: config.Stateful):
    queue_files = files.ls(state.queue, recent=True)
    return queue_files[0]


def update_history(
    state: config.Stateful, current_file: str, joined_current_file: str
):
    joined_history_file = files.get_joined_path(state.history, current_file)
    os.rename(joined_current_file, joined_history_file)


def handle_errors(state: config.Stateful, remaining: list[str],
                  errors: list[dict], paths_dict: dict[str, list[str]],
                  bold: bool):
    error_file_name = timestamps.generate_timestamped_file_name()
    write_errors(state, error_file_name, errors, paths_dict)
    state.write_remaining(remaining)
    exit_treatment_error(error_file_name, bold)


def write_errors(
    state: config.Stateful,
    error_file_name: str, errors: list[dict], paths_dict: dict[str, list[str]]
):
    joined_error_file_name = files.get_joined_path(
        state.errors, error_file_name)
    data = {
        errors_format.ERRORS_VIDEOS: errors,
        errors_format.ERRORS_PATHS: paths_dict
    }
    json_handlers.write_to_json(data, joined_error_file_name)


def exit_treatment_error(error_file_name: str, bold: bool):
    util.print_error(
        'one or more errors occurred during treatment logged in \'{}\''.format(
            colouring.highlight(error_file_name, bold)
        ), bold
    )
    sys.exit(error.TREATMENT_ERROR)


if __name__ == '__main__':
    main()
