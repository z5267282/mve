import json
import os
import sys

def load_config():
    global CFG_FILE
    cfg = None
    try:
        f = open(CFG_FILE, 'r')
        cfg = json.load(f)
        f.close()
    except FileNotFoundError:
        pass
    
    return cfg

def my_ls(paths_list):
    path = os.path.join(*paths_list)
    return os.listdir(path)

def load_file(file_path):
    data = load_config()
    paths = data[SRC_DIR] + [file_path]
    return os.path.join(*paths)

def get_earliest_file(paths_list):
    files = my_ls(paths_list)
    print(len(files))
    return sorted(files, key=lambda file_path: os.path.getctime(load_file(file_path)), reverse=True)[0] if files else None
