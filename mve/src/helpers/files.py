import os
import pathlib
import typing


def join_folder(paths_list: list[str]) -> str:
    return os.path.join(*paths_list)


def get_joined_path(paths_list: list[str], file_name: str):
    return join_folder(paths_list + [file_name])


def do_folder_operation(
    paths_list: list[str], handler: typing.Callable
) -> typing.Any:
    return handler(
        join_folder(paths_list)
    )


def ls(paths_list: list[str], recent: bool = False) -> list[str]:
    raw: list[str] = sorted(
        do_folder_operation(paths_list, os.listdir),
        key=lambda file_name: os.path.getmtime(
            get_joined_path(paths_list, file_name)
        ),
        reverse=recent
    )
    return [r for r in raw if not r.startswith('.')]


def folder_exists(paths_list: list[str]) -> bool:
    return do_folder_operation(paths_list, os.path.exists)


def tokenise_path(display: str, given: None | str) -> list[str]:
    full_path = input(f'{display} : ') if given is None else given
    return handle_dot(full_path)


def split_path(full_path: str) -> list[str]:
    return list(
        pathlib.Path(full_path).parts
    )


def handle_dot(full_path: str) -> list[str]:
    '''pathlib.Path cannot handle paths starting with a '.' so they must be
    manually handled.'''

    return ['.'] if full_path == '.' else split_path(full_path)
