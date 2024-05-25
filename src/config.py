import os
import pathlib
import typing
import sys

import constants.defaults as defaults
import constants.error as error
import constants.treatment_format as treatment_format

import helpers.check_and_exit_if as check_and_exit_if
import helpers.files as files
import helpers.json_handlers as json_handlers
import helpers.paths as paths
import helpers.util as util


class Config():
    """The Config class stores settings that change how mve runs.
    We can maintain file system invariants by fatally terminating the
    constructor."""

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

    # folder existence checking
    def no_source_folder(self):
        check_and_exit_if.no_folder(
            self.source, 'source', error.NO_SOURCE_FOLDER)

    # def no_queue(self):
    #     no_folder(self.QUEUE, 'queue', err.NO_QUEUE)

    def one_of_config_folders_missing(self):
        for folder, desc, code in zip(
            [self.source, self.renames, self.destination],
            ['source', 'renames', 'destination'],
            [error.NO_SOURCE_FOLDER, error.NO_RENAMES_FOLDER,
                error.NO_DESTINATION_FOLDER]
        ):
            check_and_exit_if.no_folder(folder, desc, code)

    def create_source_folders(self) -> paths.Paths:
        return paths.paths(self.source, self.destination, self.renames)

    def generate_paths_dict(self) -> dict[str, list[str]]:
        return {
            treatment_format.source_path: self.source,
            treatment_format.rename_path: self.renames,
            treatment_format.destination_path: self.destination
        }


class Stateful():
    # folder constants
    DEFAULT_FOLDER: list[str] = ['..', 'configs']
    ENV_KEY: str = 'MVE_CONFIGS'

    # config files
    CONFIG: str = 'config.json'
    REMAINING: str = 'remaining.json'

    def __init__(self, name: str) -> "Stateful":
        # read config from file
        contents = Stateful.read_config(name)

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
    def locate_configs_folder() -> list[str]:
        configs_folder = list(
            pathlib.Path(
                os.environ[Stateful.ENV_KEY]
            ).parts
        ) if Stateful.ENV_KEY in os.environ \
            else Stateful.DEFAULT_FOLDER

        check_and_exit_if.no_folder(
            configs_folder, 'configs', error.NO_CONFIGS_FOLDER)

        return configs_folder

    @classmethod
    def locate_given_config(name: str) -> list[str]:
        config_folder = Stateful.locate_configs_folder() + [name]

        check_and_exit_if.no_folder(
            config_folder, f'{name} config', error.NO_SUCH_CONFIG
        )

        return config_folder

    @classmethod
    def read_config(name: str) -> dict[str, typing.Any]:
        config_paths = Stateful.locate_given_config(name)
        return json_handlers.read_from_json(
            files.get_joined_path(config_paths, Stateful.CONFIG)
        )

    @classmethod
    def expect_paths_list(
        contents: dict[str, typing.Any], key: str, code: int
    ) -> str:
        if key not in contents:
            util.print_error(f"{contents} not in configuration file")
            sys.exit(code)
        return contents[key]

    # handlers for remaining videos
    # only the Stateful config needs to track the remaining videos as a file

    def join_remaining_path(self) -> str:
        # TODO
        remaining_paths = []
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

    def check_files_remaining(self):
        if self.load_remaining():
            util.stderr_print(
                f"there are files yet to be treated in '{self.join_remaining_path()}'")
            sys.exit(error.FILES_REMAINING)

    def write_remaining(self, remaining: list[str]):
        json_handlers.write_to_json(remaining, self.join_remaining_path())
