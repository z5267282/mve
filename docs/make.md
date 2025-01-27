# Overview

Create a new configuration folder.  
The paths for the source videos, alongside the edits and rename folders must be provided.  
The paths can be provided as command-line argument flags.  
The user is prompted to enter all paths not provided on the command line.

Configuration names must be unique within `MVE_CONFIGS`.

# Naming

Configs can only contain letters or hyphens, ie `[a-z-]`.

# Usage

```
usage: python3 -m mve log make [-h] [--source SOURCE] [--renames RENAMES]
                               [--edits EDITS] [--recent]
                               [--num-processes NUM_PROCESSES] [--use-moviepy]
                               [--moviepy-threads MOVIEPY_THREADS] [--testing]
                               [--bold] [--verify-name]
                               config

options:
  -h, --help            show this help message and exit

make options:
  config                the name of the config to create
  --source SOURCE       the source folder of videos
  --renames RENAMES     the renames folder
  --edits EDITS         the folder where edited videos are stored

configuration options:
  --recent              store files from most to least recently created
  --num-processes NUM_PROCESSES
                        set the number of processes used in editing
  --use-moviepy         use moviepy to edit clips
  --moviepy-threads MOVIEPY_THREADS
                        use ffmpeg to edit clips
  --testing             turn on testing mode and do not open videos when the
                        viewer plays
  --bold                set colouring to bold
  --verify-name         double-check whether a clip name starting with a
                        number is not a timestamp
```

# Path Expansion

Tilde-based home expansion (`~`) is not supported for prompt-entered paths.  
It is recommended to provide these on the command line so that that the Shell can expand them instead:

```sh
python3 -m mve log make --source ~/Desktop
```

.
