# mve
A movie editing tool using multiprocessing.  

This program can be run on Windows or Mac.  

The program requires at least `python 3.6` to ensure that dictionary insertion order is preserved.  

# 0 - file structure
```
mve/
    src/
        + config.py

        constants/
        helpers/

        + remaining.json

        + generator.py
        + viewer.py
        + treater.py
        + deleter.py
    errors/
    history/
    queue/
```

## 0.1 - `src/`
Where the script is to be run and all relevant code for the program is stored.  

### 0.1.1 - `src/config.py`
A `.py` file containing constants that can be changed each time the program is run.  

The editing can either be done with `ffmpeg` or `MoviePy` .  
+ This is controlled by the value of `USE_MOVIEPY` .  

In testing mode files are not opened in the `viewer` .  
+ Testing mode is toggled via `TESTING` .  

The boldness of colours can be toggled via `BOLD` .  

It should be imported with the following statement:  

```py
import config as cfg
```

For the remainder of the documentation will also follow this notation.  

### 0.1.2 - `src/constants/`
A folder documenting constants that **are not** to be changed.  
+ The main motivation is to avoid magic numbers

All files in this folder should be imported with one of the following 3 letter abreviations:  
```py
import constants.colour as clr
import constants.commands as cmd
import constants.error as err
import constants.errors_format as erf
import constants.file_structure as fst
import constants.generation as gen
import constants.json_settings as jsn
import constants.treatment_format as trf
import constants.video_editing as vde
```

Constants from these files will be referred to by these 3 letter abreviations for the remainder of the documentation.  

### 0.1.3 - `src/helpers/`
A folder containing `python3` helper functions.  

Any functions needed accross multiple files are placed in this folder.  

These should be imported as:  
```py
import helpers.file_name as file_name
```

### 0.1.4 - `src/remaining.json`
A `JSON` list that stores the remaining files to be edited.  

Each list item is a file name without a leading directory in the `cfg.SOURCE` folder.  
```
[
    <file name>
]
```

## 0.2 - `errors/`
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
            erf.ERROR_DATA      : [ original data if any | null ]
        }
    ],
    erf.ERRORS_PATHS : {
        trf.SOURCE_PATH      : [ list of folders of the path where videos are sourced from ],
        trf.RENAME_PATH      : [ list of folders of the path where renames are to be placed ],
        trf.DESTINATION_PATH : [ list of folders of the path where edits are to be placed ]
    }
}
```

## 0.3 - `history/`
A folder storing past `treatment` - structured files from `queue/` .  

## 0.4 - `queue/`
A folder which contains a list of `treatment` - structured `JSON` files.  

### `treatment` structure
A `JSON` dictionary that stores instructions for how files are to be treated.  

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

### `[ structure ]` for `trf.EDITS`
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


# Style
## Import blocks
All blocks of imports are written in alphabetical order.  
A single newline separates import blocks

Standard libraries are imported first.  
Then import blocks are ordered the following way if used:  
1. `config`
2. `constants`
3. `helpers`

## Body
The code body begins with a double newline beneath the last import.  

All the following programs have a `main()` function.  
Helper functions of main are separated by a double newline.  
Functions are thereafter written in stack order:  

```
    def main():
        A()
        B()


    def A():
        b()
        d()

    def b():
        c()

    def c()

    def d():
        ...


    def B():
        ...
