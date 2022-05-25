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

# help messages
HELP_MSGS = {
    KEY_END      : '[e]nd      | [ time ] [ name ]          | edit from [ time ] to end of clip',
    KEY_MIDDLE   : '[m]iddle   | [ start ] [ end ] [ name ] | edit from [ start ] to [ end ]',
    KEY_RENAME   : '[r]ename   | [ name ]                   | rename the clip to [ name ]',
    KEY_DELETE   : '[d]elete   |                            | delete the clip',
    KEY_CONTINUE : '[c]ontinue |                            | re-add the current clip so it can be transformed twice',
    KEY_HELP     : '[h]elp     |                            | print this message'
}
