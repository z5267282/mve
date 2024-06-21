'''Load all files from the given config's source folder and place them in a
remaning JSON file. Only the base name is stored. If the source folder does not
exist, the program terminates with status error.NO_SOURCE_FOLDER. The generator
checks if there are files yet to be treated and accordingly terminates with
status error.FILES_REMAINING. If remaining JSON file does not exist, it is
created. Files are stored from most recent to least recent. This behaviour can 
be toggled through the RECENT config flag.'''

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

    new_files = files.ls(cfg.source, recent=cfg.recent)
    state.write_remaining(new_files)

    joined_path = files.join_folder(cfg.source)
    util.exit_success(
        'placed file names from the folder \'{}\' in {}'.format(
            colouring.highlight(joined_path),
            state.remaining
        ), cfg.bold
    )


def run_checks(state: config.Stateful):
    state.check_files_remaining()
    state.cfg.no_source_folder()


if __name__ == '__main__':
    main()
