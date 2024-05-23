import abc
import typing
import sys

import constants.error as error
import constants.file_structure as file_structure
import constants.defaults as defaults

import helpers.files as files
import helpers.json_handlers as json_handlers
import helpers.util as util


class Config(abc.ABC):
    """The Config class stores settings that change how mve runs.
    We can maintain file system invariants by fatally terminating the
    constructor."""

    @abc.abstractmethod
    def __init__(
        self,
        # folders
        source: list[str], renames: list[str], destination: list[str],
        # options
        recent: bool,
        num_processes: int,
        use_moviepy: bool, moviepy_threads: int,
        testing: bool,
        bold: bool
    ) -> "Config":
        # folders
        self.renames: list[str] = renames
        self.destination: list[str] = destination

        # file-order generation
        self.recent = recent

        # multiprocessing
        self.num_processes: int = num_processes

        # moviepy
        self.use_moviepy: bool = use_moviepy

        self.moviepy_threads: int = use_moviepy

        # testing
        self.testing: bool = testing

        # colours
        self.bold: bool = bold


class Stateful(Config):
    def __init__(self, name: str) -> "Stateful":
        contents = Config.read_config(name)

        # folders
        source: list[str] = Stateful.expect_paths_list(
            contents, "source", error.Stateful_missing_source)
        renames: list[str] = Stateful.expect_paths_list(
            contents, "renames", error.Stateful_missing_renames)
        destination: list[str] = Stateful.expect_paths_list(
            contents, "destination", error.config_missing_destination)

        # file-order generation
        recent = contents.get("recent", defaults.recent)

        # multiprocessing
        num_processes: int = contents.get(
            "num_processes", defaults.num_processes)
        # moviepy
        use_moviepy: bool = contents.get("use_moviepy", defaults.use_moviepy)
        moviepy_threads: int = contents.get(
            "moviepy_threads", defaults.moviepy_threads)

        # testing
        testing: bool = contents.get("testing", defaults.testing)

        # colours

        bold: bool = contents.get("bold", defaults.bold)

        super().__init__(
            source, renames, destination,
            recent, num_processes, recent, moviepy_threads, testing, bold
        )

    @classmethod
    def read_config(name: str) -> dict[str, typing.Any]:
        config_paths = file_structure.CONFIGS + [name]
        if not files.folder_exists(config_paths):
            util.print_error(
                f"config '{name}' does not exist in {file_structure.CONFIGS}"
            )
            sys.exit(87)

        try:
            contents = json_handlers.read_from_json(
                files.get_joined_path(config_paths, file_structure.CONFIG)
            )
        except FileNotFoundError:
            util.print_error(
                f"could not load config '{name}' since {file_structure.CONFIG} could not be opened in {config_paths}"
            )
            sys.exit(87)
        return contents

    @classmethod
    def expect_paths_list(contents: dict[str, typing.Any], key: str, code: int) -> str:
        if key not in contents:
            util.print_error(f"{contents} not in configuration file")
            sys.exit(code)
        return contents[key]


class Stateless(Config):
    def __init__(
        self,
        # folders
        source: list[str], renames: list[str], destination: list[str]
    ):
        super().__init__(
            self,
            # folders
            source, renames, destination,
            # options
            recent=defaults.RECENT,
            num_processes=defaults.num_processes,
            use_moviepy=defaults.USE_MOVIEPY, moviepy_threads=defaults.MOVIEPY_THREADS,
            testing=defaults.TESTING,
            bold=defaults.BOLD
        )
