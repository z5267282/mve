import helpers.files as files
import helpers.util as util


class VideoPaths:
    '''A helper class to store the video path folders'''

    def __init__(
        self, source: list[str], edits: list[str], renames: list[str]
    ):
        self.source: list[str] = source
        self.edits: list[str] = edits
        self.renames: list[str] = renames

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
