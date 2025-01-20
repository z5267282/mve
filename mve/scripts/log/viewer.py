'''Sequentially view all remaining files in the given config. Each remaining 
video is played based on the operating system, with the editing command entered
afterwards. If the script is run on Mac or Windows, the native OS video player
will be used to open videos. It is assumed that a Linux environment corresponds
to a Docker container. In this case, the videos are played on a browser that is
hosted by the container. The viewer will prematurely terminate if there are no
remaining files, or the source folder for the given config does not exist.
Once complete, the viewer enques a new treatment for the given config.'''

from mve.src.config import Stateful

import mve.src.constants.treatment_format as treatment_format

import mve.src.helpers.args as args
import mve.src.helpers.util as util
import mve.src.helpers.timestamps as timestamps
import mve.src.helpers.json_handlers as json_handlers
import mve.src.helpers.files as files

import mve.src.lib.view as view

from mve.scripts.script import Legacy
from mve.scripts.script_option import ScriptOption


class Viewer(Legacy):
    def __init__(self):
        super().__init__(str(ScriptOption.VIEWER))

    def main(self, argv: list[str]) -> None:
        super().main(argv)

        name = args.expect_config_name(argv)
        state = Stateful(name)

        cfg = state.cfg

        remaining = state.load_remaining(cfg.bold)
        edits, renames, deletions = list(), dict(), list()
        folders = cfg.folders
        view.run_loop(
            remaining, edits, renames, deletions, folders, cfg.testing, cfg.bold,
            cfg.verify_name)
        state.write_remaining(remaining)

        if edits or renames or deletions:
            paths_dict = cfg.folders.generate_paths_dict()
            self.log_to_file(state, edits, renames, deletions, paths_dict)

        util.exit_success(
            util.format_remaining(len(remaining), cfg.bold), cfg.bold)

    def log_to_file(self, state: Stateful, edits: list[dict],
                    renames: dict[str, str], deletions: list[str],
                    paths_dict: dict[str, list[str]]):
        treatment_name = timestamps.generate_timestamped_file_name()
        joined_treatment_name = files.get_joined_path(
            state.queue, treatment_name)
        data = view.wrap_session(edits, renames, deletions)
        data[treatment_format.PATHS] = paths_dict
        json_handlers.write_to_json(data, joined_treatment_name)
