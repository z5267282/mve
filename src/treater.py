import concurrent.futures
import os
import moviepy.editor as mvp
import sys

import config as cfg

import constants.error as err
import constants.errors_format as erf
import constants.file_structure as fst
import constants.treatment_format as trf
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

def no_history():
    check_and_exit_if.no_folder(fst.HISTORY, 'history', err.NO_HISTORY_FOLDER)

def no_errors():
    check_and_exit_if.no_folder(fst.ERRORS, 'errors', err.NO_ERRORS_FOLDER)

def run_checks():
    check_and_exit_if.bad_args(sys.argv)
    no_queue()
    empty_queue()
    check_and_exit_if.no_source_folder()
    no_renames()
    no_history()
    no_errors()


def dequeue():
    queue_files = files.ls(fst.QUEUE)
    get_creation_time = lambda file_name: os.path.getctime(
        files.get_joined_path(fst.QUEUE, file_name)
    )
    return sorted(queue_files, key=get_creation_time)[0] 


def create_error_dict(name, message, command, data):
    return {
        erf.ERROR_FILE_NAME : name,
        erf.ERROR_MESSAGE   : message,
        erf.ERROR_COMMAND   : command,
        erf.ERROR_DATA      : data
    }

def add_error(errors, name, message, command, data):
    errors.append(
        create_error_dict(name, message, command, data)
    )

def add_to_remaining(remaining, name):
    remaining.append(name)

def handle_error(errors, remaining, name, message, command, data):
    add_error(errors, name, message, command, data)
    add_to_remaining(remaining, name)


def edit_video(joined_src_path, joined_dst_path, start, end):
    with mvp.VideoFileClip(joined_src_path) as file:
        clip = file.subclip(t_start=start, t_end=end)
        clip.write_videofile(
            joined_dst_path,
            threads=cfg.NUM_THREADS,
            fps=video_editing.FRAMES,
            codec=video_editing.VCODEC,
            preset=video_editing.COMPRESSION,
            audio_codec=video_editing.ACODEC
        )

def add_suffix(joined_path):
    return joined_path + video_editing.SUFFIX

def edit_one(edit):
    name = edit[trf.EDIT_ORIGINAL]
    joined_src_path = files.get_joined_path(cfg.SOURCE, name)
    joined_dst_path = add_suffix(
        files.get_joined_path(cfg.DESTINATION, edit[trf.EDIT_NAME])
    )

    times = edit[trf.EDIT_TIMES]
    start = times[0]
    end = times[1] if len(times) == 2 else None 

    edit_video(joined_src_path, joined_dst_path, start, end)
        
def edit_all(edits, remaining, errors):
    with concurrent.futures.ProcessPoolExecutor(max_workers=cfg.NUM_PROCESSES) as executor:
        results = [executor.submit(edit_one, edit) for edit in edits]
        for future, edit in zip(concurrent.futures.as_completed(results), edits):
            try:
                future.result()
            except Exception as e:
                handle_error(errors, remaining, edit[trf.EDIT_ORIGINAL], str(e), trf.EDITS, edit)

def do_rename(src_name, dst_name):
    joined_src_name = files.get_joined_path(cfg.SOURCE, src_name)
    joined_dst_name = add_suffix(
        files.get_joined_path(cfg.RENAMES, dst_name)
    )

    os.rename(joined_src_name, joined_dst_name)

def rename_all(renames, remaining, errors):
    for rename_source in renames:
        new_name = renames[rename_source]
        try:
            do_rename(rename_source, new_name)
        except Exception as e:
            handle_error(errors, remaining, rename_source, str(e), trf.RENAMES, new_name)

def do_delete(src_name):
    joined_src_name = files.get_joined_path(cfg.SOURCE, src_name)

    os.remove(joined_src_name)

def delete_all(deletions, remaining, errors):
    for deletion_name in deletions:
        try:
            do_delete(deletion_name)
        except Exception as e:
            handle_error(errors, remaining, deletion_name, str(e), trf.DELETIONS, None)

def treat_all(joined_current_file, remaining, errors):
    data = util.read_from_json(joined_current_file)

    edits = data[trf.EDITS]
    edit_all(edits, remaining, errors)

    renames = data[trf.RENAMES]
    rename_all(renames, remaining, errors)
    
    deletions = data[trf.DELETIONS]
    delete_all(deletions, remaining, errors)

def update_history(current_file, joined_current_file):
    joined_history_file = files.get_joined_path(fst.HISTORY, current_file)
    os.rename(joined_current_file, joined_history_file)

def write_errors(errors):
    error_file_name = util.generate_timestamped_file_name()
    joined_error_file_name = files.get_joined_path(fst.ERRORS, error_file_name)
    data = {
        erf.ERRORS_VIDEOS: errors,
        erf.ERRORS_PATHS : util.generate_paths_dict()
    }
    util.write_to_json(data, joined_error_file_name)

def main():
    run_checks()

    remaining, errors = util.load_remaining(), list()
    current_file = dequeue()
    joined_current_file = files.get_joined_path(fst.QUEUE, current_file)
    treat_all(joined_current_file, remaining, errors)
    update_history(current_file, joined_current_file)

    if errors:
        write_errors(errors)
        util.write_remaining(remaining)

if __name__ == '__main__':
    main()
