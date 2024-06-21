'''Configure folder paths and settings for a given category of videos.'''

import os
import pathlib
import typing
import sys

import constants.defaults as defaults
import constants.error as error
import constants.options as options
import constants.treatment_format as treatment_format

import helpers.check_and_exit_if as check_and_exit_if
import helpers.files as files
import helpers.json_handlers as json_handlers
import helpers.video_paths as video_paths
import helpers.util as util


class Config():
    '''The Config class stores settings that change how mve runs.
    We can maintain file system invariants by fatally terminating the
    constructor.'''

    def __init__(
        self,
        # folders
        source: list[str], renames: list[str], destination: list[str],
        # options
        recent: bool = defaults.RECENT,
        num_processes: int = defaults.NUM_PROCESSES,
        use_moviepy: bool = defaults.USE_MOVIEPY,
        moviepy_threads: int = defaults.MOVIEPY_THREADS,
        testing: bool = defaults.TESTING,
        bold: bool = defaults.BOLD
    ):
        # folders
        self.source: list[str] = source
        self.renames: list[str] = renames
        self.destination: list[str] = destination

        # file-order generation
        self.recent: bool = recent

        # multiprocessing
        self.num_processes: int = num_processes

        # moviepy
        self.use_moviepy: bool = use_moviepy

        self.moviepy_threads: int = moviepy_threads

        # testing
        self.testing: bool = testing

        # colours
        self.bold: bool = bold

    # folder existence checking

    def no_source_folder(self):
        check_and_exit_if.no_folder(
            self.source, 'source', error.NO_SOURCE_FOLDER)

    def one_of_config_folders_missing(self):
        for folder, desc, code in zip(
            [self.source, self.renames, self.destination],
            ['source', 'renames', 'destination'],
            [error.NO_SOURCE_FOLDER, error.NO_RENAMES_FOLDER,
                error.NO_DESTINATION_FOLDER]
        ):
            check_and_exit_if.no_folder(folder, desc, code)

    def create_source_folders(self) -> video_paths.VideoPaths:
        return video_paths.VideoPaths(
            self.source, self.destination, self.renames)

    def generate_paths_dict(self) -> dict[str, list[str]]:
        return {
            treatment_format.SOURCE_PATH: self.source,
            treatment_format.RENAME_PATH: self.renames,
            treatment_format.DESTINATION_PATH: self.destination
        }

    def write_config_to_file(self, joined_destination_path: str):
        data = {
            # folders
            options.SOURCE: self.source,
            options.RENAMES: self.renames,
            options.DESTINATION: self.destination,

            # file-order generation
            options.RECENT: self.recent,

            # multiprocessing
            options.NUM_PROCESSES: self.num_processes,

            # moviepy
            options.USE_MOVIEPY: self.use_moviepy,
            options.MOVIEPY_THREADS: self.moviepy_threads,

            # testing
            options.TESTING: self.testing,

            # colours
            options.BOLD: self.bold
        }
        json_handlers.write_to_json(data, joined_destination_path)


