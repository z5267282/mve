# editing folders
SOURCE_PATH  = ['D:', 'Videos', 'Batches', '1']
RENAMES_PATH = ['D:', 'Videos', 'Renames']

# log folders
QUEUE   = 'queue'
HISTORY = 'history'
ERRORS  = 'errors'

# current files
EDITS     = 'edits.json'
RENAMES   = 'renames.json'
DELETIONS = 'deletions.json'

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