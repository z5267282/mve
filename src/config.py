from json import load
from typing import Any

import constants.file_structure as file_structure

import helpers.files as files


def create_config():
    class Configuration:
        def __init__(self, source: dict[str, Any]) -> "Configuration":
            # folders
            self.SOURCE: list[str] = source["SOURCE"]
            self.RENAMES: list[str] = source["RENAMES"]
            self.DESTINATION: list[str] = source["DESTINATION"]

            # multi threading and processing
            self.NUM_THREADS: int = source.get("NUM_THREADS", 4)
            self.NUM_PROCESSES: int = source.get("NUM_PROCESSES", 4)

            # moviepy
            self.USE_MOVIEPY: bool = source.get("USE_MOVIEPY", False)

            # testing
            self.TESTING: bool = source.get("TESTING", False)

            # colours
            self.BOLD: bool = source.get("BOLD", False)

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

    for folder in ["SOURCE", "RENAMES", "DESTINATION"]:
        if not files.folder_exists(folder):
            print(f"{folder} does not exist")

    return Configuration(config)


cfg = create_config()
