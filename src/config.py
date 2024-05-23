import abc
import typing
import sys

import constants.defaults as defaults
import constants.error as error
import constants.file_structure as file_structure
import constants.treatment_format as treatment_format

import helpers.check_and_exit_if as check_and_exit_if
import helpers.files as files
import helpers.json_handlers as json_handlers
import helpers.paths as paths
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
        self.source: list[str] = source
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

    def create_source_folders(self) -> paths.Paths:
        return paths.paths(self.source, self.destination, self.renames)

    def generate_paths_dict(self) -> dict[str, list[str]]:
        return {
            treatment_format.source_path: self.source,
            treatment_format.rename_path: self.renames,
            treatment_format.destination_path: self.destination
        }


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
            # folders
            source, renames, destination,
            # options
            recent,
            num_processes,
            use_moviepy, moviepy_threads,
            testing,
            bold
        )
        self.name = name

    @classmethod
    # TODO: clean this up
    # print out full path not folder path list
    def read_config(name: str) -> dict[str, typing.Any]:
        config_paths = Stateful.get_config_paths(name)
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
    def get_config_paths(name: str) -> list[str]:
        return file_structure.CONFIGS + [name]

    @classmethod
    def expect_paths_list(contents: dict[str, typing.Any], key: str, code: int) -> str:
        if key not in contents:
            util.print_error(f"{contents} not in configuration file")
            sys.exit(code)
        return contents[key]

    # handlers for remaining videos
    # only the Stateful config needs to track the remaining videos as a file

    def join_remaining_path(self) -> str:
        remaining_paths = file_structure.make_history_paths(
            [self.name] + file_structure.REMAINING
        )
        return files.join_folder(remaining_paths)

    def check_no_remaining(self):
        '''This function should be called before any file changes relating to
        remaining are processed. We don't want to run the entire program, crash
        and then lose all work. Making this a self method maintains the
        invariant that the config folder existed.'''
        check_and_exit_if.no_file(
            self.join_remaining_path(), 'remaining', error.MISSING_REMAINING)

    def load_remaining(self) -> list[str]:
        return json_handlers.read_from_json(
            self.join_remaining_path()
        )

    def write_remaining(self, remaining: list[str]):
        json_handlers.write_to_json(remaining, self.join_remaining_path())


class Stateless(Config):
    def __init__(
        self,
        # folders
        source: list[str], renames: list[str], destination: list[str]
    ):
        super().__init__(
            # folders
            source, renames, destination,
            # options
            recent=defaults.RECENT,
            num_processes=defaults.num_processes,
            use_moviepy=defaults.USE_MOVIEPY, moviepy_threads=defaults.MOVIEPY_THREADS,
            testing=defaults.TESTING,
            bold=defaults.BOLD
        )
