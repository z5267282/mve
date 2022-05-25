import os

import config as cfg
import helper as helper

"""
    ADDING TO LOGS
"""

def add_edit(edit_dict, src_name, dst_name, times):
    new_edit = {
        cfg.EDIT_NEW_NAME : dst_name,
        cfg.EDIT_TIMES    : times
    }
    edit_dict[src_name] = new_edit

def add_rename(rename_dict, src_name, dst_name):
    rename_dict[src_name] = dst_name

def add_delete(delete_list, src_name):
    delete_list.append(src_name)

"""
    ADDING LOGS TO QUEUE
"""

def generate_folder_name():
    return helper.get_timestamp()

def write_all_logs(paths_list, folder_name, edit_dict, rename_dict, delete_list):
    joined_folder_path = helper.get_joined_path(paths_list, folder_name)
    os.mkdir(joined_folder_path)

    for data, file_name in zip(
        [edit_dict, rename_dict, delete_list],
        [cfg.EDITS, cfg.RENAMES, cfg.DELETIONS]
    ):
        helper.write_to_json(data, file_name)

"""
    VIEWING FILES
"""

def view_file(joined_path):
    os.startfile(joined_path)

"""
    COMMAND PARSING
"""

def check_bad_args(command_key):
    pass

def parse_end(token_string):
    tokens = token_string.split(' ', maxsplit=1)

    if len(tokens != 2):
        print(f'usage: {cfg.HELP_MSGS[cfg.KEY_END]}')
        return

    # if not re.fullmatch(cfg.RE_END_TIME, 

"""
    MAIN
"""

def view_error_folder(folder_name, edits, renames, delitions):
    # TODO: move error folder 
    pass

def view_remaining(edits, renames, deletions):
    # TODO
    pass

def main():
    edits = {}
    renames = {}
    deletions = []

    error_folder = helper.get_earliest_file(cfg.ERRORS)
    if error_folder:
        view_error_folder(error_folder, edits, renames, deletions)
    else:
        view_remaining(edits, renames, deletions)

    write_all_logs(cfg.QUEUE, generate_folder_name(), edits, renames, deletions)

if __name__ =='__main__':
    main()
