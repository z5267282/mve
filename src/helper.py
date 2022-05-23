import json
import os
import sys

import config as cfg

def my_ls(paths_list):
    print(paths_list)
    print('fish')
    path = os.path.join(*paths_list)
    return os.listdir(path)

def load_file(file_path):
    paths = cfg.SOURCE_PATH + [file_path]
    return os.path.join(*paths)

def get_earliest_file(paths_list):
    files = my_ls(paths_list)
    print(len(files))
    return sorted(
        files, 
        key=lambda file_path: os.path.getctime(load_file(file_path)), 
        reverse=True
    )[0] if files else None

print(get_earliest_file(my_ls(cfg.SOURCE_PATH)))
