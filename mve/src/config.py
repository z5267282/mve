'''Configure folder paths and settings for a given category of videos.'''

import argparse
import sys
import typing

import mve.src.constants.colours as colours
import mve.src.constants.defaults as defaults
import mve.src.constants.error as error
import mve.src.constants.options as options

import mve.src.helpers.check_and_exit_if as check_and_exit_if
import mve.src.helpers.colouring as colouring
import mve.src.helpers.files as files
import mve.src.helpers.json_handlers as json_handlers
import mve.src.helpers.load_env as load_env
import mve.src.helpers.video_paths as video_paths
import mve.src.helpers.util as util

from mve.scripts.script_option import ScriptOption


class Config():
    '''The Config class stores settings that change how mve runs.
    We can maintain file system invariants by fatally terminating the
    constructor.'''

    ALL_OPTIONS: set[str] = {options.SOURCE, options.RENAMES,
                             options.DESTINATION, options.RECENT,
                             options.NUM_PROCESSES, options.USE_MOVIEPY,
                             options.MOVIEPY_THREADS, options.TESTING,
                             options.BOLD, options.VERIFY_NAME}

    def __init__(
        self,
        folders: video_paths.VideoPaths,
        # options
        recent: bool = defaults.RECENT,
        num_processes: int = defaults.NUM_PROCESSES,
        use_moviepy: bool = defaults.USE_MOVIEPY,
        moviepy_threads: int = defaults.MOVIEPY_THREADS,
        testing: bool = defaults.TESTING,
        bold: bool = defaults.BOLD,
        verify_name: bool = defaults.VERIFY_NAME
    ):
        folders.verify_paths_integrity()
        self.folders: video_paths.VideoPaths = folders

        # file-order generation
        Config.check_bad_config_option_type(recent, True, 'recent', bold)
        self.recent: bool = recent

        # multiprocessing
        Config.check_bad_config_option_type(
            num_processes, False, 'num_processes', bold)
        self.num_processes: int = num_processes

        # moviepy
        Config.check_bad_config_option_type(
            use_moviepy, True, 'use_moviepy', bold)
        self.use_moviepy: bool = use_moviepy
        Config.check_bad_config_option_type(
            moviepy_threads, False, 'moviepy_threads', bold)
        self.moviepy_threads: int = moviepy_threads

        # testing
        Config.check_bad_config_option_type(
            testing, True, 'testing', bold)
        self.testing: bool = testing

        # colours
        Config.check_bad_config_option_type(bold, True, 'bold', bold)
        self.bold: bool = bold

        # double-check name was not mistaken for a command
        Config.check_bad_config_option_type(
            verify_name, True, 'verify_name', bold)
        self.verify_name: bool = verify_name

    def write_config_to_file(self, joined_destination_path: str):
        data = {
            # folders
            options.SOURCE: self.folders.source,
            options.RENAMES: self.folders.renames,
            options.DESTINATION: self.folders.edits,

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
            options.BOLD: self.bold,

            # whether to check if names start with leading numbers
            options.VERIFY_NAME: self.verify_name
        }
        json_handlers.write_to_json(data, joined_destination_path)

    @staticmethod
    def check_bad_config_option_type(variable: typing.Any,
                                     # currently only numbers and booleans are
                                     # supported option types
                                     is_bool: bool,
                                     description: str,
                                     bold: bool) -> typing.NoReturn | None:
        checker = Config.is_bool if is_bool else Config.is_int
        exp_type: type = bool if is_bool else int

        if not checker(variable):
            util.stderr_print(f'incorrect type for configuration option')
            util.print_error(
                "option '{}':".format(
                    colouring.colour_format(
                        colours.PURPLE, description, bold)
                ),
                bold)
            util.print_error(
                "  exp : {}".format(
                    colouring.colour_format(colours.GREEN,
                                            str(exp_type.__name__), bold)
                ),
                bold)
            util.print_error(
                "  got : {}".format(
                    colouring.colour_format(colours.RED,
                                            str(type(variable).__name__), bold)
                ),
                bold)

            sys.exit(error.BAD_TYPE)

    @staticmethod
    def verify_no_unknown_options(
            contents: dict, bold: bool) -> typing.NoReturn | None:

        for opt in contents:
            if not opt in Config.ALL_OPTIONS:
                util.print_error(
                    'unknown configuration option: {} '.format(
                        colouring.colour_format(colours.PURPLE, opt, bold)
                    ),
                    bold)
                sys.exit(error.BAD_CONFIG_OPTION)

    @staticmethod
    def is_bool(variable: typing.Any) -> bool:
        return type(variable) is bool

    @staticmethod
    def is_int(variable: typing.Any) -> bool:
        return type(variable) is int

    @staticmethod
    def add_options_to_parser(parent: argparse.ArgumentParser) -> None:
        options = parent.add_argument_group('configuration options')
        # file-order generation
        options.add_argument('--recent', action='store_true',
                             default=defaults.RECENT,
                             help='store files from most to least recently created')

        # multiprocessing
        options.add_argument('--num-processes', type=int,
                             default=defaults.NUM_PROCESSES,
                             help='set the number of processes used in editing')

        # moviepy
        options.add_argument('--use-moviepy', action='store_true',
                             default=defaults.USE_MOVIEPY,
                             help='use moviepy to edit clips')
        options.add_argument('--moviepy-threads', type=int,
                             default=defaults.MOVIEPY_THREADS,
                             help='use ffmpeg to edit clips')

        # testing
        options.add_argument('--testing', action='store_true',
                             default=defaults.TESTING,
                             help=f'turn on testing mode and do not open videos when the {ScriptOption.VIEWER} plays')

        # colours
        options.add_argument('--bold', action='store_true',
                             default=defaults.BOLD,
                             help='set colouring to bold')

        # double-check name was not mistaken for a command
        options.add_argument('--verify-name', action='store_true',
                             default=defaults.VERIFY_NAME,
                             help='double-check whether a clip name starting with a number is not a timestamp')


