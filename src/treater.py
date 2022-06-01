import os

import config as cfg

import constants.file_structure as fst

import helpers.files as files

def dequeue():
    queue_files = files.ls(fst.QUEUE)
    get_creation_time = lambda file_name: os.path.getctime(
        files.get_joined_path(fst.QUEUE, file_name)
    )
    return sorted(queue_files, key=get_creation_time)[0] if queue_files else None

def main():
    dequeue()

if __name__ == '__main__':
    main()
