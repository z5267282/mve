# Overview

Create a new configuration folder.  
The paths for the source videos, alongside the edits and rename folders must be provided.  
The paths can be provided as command-line argument flags.  
The user is prompted to enter all paths not provided on the command line.

Configuration names must be unique within `MVE_CONFIGS`.

# Naming

Configs can only contain letters or hyphens, ie `[a-z-]`.

# Usage

# Path Expansion

Tilde-based home expansion (`~`) is not supported for prompt-entered paths.  
It is recommended to provide these on the command line so that that the Shell can expand them instead:

```sh
python3 -m mve log make --source ~/Desktop
```

.
