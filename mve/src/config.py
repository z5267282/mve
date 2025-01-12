'''Configure folder paths and settings for a given category of videos.'''

import argparse
import sys

import mve.src.constants.defaults as defaults
import mve.src.constants.error as error
import mve.src.constants.options as options

import mve.src.helpers.check_and_exit_if as check_and_exit_if
import mve.src.helpers.files as files
import mve.src.helpers.json_handlers as json_handlers
import mve.src.helpers.load_env as load_env
import mve.src.helpers.video_paths as video_paths
import mve.src.helpers.util as util


class Config():
    '''The Config class stores settings that change how mve runs.
    We can maintain file system invariants by fatally terminating the
    constructor.'''

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

        # double-check name was not mistaken for a command
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
            options.BOLD: self.bold
        }
        json_handlers.write_to_json(data, joined_destination_path)

    @staticmethod
    def create_options_dict_from_args(opt_argv: list[str]) -> dict:
        '''Note that all flags will be converted into snake_case by
        argparse.'''
        # the parent Script should have --help enabled
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument('--list-options', action='help')

        # file-order generation
        parser.add_argument('--recent', action='store_true',
                            default=defaults.RECENT)

        # multiprocessing
        parser.add_argument('--num-processes', type=int,
                            default=defaults.NUM_PROCESSES)

        # moviepy
        parser.add_argument('--use-moviepy', action='store_true',
                            default=defaults.USE_MOVIEPY)
        parser.add_argument('--moviepy-threads', type=int,
                            default=defaults.MOVIEPY_THREADS)

        # testing
        parser.add_argument('--testing', action='store_true',
                            default=defaults.TESTING)

        # colours
        parser.add_argument('--bold', action='store_true',
                            default=defaults.BOLD)

        # double-check name was not mistaken for a command
        parser.add_argument('--verify-name', action='store_true',
                            default=defaults.VERIFY_NAME)

        opts = parser.parse_args(opt_argv)
        # make a deep copy of the dictionary-converted Namespace
        # https://docs.python.org/3/library/argparse.html#the-namespace-object
        return {k: v for k, v in vars(opts).items()}


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
        contents = json_handlers.read_from_json(config_file)

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
    def locate_folders(config_folder: list[str]) -> tuple[list[str], list[str], list[str]]:
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
