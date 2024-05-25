import os
import moviepy.editor as mvp
import sys

import config

import constants.error as error
import constants.errors_format as errors_format

import helpers.args as args
import helpers.colouring as colouring
import helpers.files as files
import helpers.json_handlers as json_handlers
import helpers.timestamps as timestamps
import helpers.util as util

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
        paths_dict = state.generate_paths_dict()
        handle_errors(state, remaining, errors, paths_dict)

    util.exit_treat_all_good()


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


def handle_errors(
    state: config.Stateful,
    remaining: list[str], errors: list[dict], paths_dict: dict[str, list[str]]
):
    error_file_name = timestamps.generate_timestamped_file_name()
    write_errors(error_file_name, errors, paths_dict)
    state.write_remaining(remaining)
    exit_treatment_error(error_file_name)


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


def exit_treatment_error(error_file_name):
    util.print_error(
        'one or more errors occurred during treatment logged in \'{}\''.format(
            colouring.highlight(error_file_name)
        )
    )
    sys.exit(error.TREATMENT_ERROR)


if __name__ == '__main__':
    main()