class Stateful():
    '''This class maintains file-structure invariants about the configs
    folder. If it can be successfully created, then all necessary files were
    present.'''

    # configs folder location
    DEFAULT_FOLDER: list[str] = ['..', 'configs']
    ENV_KEY: str = 'MVE_CONFIGS'

    # base paths

    # folders
    QUEUE = ['queue']
    HISTORY = ['history']
    ERRORS = ['errors']

    # files
    CONFIG: str = 'config.json'
    REMAINING: str = 'remaining.json'

    def __init__(self, name: str):
        queue, history, errors = Stateful.locate_folders(name)
        config_file, remaining = Stateful.locate_files(name)

        Stateful.verify_config_integrity(
            queue, history, errors, config_file, remaining,
            contents.get(options.BOLD, defaults.BOLD)
        )

        contents = json_handlers.read_from_json(config_file)
        cfg = Stateful.make_config_from_file(
            contents, contents.get(options.BOLD, defaults.BOLD)
        )

        self.queue: list[str] = queue
        self.history: list[str] = history
        self.errors: list[str] = errors

        self.config_file: str = config_file
        self.remaining: str = remaining

        self.cfg: Config = cfg
        self.name: str = name

    @staticmethod
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

    @staticmethod
    def locate_given_config(name: str) -> list[str]:
        config_folder = Stateful.locate_configs_folder() + [name]

        check_and_exit_if.no_folder(
            config_folder, f'{name} config', error.NO_SUCH_CONFIG
        )

        return config_folder

    @staticmethod
    def locate_folders(name: str) -> tuple[list[str], list[str], list[str]]:
        config_folder = Stateful.locate_given_config(name)

        queue = config_folder + Stateful.QUEUE
        history = config_folder + Stateful.HISTORY
        errors = config_folder + Stateful.ERRORS

        return queue, history, errors

    @staticmethod
    def locate_files(name: str) -> tuple[str, str]:
        config_folder = Stateful.locate_given_config(name)

        config_file = files.get_joined_path(config_folder, Stateful.CONFIG)
        remaining = files.get_joined_path(config_folder, Stateful.REMAINING)

        return config_file, remaining

    @staticmethod
    def verify_config_integrity(
        queue: list[str], history: list[str], errors: list[str],
        config_file: str, remaining: str, bold: bool
    ):
        '''Verify the given config has all the correct files'''
        # folders
        check_and_exit_if.no_folder(queue, 'queue', error.NO_QUEUE)
        check_and_exit_if.no_folder(
            history, 'history', error.NO_HISTORY_FOLDER)
        check_and_exit_if.no_folder(errors, 'errors', error.NO_ERRORS_FOLDER)

        # files
        check_and_exit_if.no_file(
            config_file, 'config file', error.NO_CONFIG_FILE, bold)
        check_and_exit_if.no_file(remaining, 'remaining videos file',
                                  error.NO_CONFIG_REMAINING, bold)

    @staticmethod
    def make_config_from_file(
            contents: dict[str, typing.Any], bold: bool) -> Config:
        # folders
        source: list[str] = Stateful.expect_paths_list(
            contents, options.SOURCE, error.CONFIG_MISSING_SOURCE, bold)
        renames: list[str] = Stateful.expect_paths_list(
            contents, options.RENAMES, error.CONFIG_MISSING_RENAMES, bold)
        destination: list[str] = Stateful.expect_paths_list(
            contents, options.DESTINATION, error.CONFIG_MISSING_DESTINATION,
            bold)

        # file-order generation
        recent = contents.get(options.RECENT, defaults.RECENT)

        # multiprocessing
        num_processes: int = contents.get(
            options.NUM_PROCESSES, defaults.NUM_PROCESSES)
        # moviepy
        use_moviepy: bool = contents.get(
            options.USE_MOVIEPY, defaults.USE_MOVIEPY)
        moviepy_threads: int = contents.get(
            options.MOVIEPY_THREADS, defaults.MOVIEPY_THREADS)

        # testing
        testing: bool = contents.get(options.TESTING, defaults.TESTING)

        # colours
        bold: bool = contents.get(options.BOLD, defaults.BOLD)

        return Config(
            # folders
            source, renames, destination,
            # options
            recent,
            num_processes,
            use_moviepy, moviepy_threads,
            testing,
            bold
        )

    @staticmethod
    def expect_paths_list(contents: dict[str, typing.Any], key: str, code: int,
                          bold: bool) -> str:
        if key not in contents:
            util.print_error(f'{contents} not in configuration file', bold)
            sys.exit(code)
        return contents[key]

    # handlers for remaining videos

    def load_remaining(self) -> list[str]:
        return json_handlers.read_from_json(self.remaining)

    def check_files_remaining(self):
        if self.load_remaining():
            util.stderr_print(
                f'there are files yet to be treated in \'{self.remaining}\''
            )
            sys.exit(error.FILES_REMAINING)

    def write_remaining(self, remaining: list[str]):
        json_handlers.write_to_json(remaining, self.remaining)
