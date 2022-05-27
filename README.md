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

For the remainder of the documentation, constants inside the config will be prefixed with `cfg.` .  

## 0.2 - `constants.py`
A `.py` file documenting constants that **are not** to be changed.  
* The main motivation is to avoid magic numbers

Similar to the config, it should be imported as:  
```py
import constants as cst
```

## 0.3 - `remaining.json`
A `JSON` list that stores the remaining files to be edited.  

Each list item is a `file name` without a leading directory in the `cfg.SOURCE` folder.  
```
[
    <file name>
]
```

## 0.4 - `treatment` structure
A `JSON` dictionary that stores instructions for how files are to be treated.  

All files with a `treatment` structure are named with a timestamp in the form `DD.MM.YYYY - hhmm` .  

All `file name` s do not have a leading directory.  
```
{
    cst.EDITS : {
        {
            <file name> : {
                cst.EDIT_NAME : [ file name ]
                cst.TIMES     : [ 1 integer | 2 (natural numbers | timestamp in form <min:sec>) ]
            }
        }
    },
    cst.RENAMES : {
        <file name> : <new file name>
    },
    cst.DELETIONS : [
        <file name>
    ],
    cst.SOURCE_PATH : [ list of folders in the source path ],
    cst.RENAME_PATH : [ list of folders in the edit path ]
}
```

## 0.5 - `queue/`
A folder which contains a list of `treatment` - structured `JSON` files.  

## 0.6 - `errors/`
A folder containing all recorded errors whilst completing the treatments.  

All files are named with a timestamp in the form `DD.MM.YYYY - hhmm`.  

It is a `JSON` dictionary where each key is structured in the following way.  
```
{
    <file name> : {
        cst.ERROR_COMMAND : [ cst.EDITS | cst.RENAMES | cst.DELETIONS ]
        cst.ERROR_DATA    : [ original data if any | null ]
    }
}
```

# 1 - generator
## usage
```
python3 generator.py
```

## overview
The generator will get the file names inside `cfg.SOURCE` and store them inside `remaining.json` .  

If `remaining.json` does not exist, it is **created**.  

If it does exist, and the list it contains is not empty, the program terminates with exit code `cst.FILES_REMAINING` .  
If the list is empty, it is **overwritten**.  

# 2 - viewer
## usage
```
python3 viewer.py
```

## overview
The viewer is a program that will sequentially view all files in `remaining.json`.  

If `remaining.json` doesn't exist the program terminates with exit code `cst.MISSING_REMAINING` .  

When the viewer is run files are sequentially opened for viewing in from the list inside of `remaining.json`.  

The file name is displayed as a prompt, but the program joins this file name with the folder `cfg.SOURCE` to locate the file.  
    + The program terminates with exit code `cst.NO_SOURCE_FOLDER` if this folder does not exist

## commands
```
[e]nd      | [ time ] [ name ]
    + edit from [ time ] to end of clip.
    + the time is in the form [ 1 integer | 2 (natural numbers | timestamp in form <min:sec>) ]
    + the name can only contain upper and lowercase letters, digits and spacebars

[m]iddle   | [ start ] [ end ] [ name ]
    + edit from [ start ] to [ end ]
    + start and end are the form [ 1 integer | 2 (natural numbers | timestamp in form <min:sec>) ]
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
1. Correctly formatted arguments
2. Clip timing (if relevant) against `moviepy.subclip()`

# 3 - treater
## usage
```
python3 treater.py
```

## overview
The treater will read the earliest created file in `queue` and use it to apply transformations.  

If `queue/` doesn't exist then the program terminates with exit code `cst.NO_QUEUE`.  

If `queue/` is empty then the program terminates with exit code `cst.EMPTY_QUEUE`.  

All files will need to be joined together with folder `cfg.SOURCE`.  
    + So the program terminates with error code `cst.NO_SOURCE_FOLDER` if this folder does not exist

If `cfg.RENAMES` does not exist the program terminates with error code `cst.NO_RENAMES_FOLDER`.  

The treatments are performed in the following order:  
1. edits
2. renames
3. deletions

Errors if any, are logged in `errors/` with its matching file structures.  

When an error occurs, the file name of the offending treatment is appended to `remaining.json` , so that it can be re-treated upon the next viewing session
    + The error is then logged

Multiprocessing occurs for the editing stage and the number of processes can be changed in `cfg.NUM_PROCESSES` .  

The number of threads per editing process can be changed in `cfg.NUM_THREADS` .  

# 4 - deleter
