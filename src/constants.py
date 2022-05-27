# file structure folders
QUEUE  = ['queue']
ERRORS = ['errors']


# remaining

# remaining file name
REMAINING = 'remaining.json'

# remaining keys

EDITS     = 'edits'
# keys within edits
EDIT_NAME  = 'new name'
EDIT_TIMES = 'times'

RENAMES   = 'renames'
DELETIONS = 'deletions'

SOURCE_PATH = 'source path'
RENAME_PATH = 'renames path'


# errors keys - keys for the a whole file in errors/
ERRORS_VIDEOS = 'files'
ERRORS_PATHS  = 'paths'

# error keys - keys for a single dictionary inside the list of error videos
ERROR_COMMAND = 'error'
ERROR_DATA    = 'data'


# exit codes in case of error

# remaining
FILES_REMAINING   = 1
MISSING_REMAINING = 2

# config path folders
NO_SOURCE_FOLDER  = 3
NO_RENAMES_FOLDER = 4

# queue
NO_QUEUE    = 5
EMPTY_QUEUE = 6


# JSON
INDENT_SPACES = 4


# video editing
SUFFIX      = '.mp4'

FRAMES      = 60
VCODEC      = "libx264"
COMPRESSION = "slower"
ACODEC      = 'aac'
