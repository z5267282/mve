import sys

import config

import helpers.args as args
import helpers.colours as colours
import helpers.files as files
import helpers.util as util


def main():
    name = args.expect_config_name(sys.argv)
    state = config.Stateful(name)
    run_checks(state.cfg)

    cfg = state.cfg

    new_files = files.ls(cfg.source, recent=cfg.recent)
    state.write_remaining(new_files)

    joined_path = files.join_folder(cfg.source)
    util.exit_success(
        "placed file names from the folder '{}' in {}".format(
            colours.highlight(joined_path),
            files.get_joined_path(state.remaining)
        )
    )


def run_checks(state: config.Stateful):
    state.check_files_remaining()
    state.cfg.no_source_folder()


if __name__ == '__main__':
    main()
