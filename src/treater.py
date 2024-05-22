import concurrent.futures
import os
import moviepy.editor as mvp
import subprocess
import sys

import config as cfg

import constants.error as err
import constants.errors_format as erf
import constants.file_structure as fst
import constants.treatment_format as trf
import constants.video_editing as vde

import helpers.check_and_exit_if as check_and_exit_if
import helpers.colours as colours
import helpers.files as files
import helpers.json_handlers as json_handlers
import helpers.paths as paths
import helpers.time_handlers as time_handlers
import helpers.timestamps as timestamps
import helpers.util as util


def main():
    run_checks()

    remaining, errors = json_handlers.load_remaining(), list()
    current_file = dequeue()
    joined_current_file = files.get_joined_path(fst.QUEUE, current_file)
    data = json_handlers.read_from_json(joined_current_file)
    folders = util.create_paths_from_config()

    TODO_FIX = False
    TODO_FIX_1, TODO_FIX_2 = 2, 4

    treat_all(data, TODO_FIX, TODO_FIX_1,
              TODO_FIX_2, remaining, errors, folders)
    update_history(current_file, joined_current_file)

    if errors:
        handle_errors(remaining, errors)

    util.exit_treat_all_good()


def run_checks():
    check_and_exit_if.no_args(sys.argv)
    check_and_exit_if.no_queue()
    check_empty_queue()
    check_and_exit_if.one_of_config_folders_missing()
    no_history()


def check_empty_queue():
    if not files.ls(fst.QUEUE):
        print(f"there are no files queued in folder '{fst.QUEUE}'")
        sys.exit(err.EMPTY_QUEUE)


def no_history():
    check_and_exit_if.no_folder(fst.HISTORY, 'history', err.NO_HISTORY_FOLDER)


def dequeue():
    queue_files = files.ls(fst.QUEUE)
    return queue_files[0]


def treat_all(data, use_moviepy: bool, moviepy_threads: int, num_processes: int, remaining, errors, paths: paths.Paths):
    edits = data[trf.EDITS]
    edit_all(edits, use_moviepy, moviepy_threads,
             num_processes, remaining, errors, paths)

    renames = data[trf.RENAMES]
    rename_all(renames, remaining, errors, paths)

    deletions = data[trf.DELETIONS]
    delete_all(deletions, remaining, errors, paths)


def edit_all(edits, use_moviepy: bool, moviepy_threads: int, num_processes: int, remaining, errors, paths: paths.Paths):
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_processes) as executor:
        results = [executor.submit(
            edit_one, edit, use_moviepy, moviepy_threads, paths) for edit in edits]
        for future, edit in zip(concurrent.futures.as_completed(results), edits):
            try:
                future.result()
            except Exception as e:
                handle_error(errors, remaining,
                             edit[trf.EDIT_ORIGINAL], str(e), trf.EDITS, edit)


def edit_one(edit, use_moviepy: bool, moviepy_threads: int, paths: paths.Paths):
    name = edit[trf.EDIT_ORIGINAL]
    joined_src_path = files.get_joined_path(paths.source, name)
    joined_dst_path = files.get_joined_path(paths.edits, edit[trf.EDIT_NAME])

    times = edit[trf.EDIT_TIMES]
    start, end = times[trf.EDIT_TIMES_START], times[trf.EDIT_TIMES_END]
    edit_video(use_moviepy, moviepy_threads,
               joined_src_path, joined_dst_path, start, end)


def edit_video(use_moviepy: bool, moviepy_threads: int, joined_src_path, joined_dst_path, start, end):
    if use_moviepy:
        edit_moviepy(moviepy_threads, joined_src_path,
                     joined_dst_path, start, end)
    else:
        edit_ffmpeg(joined_src_path, joined_dst_path, start, end)


def edit_moviepy(joined_src_path, joined_dst_path, start, end, moviepy_threads: int):
    with mvp.VideoFileClip(joined_src_path) as file:
        clip = file.subclip(t_start=start, t_end=end)
        clip.write_videofile(
            joined_dst_path,
            threads=moviepy_threads,
            fps=vde.FRAMES,
            codec=vde.VCODEC,
            preset=vde.COMPRESSION,
            audio_codec=vde.ACODEC
        )


def edit_ffmpeg(joined_src_path, joined_dst_path, start, end):
    source = ['-accurate_seek', '-i', joined_src_path]
    args = ['ffmpeg', '-y', *
            generate_ffmpeg_args(source, start, end), '-c', 'copy', joined_dst_path]
    subprocess.run(args, check=True)


def generate_ffmpeg_args(source, start, end):
    if start is None and end is None:
        return source

    if start is None:
        return [*source, '-to', end]

    if end is None:
        return ['-sseof' if start.startswith('-') else '-ss', start, *source]

    relative_time = str(
        time_handlers.get_seconds(end) - time_handlers.get_seconds(start)
    )
    return ['-ss', start, *source, '-to', relative_time]


def handle_error(errors, remaining, name, message, command, data):
    add_error(errors, name, message, command, data)
    add_to_remaining(remaining, name)


def add_error(errors, name, message, command, data):
    errors.append(
        create_error_dict(name, message, command, data)
    )


def create_error_dict(name, message, command, data):
    return {
        erf.ERROR_FILE_NAME: name,
        erf.ERROR_MESSAGE: message,
        erf.ERROR_COMMAND: command,
        erf.ERROR_DATA: data
    }


def add_to_remaining(remaining, name):
    remaining.append(name)


def rename_all(renames, remaining, errors, paths: paths.Paths):
    for rename_source in renames:
        new_name = renames[rename_source]
        try:
            do_rename(rename_source, new_name, paths)
        except Exception as e:
            handle_error(errors, remaining, rename_source,
                         str(e), trf.RENAMES, new_name)


def do_rename(src_name, dst_name, paths: paths.Paths):
    joined_src_name = files.get_joined_path(paths.source, src_name)
    joined_dst_name = files.get_joined_path(paths.renames, dst_name)
    os.rename(joined_src_name, joined_dst_name)


def delete_all(deletions, remaining, errors, paths: paths.Paths):
    for deletion_name in deletions:
        try:
            do_delete(deletion_name, paths)
        except Exception as e:
            handle_error(errors, remaining, deletion_name,
                         str(e), trf.DELETIONS, None)


def do_delete(src_name, paths: paths.Paths):
    joined_src_name = files.get_joined_path(paths.source, src_name)
    os.remove(joined_src_name)


def update_history(current_file, joined_current_file):
    joined_history_file = files.get_joined_path(fst.HISTORY, current_file)
    os.rename(joined_current_file, joined_history_file)


def handle_errors(remaining, errors):
    error_file_name = timestamps.generate_timestamped_file_name()
    write_errors(error_file_name, errors)
    json_handlers.write_remaining(remaining)
    exit_treatment_error(error_file_name)


def write_errors(error_file_name, errors):
    joined_error_file_name = files.get_joined_path(fst.ERRORS, error_file_name)
    data = {
        erf.ERRORS_VIDEOS: errors,
        erf.ERRORS_PATHS: util.generate_paths_dict()
    }
    json_handlers.write_to_json(data, joined_error_file_name)


def exit_treatment_error(error_file_name):
    util.print_error(
        f"one or more errors occurred during treatment logged in '{colours.highlight(error_file_name)}'")
    sys.exit(err.TREATMENT_ERROR)


if __name__ == '__main__':
    main()
