# Overview

Edit all videos in a given folder, but do not create logs.  
In this mode, `deleter` is not run in case the videos have further use after editing.

Paths for folders can be entered as either command-line flags, or absolute paths as input prompts.

# Usage

```
usage: python3 -m mve no-log moment [-h] [--source SOURCE | --desktop]
                                    [--dest DEST | --downloads] [--recent]
                                    [--num-processes NUM_PROCESSES]
                                    [--use-moviepy]
                                    [--moviepy-threads MOVIEPY_THREADS]
                                    [--testing] [--bold] [--verify-name]

options:
  -h, --help            show this help message and exit
  --source SOURCE       the source folder
  --desktop             set the source folder as Desktop
  --dest DEST           the location of edits and renames
  --downloads           set the destination folder as Downloads

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

# Usage
