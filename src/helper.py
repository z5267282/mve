import json
import moviepy as mvp
import os

import config as cfg

"""
    FILE RELATED
"""

def get_abs_path(paths_list, file_name):
    paths = paths_list + [file_name]
    return os.path.join(*paths)

def ls(paths_list):
    path = os.path.join(*paths_list)
    return os.listdir(path)

def ls_abs_path(paths_list):
    return [get_abs_path(paths_list, file_name) for file_name in ls(paths_list)]

def get_earliest_file(paths_list):
    files = ls_abs_path(paths_list)
    return sorted(
        files, 
        key=os.path.getctime
    )[0] if files else None

"""
    MOVIEPY
"""

def handle_clip(src_full_path, success_handler, start, end):
    error = None
    with mvp.VideoFileClip(src_full_path) as file:
        try:
            clip = file.subclip(t_start=start, t_end=end)
            success_handler(clip)
        except Exception as e:
            error = str(e)

    return error

"""
    JSON
"""

def write_to_json(item, file_path):
    with open(file_path, 'w') as f:
        json.dump(item, f, indent=cfg.JSON_INDENT)

def load_from_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data