class Stateful():
    '''This class maintains file-structure invariants about the configs
    folder. If it can be successfully created, then all necessary files were
    present.'''

    # configs folder location
    DEFAULT_FOLDER: list[str] = ['..', 'configs']

    # base paths

    # folders
    QUEUE = ['queue']
    HISTORY = ['history']
    ERRORS = ['errors']

    # files
    CONFIG: str = 'config.json'
    REMAINING: str = 'remaining.json'

    def __init__(self, name: str):
        config_folder = Stateful.locate_given_config(name)
        queue, history, errors = Stateful.locate_folders(config_folder)
        config_file, remaining = Stateful.locate_files(config_folder)
        contents = json_handlers.read_from_json(config_file, defaults.BOLD)

        Stateful.verify_config_integrity(
            queue, history, errors, config_file, remaining,
            contents.get(options.BOLD, defaults.BOLD)
        )
        cfg = Stateful.make_config_from_file(contents)

        self.queue: list[str] = queue
        self.history: list[str] = history
        self.errors: list[str] = errors

        self.config_file: str = config_file
        self.remaining: str = remaining

        self.cfg: Config = cfg
        self.name: str = name

    @staticmethod
    def locate_configs_folder() -> list[str]:
        configs_folder = env \
            if (env := load_env.get_config_paths_from_environment()
                ) is not None \
            else Stateful.DEFAULT_FOLDER

        check_and_exit_if.no_folder(
            configs_folder, 'configs', defaults.BOLD, error.NO_CONFIGS_FOLDER)

        return configs_folder

    @staticmethod
    def locate_given_config(name: str) -> list[str]:
        config_folder = Stateful.locate_configs_folder() + [name]

        check_and_exit_if.no_folder(config_folder, '{} config'.format(name),
                                    defaults.BOLD, error.NO_SUCH_CONFIG)

        return config_folder

    @staticmethod
    def locate_folders(
            config_folder: list[str]) -> tuple[list[str], list[str], list[str]]:
        queue = config_folder + Stateful.QUEUE
        history = config_folder + Stateful.HISTORY
        errors = config_folder + Stateful.ERRORS

        return queue, history, errors

    @staticmethod
    def locate_files(config_folder: list[str]) -> tuple[str, str]:
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
        check_and_exit_if.no_folder(queue, 'queue', bold, error.NO_QUEUE)
        check_and_exit_if.no_folder(
            history, 'history', bold, error.NO_HISTORY_FOLDER)
        check_and_exit_if.no_folder(errors, 'errors', bold,
                                    error.NO_ERRORS_FOLDER)

        # files
        check_and_exit_if.no_file(
            config_file, 'config file', error.NO_CONFIG_FILE, bold)
        check_and_exit_if.no_file(remaining, 'remaining videos file',
                                  error.NO_CONFIG_REMAINING, bold)

    @staticmethod
    def make_config_from_file(contents: dict) -> Config:
        # folders
        source: list[str] = Stateful.expect_paths_list(
            contents, options.SOURCE, error.CONFIG_MISSING_SOURCE,
            defaults.BOLD)
        renames: list[str] = Stateful.expect_paths_list(
            contents, options.RENAMES, error.CONFIG_MISSING_RENAMES,
            defaults.BOLD)
        destination: list[str] = Stateful.expect_paths_list(
            contents, options.DESTINATION, error.CONFIG_MISSING_DESTINATION,
            defaults.BOLD)
        folders = video_paths.VideoPaths(source, destination, renames)

        Config.verify_no_unknown_options(contents, defaults.BOLD)
        opts = Stateful.populate_config_kwargs_from_contents(contents)

        return Config(folders, **opts)

    @staticmethod
    def populate_config_kwargs_from_contents(contents: dict) -> dict:
        opts = {}

        # no nicer way to conditionally set keys, avoiding None setting
        # maybe an advanced technique using .update and filtering empty dicts?

        # multiprocessing
        if options.NUM_PROCESSES in contents:
            opts['num_processes'] = contents[options.NUM_PROCESSES]

        # file-order generation
        if options.RECENT in contents:
            opts['recent'] = contents[options.RECENT]

        # multiprocessing
        if options.NUM_PROCESSES in contents:
            opts['num_processes'] = contents[options.NUM_PROCESSES]

        # moviepy
        if options.USE_MOVIEPY in contents:
            opts['use_moviepy'] = contents[options.USE_MOVIEPY]
        if options.MOVIEPY_THREADS in contents:
            opts['moviepy_threads'] = contents[options.MOVIEPY_THREADS]

        # testing
        if options.TESTING in contents:
            opts['testing'] = contents[options.TESTING]

        # colours
        if options.BOLD in contents:
            opts['bold'] = contents[options.BOLD]

        # double-check name was not mistaken for a command
        if options.VERIFY_NAME in contents:
            opts['verify_name'] = contents[options.VERIFY_NAME]

        return opts

    @staticmethod
    def expect_paths_list(contents: dict, key: str, code: int,
                          bold: bool) -> list[str]:
        if key not in contents:
            util.print_error(f'{contents} not in configuration file', bold)
            sys.exit(code)
        return contents[key]

    # handlers for remaining videos

    def load_remaining(self, bold: bool) -> list[str]:
        return json_handlers.read_from_json(self.remaining, bold)

    def check_files_remaining(self, bold: bool):
        if self.load_remaining(bold):
            util.stderr_print(
                f'there are files yet to be treated in \'{self.remaining}\''
            )
            sys.exit(error.FILES_REMAINING)

    def write_remaining(self, remaining: list[str]):
        json_handlers.write_to_json(remaining, self.remaining)
