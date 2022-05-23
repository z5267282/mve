# overview
The config is a `.py` file with the following constants.  

Directories of the format `[ folder_1, folder_2, ... folder_n ]` .  
```py
SOURCE_PATH    # source files to be edited
RENAMES_PATH   # where renamed files are to be stored
```

Filenames containing the data for the following instructions with a `current/` structured folder.  
```py
EDITS
RENAMES
DELETIONS
```

Lastly, it contains the location of where the remaining files are to be taken from.  
```py
REMAINING
```
