# usage: python3 make.py <name of config>
# > source absolute path
# > renames absolute path
# > destination absolute path

# the config name must only contain [a-z-]

# will simply overwrite if config exists already

import json
import os
import re
import sys

import constants.file_structure as fst
import constants.json_settings as jsn

import helpers.files as files
import helpers.util as util

def main():
    args: list[str] = sys.argv[1:]
    if len(args) != 1:
        util.print_error("usage: python3 make.py <name of config>" )
        sys.exit(1)

    config, = args
    if not re.fullmatch(r"[a-z-]+", config):
        util.print_error("config must contain only a-z or - characters")
        sys.exit(2)

    is_current: bool = False
    current_config: str = files.get_joined_path(fst.CONFIGS, fst.CURRENT_CONFIG)
    with open(current_config, "r") as f:
        current: str = json.load(f)
        if current == config:
            is_current = True
    
    contents = make_config_contents()
    config_path: str = fst.CONFIG if is_current \
        else files.get_joined_path(fst.CONFIGS, f"{config}.json")
    with open(config_path, "w") as f:
        print(contents, file=f)
    print(f"wrote {config} to {config_path}")


def stringify_path(display: str) -> str:
    folder = input(f"{display}: ")
    if not os.path.exists(folder):
        util.print_error(f"the {display} folder {folder} doesn't exist")
        sys.exit(3)
    folders: list[str] = os.path.split(folder)
    return json.dumps(folders)


def make_config_contents() -> str:
    print("enter these folders")
    source: str = stringify_path("source")
    renames: str = stringify_path("renames")
    edits: str = stringify_path("destination")

    return f"""SOURCE      = {source}
RENAMES     = {renames}
DESTINATION = {edits} 

# multi threading and processing
NUM_THREADS   = 4
NUM_PROCESSES = 4

# MoviePy
USE_MOVIEPY = False

# testing
TESTING = False

# colours
BOLD = False"""


if __name__ == "__main__":
    main()