```

All files end with a lone newline.  

# 1 - generator
## usage
```
python3 generator.py
```

## overview
The generator will get the file names inside `cfg.SOURCE` and store them inside `remaining.json` .  
+ File names **without** leading folders are stored

If `cfg.SOURCE` does not exist the program terminates with exit code `err.NO_SOURCE_FOLDER` .  

If `remaining.json` does exist, and the list it contains is not empty, the program terminates with exit code `err.FILES_REMAINING` .  

If `remaining.json` does not exist, it is **created**.  

If the list is empty, it is **overwritten**.  

Files are stored from most recent to least recent.  
+ This can be toggled via `gen.RECENT`

# 2 - viewer
## usage
```
python3 viewer.py
```

## overview
The viewer is a program that will sequentially view all files in `remaining.json`.  

If `remaining.json` doesn't exist the program terminates with exit code `err.MISSING_REMAINING` .  

When the viewer is run files are sequentially opened for viewing in from the list inside of `remaining.json`.  

The file name is displayed as a prompt, but the program joins this file name with the folder `cfg.SOURCE` to locate the file.  
+ The program terminates with exit code `err.NO_SOURCE_FOLDER` if this folder does not exist

If `queue/` doesn't exist then the program terminates with exit code `err.NO_QUEUE`.  

Upon viewing a video, the user enters one of the following commands which are then stored in `queue/` in a `treatment` - like structure.
+ If no treatment commands (as opposed to control flow commands) were entered, then then no file is created

The folder paths to the source, renames and destination folders are logged in a viewing session for use by the treater.  
Hence if one of the following folders does not exist, the viewier will exit with the corresponding exit code:  
```
cfg.SOURCE      -> err.NO_SOURCE_FOLDER
cfg.RENAMES     -> err.NO_RENAMES_FOLDER
cfg.DESTINATION -> err.NO_DESTINATION_FOLDER
```

## commands
```
[e]nd      | [ start ] [ name ]
    + edit from [ start ] to end of clip.
    + the time is in the form [ integer | timestamp in form <[hour]-min-sec> ]
    + the name can only contain upper and lowercase letters, digits and spacebars

[s]tart    | [ end ] [ name ]
    + edit from start to [ time ] of clip.
    + the time is in the form [ integer | timestamp in form <[hour]-min-sec> ]
    + the name can only contain upper and lowercase letters, digits and spacebars

[m]iddle   | [ start ] [ end ] [ name ]
    + edit from [ start ] to [ end ]
    + start and end are the form [ natural number | timestamp in form <[hour]-min-sec> ]
    + the name can only contain upper and lowercase letters, digits and spacebars

[w]hole    | [ name ]
    + edit the entire clip from start to end
    + like running [ s 0 ] 
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
3. [ when applicable ] New name does not exist in the output folder
4. [ when applicable ] Timestamps in bounds of the video

# 3 - treater
## usage
```
python3 treater.py
```

## overview
The treater will read the earliest created file in `queue/` and use it to apply transformations.  

If `queue/` doesn't exist then the program terminates with exit code `err.NO_QUEUE`.  

If `queue/` is empty then the program terminates with exit code `err.EMPTY_QUEUE`.  

All files will need to be joined together with folder `cfg.SOURCE`.  
+ So the program terminates with exit code `err.NO_SOURCE_FOLDER` if this folder does not exist

If `cfg.RENAMES` does not exist the program terminates with exit code `err.NO_RENAMES_FOLDER`.  

The treatments are performed in the following order:  
1. edits
2. renames
3. deletions

Edits are placed in `cfg.DESTINATION` .  
+ So the program terminates with exit code `err.NO_DESTINATION_FOLDER` if this folder does not exist

Once the treatments are completed, the earliest file in `queue` is moved to `history/` .  
+ If `history/` doesn't exist the program terminates with exit code `err.NO_HISTORY_FOLDER` .  

Errors if any, are logged in `errors/` with its matching file structures.  
+ If `errors/` doesn't exist the program terminates with exit code `err.NO_ERRORS_FOLDER` .  

When an error occurs, the file name of the offending treatment is appended to `remaining.json` , so that it can be re-treated upon the next viewing session
+ The error is then logged
+ The program terminates with exit code `err.TREATMENT_ERROR`

Multiprocessing occurs for the editing stage and the number of processes can be changed in `cfg.NUM_PROCESSES` .  

The number of threads per editing process can be changed in `cfg.NUM_THREADS` .  

# 4 - deleter
## usage
```
python3 deleter.py
```

## overview
The deleter deletes the folder `cfg.SOURCE` .  

If `remaining.json` exists and contains a non-empty list, the program terminates with exit code `err.FILES_REMAINING` .  

If `cfg.SOURCE` doesn't exist then the program teriminates with exit code `err.NO_SOURCE_FOLDER` .  

## 5 - swapper
## usage
```
python3 swapper.py [config name]
```

The swapper is used to change between config files.  

Config files should be named in a folder within `src/configs` and contain a separate
```
+ config.py
+ remaining.json
```

The current config is maintained as a string in `src/current.json` .  

The swapper moves `config.py` and `remaining.json` of the given config into `src` .  

The new config can be the same as the old one.  

If `src/configs` doesn't exist the program terminates with exit code `err.NO_CONFIGS_FOLDER` .  

If the given config doesn't exist the program term terminates with exit code `err.NO_CONFIG` .  
