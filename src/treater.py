import concurrent.futures
import os
import moviepy.editor as mvp
import subprocess
import sys

import config

import constants.error as error
import constants.errors_format as erf
import constants.treatment_format as treatment_format
import constants.video_editing as video_editing

import helpers.args as args
import helpers.colours as colours
import helpers.files as files
import helpers.json_handlers as json_handlers
import helpers.paths as paths
import helpers.time_handlers as time_handlers
import helpers.timestamps as timestamps
import helpers.util as util


def main():
    name = args.expect_config_name(sys.argv)
    state = config.Stateful(name)
    run_checks(state)

    cfg = state.cfg

    remaining, errors = state.load_remaining(), list()
    current_file = dequeue(state)
    joined_current_file = files.get_joined_path(state.queue, current_file)
    data = json_handlers.read_from_json(joined_current_file)
    folders = cfg.create_source_folders()

    treat_all(
        data,
        cfg.use_moviepy, cfg.moviepy_threads,
        cfg.num_processes,
        remaining, errors, folders
    )
    update_history(state, current_file, joined_current_file)

    if errors:
        paths_dict = state.generate_paths_dict()
        handle_errors(state, remaining, errors, paths_dict)

    util.exit_treat_all_good()


def run_checks(state: config.Stateful):
    check_empty_queue(state)
    state.cfg.one_of_config_folders_missing()


def check_empty_queue(state: config.Stateful):
    if not files.ls(state.queue):
        print(f"there are no files queued in folder '{state.queue}'")
        sys.exit(error.EMPTY_QUEUE)


def dequeue(state: config.Stateful):
    queue_files = files.ls(state.queue, recent=True)
    return queue_files[0]


def treat_all(
    data: list[dict],
    use_moviepy: bool, moviepy_threads: int, num_processes: int,
    remaining: list[str], errors: list[dict], paths: paths.Paths
):
    edits = data[treatment_format.EDITS]
    edit_all(edits, use_moviepy, moviepy_threads,
             num_processes, remaining, errors, paths)

    renames = data[treatment_format.RENAMES]
    rename_all(renames, remaining, errors, paths)

    deletions = data[treatment_format.DELETIONS]
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
                             edit[treatment_format.EDIT_ORIGINAL], str(e), treatment_format.EDITS, edit)


def edit_one(edit, use_moviepy: bool, moviepy_threads: int, paths: paths.Paths):
    name = edit[treatment_format.EDIT_ORIGINAL]
    joined_src_path = files.get_joined_path(paths.source, name)
    joined_dst_path = files.get_joined_path(
        paths.edits, edit[treatment_format.EDIT_NAME])

    times = edit[treatment_format.EDIT_TIMES]
    start, end = times[treatment_format.EDIT_TIMES_START], times[treatment_format.EDIT_TIMES_END]
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
            fps=video_editing.FRAMES,
            codec=video_editing.VCODEC,
            preset=video_editing.COMPRESSION,
            audio_codec=video_editing.ACODEC
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
                         str(e), treatment_format.RENAMES, new_name)


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
                         str(e), treatment_format.DELETIONS, None)


def do_delete(src_name: list[str], paths: paths.Paths):
    joined_src_name = files.get_joined_path(paths.source, src_name)
    os.remove(joined_src_name)


def update_history(
    state: config.Stateful, current_file: str, joined_current_file: str
):
    joined_history_file = files.get_joined_path(state.history, current_file)
    os.rename(joined_current_file, joined_history_file)


def handle_errors(
    state: config.Stateful,
    remaining: list[str], errors: list[dict], paths_dict: dict[str, list[str]]
):
    error_file_name = timestamps.generate_timestamped_file_name()
    write_errors(error_file_name, errors, paths_dict)
    state.write_remaining(remaining)
    exit_treatment_error(error_file_name)


def write_errors(
    state: config.Stateful,
    error_file_name: str, errors: list[dict], paths_dict: dict[str, list[str]]
):
    joined_error_file_name = files.get_joined_path(
        state.errors, error_file_name)
    data = {
        erf.ERRORS_VIDEOS: errors,
        erf.ERRORS_PATHS: paths_dict
    }
    json_handlers.write_to_json(data, joined_error_file_name)


def exit_treatment_error(error_file_name):
    util.print_error(
        "one or more errors occurred during treatment logged in '{}'".format(
            colours.highlight(error_file_name)
        )
    )
    sys.exit(error.TREATMENT_ERROR)


if __name__ == '__main__':
    main()
