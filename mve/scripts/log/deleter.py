'''Delete the source folder for the given config once all remaining files have
been processed. It is not intended to be run when inside a Docker container
as the source folder will be mounted as a volume.'''

import shutil

import mve.src.config as config

import mve.src.helpers.args as args
import mve.src.helpers.colouring as colouring
import mve.src.helpers.files as files
import mve.src.helpers.util as util

from mve.scripts.script import Legacy


class Deleter(Legacy):
    def main(self, argv: list[str]) -> None:
        super().main(argv)

        name = args.expect_config_name(argv)
        state = config.Stateful(name)
        self.run_checks(state)

        cfg = state.cfg

        files.do_folder_operation(cfg.source, shutil.rmtree)

        util.exit_success('removed the folder \'{}\''.format(
            colouring.highlight_path(cfg.source, cfg.bold)
        ), cfg.bold)

    def run_checks(self, state: config.Stateful):
        state.check_files_remaining()
        state.cfg.no_source_folder()
