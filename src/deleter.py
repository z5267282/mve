'''Delete the source folder for the given config once all remaining files have
been processed. It is not intended to be run when inside a Docker container
as the source folder will be mounted as a volume.'''

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
    run_checks(state)

    cfg = state.cfg

    files.do_folder_operation(cfg.source, shutil.rmtree)

    util.exit_success('removed the folder \'{}\''.format(
        colouring.highlight_path(cfg.source, cfg.bold)
    ), cfg.bold)


def run_checks(state: config.Stateful):
    state.check_files_remaining()
    state.cfg.no_source_folder()


if __name__ == '__main__':
    main()
