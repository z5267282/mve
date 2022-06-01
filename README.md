# mve
A movie editing tool using multiprocessing.  

This program can only be run on Windows.  

# 0 - file structure

## 0.1 - `config.py`
A `.py` file containing constants that can be changed each time the program is run.  

It should be imported with the following statement:  

```py
import config as cfg
```

For the remainder of the documentation will also follow this notation.  

## 0.2 - `src/constants/`
A folder documenting constants that **are not** to be changed.  
+ The main motivation is to avoid magic numbers

All files in this folder should be imported with one of the following 3 letter abreviations:  
```py
import constants.commands as cmd
import constants.error as err
import constants.errors_format as erf
import constants.file_structure as fst
import json_settings as jsn
import treatment_format as trf
import video_editing as vde
```

## 0.3 - `src/helpers/`
A folder containing `python3` helper functions.  

Any functions needed accross multiple files are placed in this folder.  

These should be imported as:  
```py
import helpers.file_name as file_name
```

## 0.4 - `remaining.json`
A `JSON` list that stores the remaining files to be edited.  

Each list item is a file name without a leading directory in the `cfg.SOURCE` folder.  
```
[
    <file name>
]
```

## 0.5 - `treatment` structure
A `JSON` dictionary that stores instructions for how files are to be treated.  

All files with a `treatment` structure are named with a timestamp in the form `DD.MM.YYYY - hhmm` .  

All file names do not have a leading directory.  
```
{
    trf.EDITS : {
        {
            <file name> : {
                trf.EDIT_NAME : [ file name ]
                trf.TIMES     : [ 1 integer | 2 (natural numbers | timestamp in form <min:sec>) ]
            }
        }
    },
    trf.RENAMES : {
        <file name> : <new file name>
    },
    trf.DELETIONS : [
        <file name>
    ],
    trf.SOURCE_PATH : [ list of folders in the source path ],
    trf.RENAME_PATH : [ list of folders in the edit path ]
}
```

## 0.6 - `queue/`
A folder which contains a list of `treatment` - structured `JSON` files.  

## 0.7 - `history/`
A folder storing past `treatment` - structured files from `queue` .  

## 0.8 - `errors/`
A folder containing all recorded errors whilst completing the treatments.  

All files are named with a timestamp in the form `DD.MM.YYYY - hhmm`.  

It is a `JSON` dictionary where each key is structured in the following way.  
```
{
    erf.ERRORS_VIDEOS : {
        <file name> : {
            erf.ERROR_COMMAND : [ trf.EDITS | trf.RENAMES | trf.DELETIONS ]
            erf.ERROR_DATA    : [ original data if any | null ]
        }
    },
    erf.ERRORS_PATHS : {
        trf.SOURCE_PATH : [ list of folders in the source path ],
        trf.RENAME_PATH : [ list of folders in the edit path ] }
}
```

# 1 - generator
## usage
```
python3 generator.py
```

## overview
The generator will get the file names inside `cfg.SOURCE` and store them inside `remaining.json` .  
+ File names **without** leading folders are stored

If cfg.SOURCE does not exist the program terminates with exit code `NO_SOURCE_FOLDER` .  

If `remaining.json` does exist, and the list it contains is not empty, the program terminates with exit code `FILES_REMAINING` .  

If `remaining.json` does not exist, it is **created**.  

If the list is empty, it is **overwritten**.  

# 2 - viewer
## usage
```
python3 viewer.py
```

## overview
The viewer is a program that will sequentially view all files in `remaining.json`.  

If `remaining.json` doesn't exist the program terminates with exit code `ern.MISSING_REMAINING` .  

When the viewer is run files are sequentially opened for viewing in from the list inside of `remaining.json`.  

The file name is displayed as a prompt, but the program joins this file name with the folder `cfg.SOURCE` to locate the file.  
+ The program terminates with exit code `ern.NO_SOURCE_FOLDER` if this folder does not exist

Upon viewing a video, the user enters one of the following commands which are then stored in `queue/` in a `treatment` - like structure.
+ If no treatment commands (as opposed to control flow commands) were entered, then then no file is created

## commands
```
[e]nd      | [ time ] [ name ]
    + edit from [ time ] to end of clip.
    + the time is in the form [ integer | timestamp in form <min-sec>) ]
    + the name can only contain upper and lowercase letters, digits and spacebars

[m]iddle   | [ start ] [ end ] [ name ]
    + edit from [ start ] to [ end ]
    + start and end are the form [ natural number | timestamp in form <min-sec>) ]
    + the name can only contain upper and lowercase letters, digits and spacebars

[r]ename   | [ name ]
    + rename the clip to [ name ]
    + the name can only contain upper and lowercase letters, digits and spacebars

[d]elete   |
    + delete the clip

[c]ontinue |
    + re-add the current clip so it can be transformed twice

[q]uit     |
    + quit the viewer and save a new treatment structured file to queue/

[h]elp     |
    + print this message
```

## errors
Errors are dealt with immediately.  

If an error occurs nothing is logged and the video is reshown, with input also being re-asked.  

The following errors are checked against:  
1. Correct number of arguments
2. Correctly formatted arguments

# 3 - treater
## usage
```
python3 treater.py
```

## overview
The treater will read the earliest created file in `queue` and use it to apply transformations.  

If `queue/` doesn't exist then the program terminates with exit code `ern.NO_QUEUE`.  

If `queue/` is empty then the program terminates with exit code `ern.EMPTY_QUEUE`.  

All files will need to be joined together with folder `cfg.SOURCE`.  
    + So the program terminates with exit code `ern.NO_SOURCE_FOLDER` if this folder does not exist

If `cfg.RENAMES` does not exist the program terminates with exit code `ern.NO_RENAMES_FOLDER`.  

The treatments are performed in the following order:  
1. edits
2. renames
3. deletions

Once the treatments are completed, the earliest file in `queue` is moved to `history/` .  

Errors if any, are logged in `errors/` with its matching file structures.  

When an error occurs, the file name of the offending treatment is appended to `remaining.json` , so that it can be re-treated upon the next viewing session
+ The error is then logged

Multiprocessing occurs for the editing stage and the number of processes can be changed in `cfg.NUM_PROCESSES` .  

The number of threads per editing process can be changed in `cfg.NUM_THREADS` .  

# 4 - deleter
## overview
The deletor deletes the folder `cfg.SOURCE` .  

If `remaining.json` exists and contains a non-empty list, the program terminates with exit code `ern.FILES_REMAINING` .  

If `cfg.SOURCE` doesn't exist then the program teriminates with exit code `ern.NO_SOURCE_FOLDER` .  

## usage
```
python3 deleter.py
```
