class VideoPaths:
    '''A helper class to store the video path folders'''

    def __init__(
        self, source: list[str], edits: list[str], renames: list[str]
    ):
        self.source: list[str] = source
        self.edits: list[str] = edits
        self.renames: list[str] = renames
