import os


def join_folder(paths_list):
    return os.path.join(*paths_list)

def get_joined_path(paths_list, file_name):
    return join_folder(paths_list + [file_name])

def do_folder_operation(paths_list, handler):
    return handler(
        join_folder(paths_list)
    )

def ls(paths_list, recent=False):
    return sorted(
        do_folder_operation(paths_list, os.listdir),
        reversed=recent 
    )

def folder_exists(paths_list):
    return do_folder_operation(paths_list, os.path.exists)
