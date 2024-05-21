from json import load
from typing import Any
import sys

import constants.error as error
import constants.file_structure as file_structure
import constants.defaults as defaults

import helpers.files as files
import helpers.util as util


def create_config():
    def expect_paths_list(contents: dict[str, Any], key: str, code: int) -> str:
        if key not in contents:
            util.print_error(f"{contents} not in configuration file")
            sys.exit(code)
        return contents[key]

    class Configuration:
        def __init__(self, contents: dict[str, Any]) -> "Configuration":
            # folders
            self.SOURCE: list[str] = expect_paths_list(
                contents, "SOURCE", error.CONFIG_MISSING_SOURCE)
            self.RENAMES: list[str] = expect_paths_list(
                contents, "RENAMES", error.CONFIG_MISSING_RENAMES
            )
            self.DESTINATION: list[str] = expect_paths_list(
                contents, "DESTINATION", error.CONFIG_MISSING_DESTINATION
            )

            # multi threading and processing
            self.NUM_THREADS: int = contents.get(
                "NUM_THREADS", defaults.NUM_THREADS)
            self.NUM_PROCESSES: int = contents.get(
                "NUM_PROCESSES", defaults.NUM_PROCESSES)

            # moviepy
            self.USE_MOVIEPY: bool = contents.get(
                "USE_MOVIEPY", defaults.USE_MOVIEPY)

            # testing
            self.TESTING: bool = contents.get("TESTING", defaults.TESTING)

            # colours
            self.BOLD: bool = contents.get("BOLD", defaults.BOLD)

    current_path: str = files.get_joined_path(
        file_structure.CONFIGS, "current.json")
    try:
        with open(current_path, "r") as f:
            current = load(f)
    except FileNotFoundError:
        print(
            f"could not load the current config - {current_path} does not exist")

    config_path = files.get_joined_path(
        file_structure.CONFIGS, f"{current}.json")
    try:
        with open(config_path, "r") as f:
            config = load(f)
    except FileNotFoundError:
        print(
            f"the current config does not have a corresponding file {config_path}")

    return Configuration(config)


cfg = create_config()
