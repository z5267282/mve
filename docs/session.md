# Remaining Files

A `JSON` list that stores the remaining files to be edited is stored in `remaining.json` of the given config.  
Each list item is a file name without a leading directory in the `cfg.SOURCE` folder:

```
[
    <file name>
]
```

# File Structure

The `viewer.py` script will transform all commands into a JSON file with the following keys.

# Errors

A folder containing all recorded errors whilst completing the treatments.  
All files are named with a timestamp in the form `DD.MM.YYYY - hhmm`.  
It is a `JSON` dictionary where each key is structured in the following way.  
File names could be duplicated and hence a list of objects is used.

```
{
    erf.ERRORS_VIDEOS : [
        {
            erf.ERROR_FILE_NAME : [ file name ],
            erf.ERROR_MESSAGE   : [ error message ],
            erf.ERROR_COMMAND   : [ trf.EDITS | trf.RENAMES | trf.DELETIONS ],
            erf.ERROR_DATA      : [ error message ]
        }
    ],
    erf.ERRORS_PATHS : {
        trf.SOURCE_PATH      : [ list of folders of the path where videos are sourced from ],
        trf.RENAME_PATH      : [ list of folders of the path where renames are to be placed ],
        trf.DESTINATION_PATH : [ list of folders of the path where edits are to be placed ]
    }
}
```

# Treatment File Structure

Treatments are stored as a JSON dictionary.  
All files with a `treatment` structure are named with a timestamp in the form `DD.MM.YYYY - hhmm` .  
All file names do not have a leading directory.  
There can be multiple edit commands with the same file name.

```
{
    trf.EDITS : [
        {
                trf.EDIT_ORIGINAL : [ original file name ],
                trf.EDIT_NAME     : [ file name ],
                trf.EDIT_TIMES    : [ [ structure ] ]
        }
    ],
    trf.RENAMES : {
        <file name> : <new file name>
    },
    trf.DELETIONS : [
        <file name>
    ],
    trf.PATHS : {
        trf.SOURCE_PATH      : [ list of folders of the path where videos are sourced from ],
        trf.RENAME_PATH      : [ list of folders of the path where renames are to be placed ],
        trf.DESTINATION_PATH : [ list of folders of the path where edits are to be placed ]
    }
}
```

# Edits

The values for `trf.EDITS` are complex based on the edit command and hence they have been listed here:

```
cmd.END = {
    trf.EDIT_TIMES_START : [ integer | timestamp in the form <[hh:]mm:ss> ],
    trd.EDIT_TIMES_END   : null
}

cmd.START = {
    trf.EDIT_TIMES_START : null,
    trd.EDIT_TIMES_END   : [ natural number | timestamp in the form <[hh:]mm:ss> ]
}

cmd.MIDDLE = {
    trf.EDIT_TIMES_START : [ natural number | timestamp in the form <[hh:]mm:ss> ],
    trd.EDIT_TIMES_END   : [ natural number | timestamp in the form <[hh:]mm:ss> ]
}

cmd.WHOLE = {
    trf.EDIT_TIMES_START : null,
    trd.EDIT_TIMES_END   : null
}
```
