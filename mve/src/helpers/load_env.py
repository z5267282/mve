'''Load information from system environment variables'''

import os
import pathlib

import mve.src.constants.environment as environment


def get_config_paths_from_environment() -> None | list[str]:
    return list(pathlib.Path(raw).parts) \
        if (raw := os.getenv(environment.CONFIGS)
            ) is not None \
        else raw
