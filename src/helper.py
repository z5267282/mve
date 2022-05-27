import datetime as dt
import json
import moviepy as mvp
import os

import config as cfg


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

"""
    TIMESTAMPING
"""

def get_timestamp():
    right_now = dt.datetime.now()
    return right_now.strftime('%d.%m.%Y - %H%M')

"""
    LOGGING
"""
def log_paths():
    # TODO 
    pass
