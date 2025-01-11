import mve.src.constants.error as error
import mve.src.constants.defaults as defaults
import mve.src.constants.treatment_format as treatment_format

import mve.src.helpers.check_and_exit_if as check_and_exit_if
import mve.src.helpers.files as files
import mve.src.helpers.util as util


class VideoPaths:
    '''A helper class to store the video path folders'''

    def __init__(
        self, source: list[str], edits: list[str], renames: list[str]
    ):
        self.source: list[str] = source
        self.edits: list[str] = edits
        self.renames: list[str] = renames

    def verify_paths_integrity(self):
        '''Exit the program if one of the stored paths does not exist.'''
        for folder, desc, code in zip(
            [self.source, self.renames, self.edits],
            ['source', 'renames', 'destination'],
            [error.NO_SOURCE_FOLDER, error.NO_RENAMES_FOLDER,
                error.NO_DESTINATION_FOLDER]
        ):
            check_and_exit_if.no_folder(folder, desc, defaults.BOLD, code)

    def generate_paths_dict(self) -> dict[str, list[str]]:
        '''Generate the JSON dictionary for logging.'''
        return {
            treatment_format.SOURCE_PATH: self.source,
            treatment_format.RENAME_PATH: self.renames,
            treatment_format.DESTINATION_PATH: self.edits
        }

    @staticmethod
    def make_all_paths_from_defaults(source: None | str, edits: None | str,
                                     renames: None | str) -> "VideoPaths":
        VideoPaths.print_prompt([source, edits, renames])
        return VideoPaths(
            files.tokenise_path('source', source),
            files.tokenise_path('destination', edits),
            files.tokenise_path('renames', renames)
        )

    @staticmethod
    def make_merged_dest_from_defaults(source: None | str, dest: None | str,
                                       ) -> "VideoPaths":
        VideoPaths.print_prompt([source, dest])
        output = files.tokenise_path('output', dest)
        return VideoPaths(files.tokenise_path('source', source), output, output)

    @staticmethod
    def print_prompt(args: list[None | str]):
        nones: int = VideoPaths.count_none(args)
        if nones > 0:
            plural = util.plural(nones)
            grammar = 'this' if nones == 1 else 'these'
            print(f'enter the absolute path for {grammar} folder{plural}')

    @staticmethod
    def count_none(args: list[None | str]) -> int:
        return sum(1 if arg is None else 0 for arg in args)
