import typing
import sys

import constants.error as error
import constants.file_structure as file_structure
import constants.defaults as defaults

import helpers.files as files
import helpers.json_handlers as json_handlers
import helpers.util as util


class Config:
    """The Config class stores settings that change how mve runs.
    We can maintain file system invariants by fatally terminating the
    constructor."""

    def __init__(self, name: str) -> "Config":
        contents = Config.read_config(name)

        # folders
        self.SOURCE: list[str] = Config.expect_paths_list(
            contents, "SOURCE", error.CONFIG_MISSING_SOURCE)
        self.RENAMES: list[str] = Config.expect_paths_list(
            contents, "RENAMES", error.CONFIG_MISSING_RENAMES)
        self.DESTINATION: list[str] = Config.expect_paths_list(
            contents, "DESTINATION", error.CONFIG_MISSING_DESTINATION)

        # multiprocessing
        self.NUM_PROCESSES: int = contents.get(
            "NUM_PROCESSES", defaults.NUM_PROCESSES)
        # moviepy
        self.USE_MOVIEPY: bool = contents.get(
            "USE_MOVIEPY", defaults.USE_MOVIEPY)
        self.MOVIEPY_THREADS: int = contents.get(
            "MOVIEPY_THREADS", defaults.MOVIEPY_THREADS)

        # testing
        self.TESTING: bool = contents.get("TESTING", defaults.TESTING)

        # colours
        self.BOLD: bool = contents.get("BOLD", defaults.BOLD)

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
