import shutil

from mve.src.config import Stateful

import mve.src.helpers.args as args
import mve.src.helpers.colouring as colouring
import mve.src.helpers.files as files
import mve.src.helpers.util as util

from mve.scripts.script import Legacy
from mve.scripts.script_option import ScriptOption


class Deleter(Legacy):
    def __init__(self):
        super().__init__(str(ScriptOption.DELETER))

    def main(self, argv: list[str]) -> None:
        super().main(argv)

        name = args.expect_config_name(argv)
        state = Stateful(name)
        self.run_checks(state)

        cfg = state.cfg

        files.do_folder_operation(cfg.folders.source, shutil.rmtree)

        util.exit_success('removed the folder \'{}\''.format(
            colouring.highlight_path(cfg.folders.source, cfg.bold)
        ), cfg.bold)

    def run_checks(self, state: Stateful):
        state.check_files_remaining(state.cfg.bold)
