# Overview

Focus mode lets you edit one file continuously.  
It should be used for making montages of one video.  
All edits will be put in `~/Downloads`.

# Usage

```
python3 -m mve no-log focus [--destination DESTINATION] source
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
