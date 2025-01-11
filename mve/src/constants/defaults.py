'''These defaults are used before a config has been successfully made by
its constructor (ie. some constructor invariants might fail.'''

# file-order generation
RECENT: bool = False

# multiprocessing
NUM_PROCESSES: int = 4

# moviepy
USE_MOVIEPY: bool = False
MOVIEPY_THREADS: int = 4

# testing
TESTING: bool = False

# colours
BOLD: bool = False

# whether to check if names start with leading numbers
VERIFY_NAME: bool = True
