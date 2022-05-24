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
    abs_folder_path = helper.get_abs_path(paths_list, folder_name)
    os.mkdir(abs_folder_path)

    data_items = [edit_dict, rename_dict, delete_list]
    file_names = [cfg.EDITS, cfg.RENAMES, cfg.DELETIONS]
    for data, file_name in zip(data_items, file_names):
        helper.write_to_json(data, file_name)

"""
    VIEWING FILES
"""

def view_file(abs_path):
    os.startfile(abs_path)

"""
    MAIN
"""

def main():
    edits = {}
    renames = {}
    deletions = []

    # write_all_logs(cfg.QUEUE, generate_folder_name(), edits, renames, deletions)

if __name__ =='__main__':
    main()
