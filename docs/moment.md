# Overview

Edit all videos in a given folder, but do not create logs.  
In this mode, `deleter` is not run in case the videos have further use after editing.

Paths for folders can be entered as either command-line flags, or absolute paths as input prompts.

# Usage

```sh
python3 -m mve no-log moment [--info] [--source SOURCE | --desktop] [--dest DEST | --downloads]
  --info
  --source SOURCE  the source folder
  --desktop        set the source folder as Desktop
  --dest DEST      the location of edits and renames
  --downloads      set the destination folder as Downloads
```
