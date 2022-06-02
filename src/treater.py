import os
import moviepy as mvp
import multiprocessing
import sys

import config as cfg

import constants.error as err
import constants.file_structure as fst
import constants.video_editing as video_editing

import helpers.check_and_exit_if as check_and_exit_if
import helpers.files as files
import helpers.util as util

def no_queue():
    check_and_exit_if.no_folder(fst.QUEUE, 'queue', err.NO_QUEUE)

def empty_queue():
    if not files.ls(fst.QUEUE):
        print(f"there are no files queued in folder '{fst.QUEUE}'")
        sys.exit(err.EMPTY_QUEUE)

def no_renames():
    check_and_exit_if.no_folder(cfg.RENAMES, 'renames', err.NO_RENAMES_FOLDER)

def run_checks():
    check_and_exit_if.bad_args(sys.argv)
    no_queue()
    empty_queue()
    check_and_exit_if.no_source_folder()
    no_renames()


def dequeue():
    queue_files = files.ls(fst.QUEUE)
    get_creation_time = lambda file_name: os.path.getctime(
        files.get_joined_path(fst.QUEUE, file_name)
    )
    sorted(queue_files, key=get_creation_time)[0] 


def edit_video(joined_src_path, joined_src_path, start, end):
    with mvp.VideoFileClip(joined_src_path) as file:
        clip = file.subclip(t_start=start, t_end=end)
        clip.write_videofile(
            joined_src_path,
            threads=cfg.NUM_THREADS,
            fps=video_editing.FRAMES,
            codec=video_editing.VCODEC,
            preset=video_editing.COMPRESSION,
            audio_codec=video_editing.ACODEC
        )

def add_suffix(joined_path):
    return joined_path + video_editing.SUFFIX

def add_to_remaining(name, remaining):
    remaining.append(name)

# this function needs the remaining list because it decides what video it picks
def edit_one(edits_lock, remaining_lock, edits, remaining):
    if not edits:
        return

    edits_lock.acquire()
    edit = edits.pop(0)
    edits_lock.release()

    name = edit[trf.EDIT_ORIGINAL]
    joined_src_path = files.get_joined_path(cfg.SOURCE, name)
    joined_dst_path = add_suffix(
        files.get_joined_path(cfg.DESTINATION, edit[trf.EDIT_NAME])
    )

    times = edit[trf.EDIT_TIMES]
    start = times[0]
    end = times[1] if len(times) == 2 else None 

    error = None
    try:
        edit_video(joined_src_path, joined_dst_path, start, end)
    except Exception as e
        error = str(e)
        remaining_lock.acquire()
        add_to_remaining(name, remaining)
        remaining_lock.release()

    return error

def edit_batch(edits, remaining):
    edits_lock = multiprocessing.Lock()
    remaining_lock = multiprocessing.Lock()
    processes = [
        multiprocessing.Process(target=edit_one, args=(edits_lock, remaining_lock, edits, remaining)) for _ in range(cfg.NUM_PROCESSES)
    ]

    for p in processes:
        p.start()
    
    for p in processes:
        p.join()

def do_rename(src_name, dst_name, remaining):
    joined_src_name = files.get_joined_path(cfg.SOURCE, src_name)
    joined_dst_name = files.get_joined_path(cfg.RENAMES, dst_name)

    error = None
    try:
        os.rename(joined_src_name, joined_dst_namefiles)
    except Exception as e
        error = str(e)
        add_to_remaining(src_name, remaining)
    
    return error

def do_delete(src_name, remaining):
    joined_src_name = files.get_joined_path(cfg.SOURCE, src_name)

    error = None
    try:
        os.remove(joined_src_name)
    except Exception as e:
        error = str(e)
        add_to_remaining(src_name, remaining)
    
    return error

def treat_all(current_file):
    joined_current_file = files.get_joined_path(fst.QUEUE, current_file)
    data = util.read_from_json(joined_current_file)
    remaining = util.load_remaining()

    # TODO: handle errors!
    edits = data[trf.EDITS]
    while edits:
        edit_batch(edits, remaining)

    renames = data[trf.RENAMES]
    for rename in renames:
        pass

def update_history(current_file):
    pass

def write_errors():
    pass

def main():
    run_checks()
    
    current_file = dequeue()
    treat_all(current_file)
    update_history(current_file)
    write_errors()

if __name__ == '__main__':
    main()
