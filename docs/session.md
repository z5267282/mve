# Remaining Files

A `JSON` list that stores the remaining files to be edited is stored in `remaining.json` of the given config.  
Each list item is a file name without a leading directory in the given config's source folder.

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
    errors_format.ERRORS_VIDEOS : [
        {
            errors_format.ERROR_FILE_NAME : [ file name ],
            errors_format.ERROR_MESSAGE   : [ error message ],
            errors_format.ERROR_COMMAND   : [ treatment_format.EDITS | treatment_format.RENAMES | treatment_format.DELETIONS ],
            errors_format.ERROR_DATA      : [ error message ]
        }
    ],
    errors_format.ERRORS_PATHS : {
        treatment_format.SOURCE_PATH      : [ list of folders of the path where videos are sourced from ],
        treatment_format.RENAME_PATH      : [ list of folders of the path where renames are to be placed ],
        treatment_format.DESTINATION_PATH : [ list of folders of the path where edits are to be placed ]
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
    treatment_format.EDITS : [
        {
                treatment_format.EDIT_ORIGINAL : [ original file name ],
                treatment_format.EDIT_NAME     : [ file name ],
                treatment_format.EDIT_TIMES    : [ [ structure ] ]
        }
    ],
    treatment_format.RENAMES : {
        <file name> : <new file name>
    },
    treatment_format.DELETIONS : [
        <file name>
    ],
    treatment_format.PATHS : {
        treatment_format.SOURCE_PATH      : [ list of folders of the path where videos are sourced from ],
        treatment_format.RENAME_PATH      : [ list of folders of the path where renames are to be placed ],
        treatment_format.DESTINATION_PATH : [ list of folders of the path where edits are to be placed ]
    }
}
```

# Edits

The values for `treatment_format.EDITS` are complex based on the edit command and hence they have been listed here:

```
commands.END = {
    treatment_format.EDIT_TIMES_START : [ integer | timestamp in the form <[hh:]mm:ss> ],
    trd.EDIT_TIMES_END   : null
}

commands.START = {
    treatment_format.EDIT_TIMES_START : null,
    trd.EDIT_TIMES_END   : [ natural number | timestamp in the form <[hh:]mm:ss> ]
}

commands.MIDDLE = {
    treatment_format.EDIT_TIMES_START : [ natural number | timestamp in the form <[hh:]mm:ss> ],
    trd.EDIT_TIMES_END   : [ natural number | timestamp in the form <[hh:]mm:ss> ]
}

commands.WHOLE = {
    treatment_format.EDIT_TIMES_START : null,
    trd.EDIT_TIMES_END   : null
}
```
