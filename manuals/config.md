# overview
The config is a `.py` file with the following constants.  

# editing folders
Directories of the format `[ folder_1, folder_2, ... folder_n ]` .  
```py
SOURCE_PATH  # source files to be edited
RENAMES_PATH # where renamed files are to be stored
```

# log folders
Names of directories within the repository's root to store treatments.  
```py
QUEUE
HISTORY
ERRORS
```

# current files
Filenames containing the data for the following instructions with a `current/` structured folder.  
```py
EDITS
RENAMES
DELETIONS
```

# other files
Where remaining files are to be taken from.  
```py
REMAINING
```

# edit structure keys inside `current/`
`edit.json` is the only file (apart from `errors/`) which has JSON objects that require keys.  
```py
EDIT_NEW_NAME
EDIT_TIMES
```

# multiprocessing
```py
NUM_THREADS   # number of threads per edit
NUM_PROCESSES # number of processes to perform video editing
```
