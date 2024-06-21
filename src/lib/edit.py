import concurrent.futures
import os
import moviepy.editor as mvp
import subprocess

import constants.errors_format as errors_format
import constants.treatment_format as treatment_format
import constants.video_editing as video_editing

import helpers.files as files
import helpers.video_paths as video_paths
import helpers.time_handlers as time_handlers


def treat_all(
    data: list[dict],
    use_moviepy: bool, moviepy_threads: int, num_processes: int,
    remaining: list[str], errors: list[dict], paths: video_paths.VideoPaths
):
    edits = data[treatment_format.EDITS]
    edit_all(edits, use_moviepy, moviepy_threads,
             num_processes, remaining, errors, paths)

    renames = data[treatment_format.RENAMES]
    rename_all(renames, remaining, errors, paths)

    deletions = data[treatment_format.DELETIONS]
    delete_all(deletions, remaining, errors, paths)


def edit_all(
        edits: list[dict], use_moviepy: bool, moviepy_threads: int,
        num_processes: int, remaining: list[str], errors: list[dict],
        paths: video_paths.VideoPaths):
    with concurrent.futures.ProcessPoolExecutor(
            max_workers=num_processes) as executor:
        results = [executor.submit(
            edit_one, edit, use_moviepy, moviepy_threads, paths)
            for edit in edits]
        for future, edit in zip(
                concurrent.futures.as_completed(results), edits):
            try:
                future.result()
            except Exception as e:
                handle_error(
                    errors, remaining, edit[treatment_format.EDIT_ORIGINAL],
                    str(e), treatment_format.EDITS, edit)


def edit_one(edit: dict, use_moviepy: bool, moviepy_threads: int,
             paths: video_paths.VideoPaths):
    name = edit[treatment_format.EDIT_ORIGINAL]
    joined_src_path = files.get_joined_path(paths.source, name)
    joined_dst_path = files.get_joined_path(
        paths.edits, edit[treatment_format.EDIT_NAME])

    times = edit[treatment_format.EDIT_TIMES]
    start = times[treatment_format.EDIT_TIMES_START]
    end = times[treatment_format.EDIT_TIMES_END]
    edit_video(use_moviepy, moviepy_threads,
               joined_src_path, joined_dst_path, start, end)


def edit_video(
        use_moviepy: bool, moviepy_threads: int,
        joined_src_path: str, joined_dst_path: str,
        start: None | str, end: None | str):
    if use_moviepy:
        edit_moviepy(moviepy_threads, joined_src_path,
                     joined_dst_path, start, end)
    else:
        edit_ffmpeg(joined_src_path, joined_dst_path, start, end)


def edit_moviepy(
        joined_src_path: str, joined_dst_path: str,
        start: None | str, end: None | str, moviepy_threads: int):
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


def edit_ffmpeg(
        joined_src_path: str, joined_dst_path: str,
        start: None | str, end: None | str):
    source = ['-accurate_seek', '-i', joined_src_path]
    args = ['ffmpeg', '-y', *generate_ffmpeg_args(source, start, end),
            '-c', 'copy', joined_dst_path]
    subprocess.run(args, check=True)


def generate_ffmpeg_args(
        source: list[str], start: None | str, end: None | str) -> list[str]:
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


def handle_error(
        errors: list[dict], remaining: list[str],
        name: str, message: str, command: str, data: str):
    add_error(errors, name, message, command, data)
    add_to_remaining(remaining, name)


def add_error(
        errors: list[dict], name: str, message: str, command: str, data: str):
    errors.append(
        create_error_dict(name, message, command, data)
    )


def create_error_dict(name: str, message: str, command: str, data: str):
    return {
        errors_format.ERROR_FILE_NAME: name,
        errors_format.ERROR_MESSAGE: message,
        errors_format.ERROR_COMMAND: command,
        errors_format.ERROR_DATA: data
    }


def add_to_remaining(remaining: list[str], name: str):
    remaining.append(name)


def rename_all(
        renames: dict[str, str], remaining: list[str], errors: list[dict],
        paths: video_paths.VideoPaths):
    for rename_source in renames:
        new_name = renames[rename_source]
        try:
            do_rename(rename_source, new_name, paths)
        except Exception as e:
            handle_error(errors, remaining, rename_source,
                         str(e), treatment_format.RENAMES, new_name)


def do_rename(src_name: str, dst_name: str, paths: video_paths.VideoPaths):
    joined_src_name = files.get_joined_path(paths.source, src_name)
    joined_dst_name = files.get_joined_path(paths.renames, dst_name)
    os.rename(joined_src_name, joined_dst_name)


def delete_all(
        deletions: list[str], remaining: list[str], errors: list[dict],
        paths: video_paths.VideoPaths):
    for deletion_name in deletions:
        try:
            do_delete(deletion_name, paths)
        except Exception as e:
            handle_error(errors, remaining, deletion_name,
                         str(e), treatment_format.DELETIONS, None)


def do_delete(src_name: str, paths: video_paths.VideoPaths):
    joined_src_name = files.get_joined_path(paths.source, src_name)
    os.remove(joined_src_name)
