'''Edit all videos according to the first enqueued treatment of the given
config. The treatments are performed in the following order: edits, renames and
deletions. Edits are placed in the given config's destination folder. Once the
enqueued treatment has been processed, it is moved into the history of the
given config. Errors if any, are logged in the given config's errors folder.
When an error occurs, the file name of the offending treatment is appended to
the remaining JSON file. After it has been rewatched in the viewer, it can also
be re-treated upon the next viewing session. The program prematurely terminates
if any of the aformentioned folders do not exist.'''

import os
import sys

from mve.src.config import Stateful

import mve.src.constants.colours as colours
import mve.src.constants.error as error
import mve.src.constants.errors_format as errors_format

import mve.src.helpers.args as args
import mve.src.helpers.colouring as colouring
import mve.src.helpers.files as files
import mve.src.helpers.json_handlers as json_handlers
import mve.src.helpers.timestamps as timestamps
import mve.src.helpers.util as util

import mve.src.lib.edit as edit

from mve.scripts.script import Legacy
from mve.scripts.script_option import ScriptOption


class Treater(Legacy):
    def __init__(self):
        super().__init__(str(ScriptOption.TREATER))

    def main(self, argv: list[str]) -> None:
        super().main(argv)

        name = args.expect_config_name(argv)
        state = Stateful(name)
        self.run_checks(state)

        cfg = state.cfg

        remaining, errors = state.load_remaining(cfg.bold), list()
        current_file = self.dequeue(state)
        joined_current_file = files.get_joined_path(state.queue, current_file)
        data = json_handlers.read_from_json(joined_current_file, cfg.bold)
        folders = cfg.folders

        edit.treat_all(
            data,
            cfg.use_moviepy, cfg.moviepy_threads,
            cfg.num_processes,
            remaining, errors, folders
        )
        self.update_history(state, current_file, joined_current_file)

        if errors:
            paths_dict = cfg.folders.generate_paths_dict()
            self.handle_errors(state, remaining, errors, paths_dict, cfg.bold)

        self.remind_to_run_deleter(remaining, state)

        util.exit_treat_all_good(cfg.bold)

    def run_checks(self, state: Stateful):
        self.check_empty_queue(state)

    def check_empty_queue(self, state: Stateful):
        if not files.ls(state.queue):
            print(f'there are no files queued in folder \'{state.queue}\'')
            sys.exit(error.EMPTY_QUEUE)

    def dequeue(self, state: Stateful):
        queue_files = files.ls(state.queue, recent=True)
        return queue_files[0]

    def update_history(self,
                       state: Stateful, current_file: str,
                       joined_current_file: str):
        joined_history_file = files.get_joined_path(
            state.history, current_file)
        os.rename(joined_current_file, joined_history_file)

    def handle_errors(self, state: Stateful, remaining: list[str],
                      errors: list[dict], paths_dict: dict[str, list[str]],
                      bold: bool):
        error_file_name = timestamps.generate_timestamped_file_name()
        self.write_errors(state, error_file_name, errors, paths_dict)
        state.write_remaining(remaining)
        self.exit_treatment_error(error_file_name, bold)

    def write_errors(self, state: Stateful, error_file_name: str,
                     errors: list[dict], paths_dict: dict[str, list[str]]
                     ):
        joined_error_file_name = files.get_joined_path(
            state.errors, error_file_name)
        data = {
            errors_format.ERRORS_VIDEOS: errors,
            errors_format.ERRORS_PATHS: paths_dict
        }
        json_handlers.write_to_json(data, joined_error_file_name)

    def exit_treatment_error(self, error_file_name: str, bold: bool):
        util.print_error(
            'one or more errors occurred during treatment logged in \'{}\''.format(
                colouring.highlight(error_file_name, bold)
            ), bold
        )
        sys.exit(error.TREATMENT_ERROR)

    def remind_to_run_deleter(self, remaining: list[str],
                              state: Stateful) -> None:
        if not remaining and not files.ls(state.queue):
            reminder = colouring.colour_box(colours.YELLOW, 'reminder',
                                            state.cfg.bold)
            print('{} - there are no more remaining files to be viewed and the last treatment has been run, so {} should be run'.
                  format(reminder,
                         colouring.highlight(
                             str(ScriptOption.DELETER), state.cfg.bold)
                         )
                  )
