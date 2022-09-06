import os


def get_joined_path(paths_list, file_name):
    paths = paths_list + [file_name]
    return os.path.join(*paths)

def do_folder_operation(paths_list, handler):
    path = os.path.join(*paths_list)
    return handler(path)

def ls(paths_list):
    return sorted(do_folder_operation(paths_list, os.listdir))

def folder_exists(paths_list):
    return do_folder_operation(paths_list, os.path.exists)
