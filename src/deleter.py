import shutil
import sys

import config

import helpers.args as args
import helpers.colouring as colouring
import helpers.files as files
import helpers.util as util


def main():
    name = args.expect_config_name(sys.argv)
    state = config.Stateful(name)
    run_checks(state.cfg)

    cfg = state.cfg

    files.do_folder_operation(cfg.source, shutil.rmtree)

    joined_path = files.join_folder(cfg.source)
    util.exit_success(
        f'removed the folder \'{colouring.highlight(joined_path)}\'')


def run_checks(state: config.Stateful):
    state.check_files_remaining()
    state.cfg.no_source_folder()


if __name__ == '__main__':
    main()
