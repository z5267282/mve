# Overview

Focus mode lets you edit one file continuously.  
It should be used for making montages of one video.  
All edits will be put in `~/Downloads`.

# Usage

```
usage: focus [-h] [--destination DESTINATION] [--recent]
             [--num-processes NUM_PROCESSES] [--use-moviepy]
             [--moviepy-threads MOVIEPY_THREADS] [--testing] [--bold]
             [--verify-name]
             source

options:
  -h, --help            show this help message and exit

focus options:
  source
  --destination DESTINATION

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

# Commands

## Editing

In focus mode you can only enter middle commands:

```
<[hh]-mm-ss> <[hh]-mm-ss>
```

The name of the edit will be the two timestamps.  
To override this behaviour you can add a `--name` flag and then specify the name of the file eg:

```
--name 'special moment' 1-30 1-35
```

## Quitting

Enter `q` to quit the program.
