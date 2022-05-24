import os

import config as cfg
import helper as helper

"""
    DOING COMMANDS
"""
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
        dst_full_path = helper.load_file(dst_path, dst_name)
        os.rename(src_full_path, dst_full_path)
    except OSError as e:
        error = str(e)

    return error

def do_delete(src_full_path):
    os.remove(src_full_path)

"""
    ADDING TO LOGS
"""
def add_edit(edit_ls, src_name, dst_name, times):
    new_edit = {
        cfg.EDIT_NEW_NAME : dst_name,
        cfg.EDIT_TIMES    : times
    }
    edit_ls.append({src_name : new_edit})

"""
"""