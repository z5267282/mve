import os
import sys

import config as cfg
import helper as helper

def files_remaining():
    remaining_file = cfg.REMAINING
    return os.path.exists(remaining_file) and bool(
        helper.load_from_json(remaining_file)
    )

def main():
    if files_remaining():
        print(
            "couldn't generate list of remaining files; there are files left to be edited",
            file=sys.stderr
        )
        sys.exit(1)

    abs_file_names = helper.ls_abs_path(cfg.SOURCE_PATH)
    helper.write_to_json(abs_file_names, cfg.REMAINING)

if __name__ == '__main__':
    main()
