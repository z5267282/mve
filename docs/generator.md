# Overview

Load all videos from a particular configuration and prepare them for viewing.

# File Order

Files are sorted by creation time.  
This can be modified in the `RECENT` configuration option.

# Usage

```sh
python3 -m mve log generator <config>
```

# Defences

It is expected that no source videos in the configuration are directly modified after the user.  
They can be entirely handled using the `mve` project.  
Accordingly, `generator` will not work if there are still files left in the configuration's `remaining.json`.
