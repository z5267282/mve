'''Load all files from the given config's source folder and place them in a
remaning JSON file. Only the base name is stored. If the source folder does not
exist, the program terminates with status error.NO_SOURCE_FOLDER. The generator
checks if there are files yet to be treated and accordingly terminates with
status error.FILES_REMAINING. If remaining JSON file does not exist, it is
created. Files are stored from most recent to least recent. This behaviour can 
be toggled through the RECENT config flag.'''

import mve.src.config as config

import mve.src.constants.video_editing as video_editing

import mve.src.helpers.args as args
import mve.src.helpers.colouring as colouring
import mve.src.helpers.files as files
import mve.src.helpers.util as util

from mve.scripts.script import Legacy


class Generator(Legacy):
    def main(self, argv: list[str]) -> None:
        super().main(argv)

        name = args.expect_config_name(argv)
        state = config.Stateful(name)
        self.run_checks(state)

        cfg = state.cfg

        new_files = list(
            filter(
                self.good_file, files.ls(cfg.source, recent=cfg.recent)
            )
        )
        state.write_remaining(new_files)

        joined_path = files.join_folder(cfg.source)
        util.exit_success(
            'placed file names from the folder \'{}\' in {}'.format(
                colouring.highlight(joined_path, cfg.bold), state.remaining),
            cfg.bold)

    def run_checks(self, state: config.Stateful):
        state.check_files_remaining()
        state.cfg.no_source_folder()

    def good_file(self, file: str) -> bool:
        # ignore hidden files
        if file.startswith('.'):
            return False

        # convert the name to lowercase for glob suffix comparisons
        # we want case insensitivity here
        lower_name = file.lower()
        return any(lower_name.endswith(suffix) for suffix in video_editing.GLOBS)
