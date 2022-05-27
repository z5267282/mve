import os

import config as cfg
import helper as helper

def get_earliest_file(paths_list):
    files = ls_joined_path(paths_list)
    return sorted(
        files, 
        key=os.path.getctime
    )[0] if files else None

def do_edit(src_full_path, dst_full_path, start, end=None):
    edit_video = lambda clip: clip.write_videofile(
            dst_full_path, 
            threads=cfg.NUM_THREADS,
            fps=cfg.FRAMES,
            codec=cfg.VCODEC,
            preset=cfg.COMPRESSION,
            audio_codec=cfg.ACODEC
    )
    return helper.handle_clip(src_full_path, edit_video, start, end)

def do_rename(src_full_path, dst_path, dst_name):
    error = None
    try:
        dst_full_path = helper.get_joined_path(dst_path, dst_name)
        os.rename(src_full_path, dst_full_path)
    except OSError as e:
        error = str(e)

    return error

def do_delete(src_full_path):
    error = None
    try:
        os.remove(src_full_path)
    except OSError as e:
        error = str(e)
    
    return error
