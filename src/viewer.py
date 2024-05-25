import sys

import config

import constants.treatment_format as treatment_format

import helpers.args as args
import helpers.util as util
import helpers.timestamps as timestamps
import helpers.json_handlers as json_handlers
import helpers.files as files

import lib.view as view


def main():
    name = args.expect_config_name(sys.argv)
    state = config.Stateful(name)
    run_checks(state)

    cfg = state.cfg

    remaining = state.load_remaining()
    edits, renames, deletions = list(), dict(), list()
    folders = cfg.create_source_folders()
    view.run_loop(remaining, edits, renames, deletions, folders)
    state.write_remaining(remaining)

    if edits or renames or deletions:
        paths_dict = cfg.generate_paths_dict()
        log_to_file(state, edits, renames, deletions, paths_dict)

    util.exit_success(
        util.format_remaining(
            len(remaining)
        )
    )


def run_checks(cfg: config.Config):
    cfg.one_of_config_folders_missing()


def log_to_file(state: config.Stateful, edits, renames, deletions, paths_dict: dict[str, list[str]]):
    treatment_name = timestamps.generate_timestamped_file_name()
    joined_treatment_name = files.get_joined_path(state.queue, treatment_name)
    data = view.wrap_session(edits, renames, deletions)
    data[treatment_format.PATHS] = paths_dict
    json_handlers.write_to_json(data, joined_treatment_name)


if __name__ == '__main__':
    main()
