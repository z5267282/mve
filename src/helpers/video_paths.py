import pathlib


class VideoPaths:
    '''A helper class to store the video path folders'''

    def __init__(
        self, source: list[str], edits: list[str], renames: list[str]
    ):
        self.source: list[str] = source
        self.edits: list[str] = edits
        self.renames: list[str] = renames

    @staticmethod
    def make_paths_from_defaults(source: None | str, edits: None | str,
                                 renames: None | str) -> "VideoPaths":
        if any(folder is None for folder in [source, renames, edits]):
            print('enter these folders')
        return VideoPaths(
            VideoPaths.tokenise_path('source', source),
            VideoPaths.tokenise_path('destination', edits),
            VideoPaths.tokenise_path('renames', renames)
        )

    @staticmethod
    def tokenise_path(display: str, given: None | str) -> list[str]:
        if given is not None:
            return list(
                pathlib.Path(given).parts
            )
        folder = input(f'{display}: ')
        return list(
            pathlib.Path(folder).parts
        )
