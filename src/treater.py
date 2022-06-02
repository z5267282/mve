import os
import sys

import config as cfg

import constants.error as err
import constants.file_structure as fst

import helpers.check_and_exit_if as check_and_exit_if
import helpers.files as files



def no_queue():
    check_and_exit_if.no_folder(fst.QUEUE, 'queue', err.NO_QUEUE)

def empty_queue():
    if not files.ls(fst.QUEUE):
        print(f"there are no files queued in folder '{fst.QUEUE}'")
        sys.exit(err.EMPTY_QUEUE)

def no_renames():
    check_and_exit_if.no_folder(cfg.RENAMES, 'renames', err.NO_RENAMES_FOLDER)

def run_checks():
    check_and_exit_if.bad_args(sys.argv)
    no_queue()
    empty_queue()
    check_and_exit_if.no_source_folder()
    no_renames()


def dequeue():
    queue_files = files.ls(fst.QUEUE)
    get_creation_time = lambda file_name: os.path.getctime(
        files.get_joined_path(fst.QUEUE, file_name)
    )
    sorted(queue_files, key=get_creation_time)[0] 

def treat_all(current_file):
    pass

def update_history(current_file):
    pass

def write_errors():
    pass

def main():
    run_checks()
    
    current_file = dequeue()
    treat_all(current_file)
    update_history(current_file)
    write_errors()

if __name__ == '__main__':
    main()
