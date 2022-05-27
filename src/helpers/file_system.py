import os

def get_joined_path(paths_list, file_name):
    paths = paths_list + [file_name]
    return os.path.join(*paths)

def ls(paths_list):
    path = os.path.join(*paths_list)
    return os.listdir(path)
