# Overview

Focus mode lets you edit one file continuously.
It should be used for making montages of one video.

# Usage

Provide the absolute path to the video as a command line argument.

```
python3 focus.py <absolute file path>
```

All edits will be put in `~/Downloads`
In focus mode you can only enter middle commands.

```
> 1-30 1-35
```

The name of the edit will be the two timestamps.
To override this behaviour you can add a `--name` flag and then specify the name of the file.

```
> --name 'special moment' 1-30 1-35
```
