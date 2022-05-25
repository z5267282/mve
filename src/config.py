# editing folders
SOURCE_PATH  = ['D:', 'Videos', 'Batches', '1']
RENAMES_PATH = ['D:', 'Videos', 'Renames']

# log folders
QUEUE   = ['queue']
HISTORY = ['history']
ERRORS  = ['errors']

# current files
EDITS     = 'edits.json'
RENAMES   = 'renames.json'
DELETIONS = 'deletions.json'

PATHS     = 'paths.json'

# other files
REMAINING = 'remaining.json'

# video editing settings
SUFFIX = '.mp4'

NUM_THREADS = 8
FRAMES      = 60
VCODEC      = "libx264"
COMPRESSION = "slower"
ACODEC      = 'aac'

# edit structure keys inside current/
EDIT_NEW_NAME = 'new name'
EDIT_TIMES    = 'times'

# multiprocessing
NUM_PROCESSES = 4

# JSON settings
JSON_INDENT = 4

# command keys
KEY_END      = 'e'
KEY_MIDDLE   = 'm'
KEY_RENAME   = 'r'
KEY_DELETE   = 'd'
KEY_CONTINUE = 'c'
KEY_HELP     = 'h'

# keys for storing commands
CMD_NAME = 'name'
CMD_ARGS = 'args'
CMD_DESC = 'description'

# help messages
HELP_MSGS = {
    KEY_END      : {CMD_NAME: '[e]nd', CMD_ARGS: ['time', 'name'], CMD_DESC: 'edit from [ time ] to end of clip'},
    KEY_MIDDLE   : {CMD_NAME: '[m]iddle', CMD_ARGS: ['start', 'end', 'name' ], CMD_DESC: 'edit from [ start ] to [ end ]'},
    KEY_RENAME   : {CMD_NAME: '[r]ename', CMD_ARGS: ['name'], CMD_DESC: 'rename the clip to [ name ]'},
    KEY_DELETE   : {CMD_NAME: '[d]elete', CMD_ARGS: [], CMD_DESC: 'delete the clip'},
    KEY_CONTINUE : {CMD_NAME: '[c]ontinue', CMD_ARGS: [], CMD_DESC: 're-add the current clip so it can be transformed twice'},
    KEY_HELP     : {CMD_NAME: '[h]elp', CMD_ARGS: [], CMD_DESC: 'print this message'}
}

# regex patterns
RE_NAME     = r'[a-zA-Z0-9 ]+'
RE_END_TIME = r'-?[0-9]+|([0-9]+-)+[0-9]+'
