# Overview

A command-line video-editing program.  
First view videos to determine suitable timestamps to create cuts.  
Then, the program will edit the videos accordingly.

# Instructions

The project can be run in a stateful or stateless mode, depending on whether records should be kept.

## 1. Stateful

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

## 2. Stateless

For one-off editing where history is not needed, the following scripts can be run.

| script       | description                                             |
| ------------ | ------------------------------------------------------- |
| `moment.py`  | make edits for all videos from a particular folder      |
| `focus.py`   | continuously make clips of a particular video           |
| `combine.py` | join all clips from a folder into a single complication |

# Environment Variable

The environment variable `MVE_CONFIGS` should store the full path to the folder storing configurations.  
If it is not set, it will default to the parent folder of the `mve` repository (ie. `..`).

# Documentation Guide

Documentation for specific parts of the project are in the `docs/` folder.

| file         | description                                 |
| ------------ | ------------------------------------------- |
| `configs.md` | structure of a configuration folder         |
| `session.md` | how a viewing session is stored and treated |
