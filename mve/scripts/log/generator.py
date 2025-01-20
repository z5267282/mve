from mve.src.config import Stateful

import mve.src.constants.video_editing as video_editing

import mve.src.helpers.args as args
import mve.src.helpers.colouring as colouring
import mve.src.helpers.files as files
import mve.src.helpers.util as util

from mve.scripts.script import Legacy
from mve.scripts.script_option import ScriptOption


class Generator(Legacy):
    def __init__(self):
        super().__init__(str(ScriptOption.GENERATOR))

    def main(self, argv: list[str]) -> None:
        super().main(argv)

        name = args.expect_config_name(argv)
        state = Stateful(name)
        self.run_checks(state)

        cfg = state.cfg

        new_files = list(
            filter(
                self.good_file, files.ls(cfg.folders.source, recent=cfg.recent)
            )
        )
        state.write_remaining(new_files)

        joined_path = files.join_folder(cfg.folders.source)
        util.exit_success(
            'placed file names from the folder \'{}\' in {}'.format(
                colouring.highlight(joined_path, cfg.bold), state.remaining),
            cfg.bold)

    def run_checks(self, state: Stateful):
        state.check_files_remaining(state.cfg.bold)

    def good_file(self, file: str) -> bool:
        # ignore hidden files
        if file.startswith('.'):
            return False

        # convert the name to lowercase for glob suffix comparisons
        # we want case insensitivity here
        lower_name = file.lower()
        return any(lower_name.endswith(suffix) for suffix in video_editing.GLOBS)
