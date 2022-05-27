import os

def get_joined_path(paths_list, file_name):
    paths = paths_list + [file_name]
    return os.path.join(*paths)
