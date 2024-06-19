# Overview

A command-line video-editing program.  
First view videos to determine suitable timestamps to create cuts.  
Then, the program will edit the videos accordingly.

# Instructions

The project can be run in a stateful or stateless mode, depending on whether records should be kept.

## 1. Stateful Mode

To edit and record a history of treatments, run these `src/*.py` scripts in this order:

| no. | script         | description                                                                |
| --- | -------------- | -------------------------------------------------------------------------- |
| 1.  | `make.py`      | generate a new configuration in the project history                        |
| 2.  | `generator.py` | populate the config's remaining video list                                 |
| 3.  | `viewer.py`    | view each remaining video in the config, record treatments and enqueue     |
| 4.  | `treater.py`   | perform all treatments on the first enqueued treatment file for the config |
| 5.  | `deleter.py`   | mark the config as complete and delete its source folder                   |

Each script should be run with these this argument:

```sh
python3 script.py config
```

All scripts can be run on a docker container with the exception of **`make.py`** as it requires OS-specific path information.

## 2. Stateless Mode

Run `moment.py` to run treatments without recording history.  
You will be prompted to enter a source folder and then view videos.  
Once all videos have been viewed and recorded with a treatment, editing occurs immediately thereafter.

In stateless mode, the config is based on `constants.defaults`.

# History Structure

A folder with the following structure will store all editing history:

```
config/
    errors/
    history/
    queue/

    + remaining.json
    + config.json
```

## Environment Variable

The environment variable `MVE_CONFIGS` should store the full path to the history folder.  
If it is not set, it will default to the parent folder of the `mve` repository (ie. `..`).

## Integrity

Run `integrity.py` to verify that the history folder follows the correct structure.

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

## Errors

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

## Treatment File Structure

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

## Edits

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
