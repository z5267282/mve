import moviepy as mvp
import os

import config as cfg

"""
    FILE RELATED
"""

def my_ls(paths_list):
    print(paths_list)
    print('fish')
    path = os.path.join(*paths_list)
    return os.listdir(path)

def load_file(paths_list, file_name):
    paths = paths_list + [file_name]
    return os.path.join(*paths)

def load_source_file(file_path):
    return load_file(cfg.SOURCE_PATH, file_path)

def get_earliest_file(paths_list):
    files = my_ls(paths_list)
    print(len(files))
    return sorted(
        files, 
        key=lambda file_path: os.path.getctime(load_source_file(file_path)), 
        reverse=True
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
