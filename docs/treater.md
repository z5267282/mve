# Overview

Edit all videos according to the first enqueued treatment of the given configuration.  
The treatments are performed in the following order:

1. edits;
2. rename;
3. deletions.

Edits are placed in the given config's destination folder.  
Once the enqueued treatment has been processed, it is moved into the `history` folder of the given configuration.

# Usage

```sh
python3 -m mve log treater <config>`
```

# Errors

Errors if any, are logged in the given config's errors folder.  
When an error occurs, the file name of the offending treatment is re-appended to the remaining JSON file.  
After it has been rewatched in the viewer, it can also be re-treated upon the next viewing session.
