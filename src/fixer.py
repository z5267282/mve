# usage: <history file to fix>

import sys

import helpers.util as util

def main():
    file_name, = sys.argv[1:]
    session = util.read_from_json(file_name)
    edits = session['edits']
    for edit in edits:
        treat_edit(edit)
    
    util.write_to_json(session, file_name)

def treat_edit(edit):
    times = edit['times']
    start = times.pop(0)
    new_times = {'start' : start}
    if times:
        new_times['end'] = times.pop()
    edit['times'] = new_times

if __name__ == '__main__':
    main()
