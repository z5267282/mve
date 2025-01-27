# Overview

A session is one execution of the `viewer` script.  
In a session, videos are played in order and any files still remaining are recorded for the next session.

# Remaining Files

A `JSON` list that stores the remaining files to be edited is stored in `remaining.json` of the given config.  
Each list item is a file name without a leading directory in the given config's source folder.

```json
["<file name...>"]
```

# Treatments

All edits are treated, then all renames and all deletions.  
Errors if any are logged in a file \(see #Errors\), in the order they appeared in the treatment file.

# Treatment File Structure

Treatments are stored as a JSON dictionary.  
All files with a `treatment` structure are named with a timestamp in the form `DD.MM.YYYY - hhmm` .  
All file names do not have a leading directory.  
There can be multiple edit commands with the same file name.

```json
{
  "edits": [
    {
      "original": "<original file name>",
      "new name": "<new file name>",
      "times": "<edits structure>"
    }
  ],
  "renames": {
    "<file name>": "<new file name>"
  },
  "deletions": ["<file name...>"],
  "paths": {
    "source path": "<list of folders of the path where videos are sourced from>",
    "renames path": "<list of folders of the path where renames are to be placed>",
    "destination path": "<list of folders of the path where edits are to be placed>"
  }
}
```

## Edits

The values for the `edits` key are complex based on the edit command and hence they have been listed here:

```json
{
  "e": {
    "start": "<integer | timestamp in the form [hh:]mm:ss>",
    "end": null
  },
  "s": {
    "start": null,
    "end": "<natural number | timestamp in the form [hh:]mm:ss"
  },
  "m": {
    "start": "<natural number | timestamp in the form [hh:]mm:ss>",
    "end": "<natural number | timestamp in the form [hh:]mm:ss>"
  },
  "w": {
    "start": null,
    "end": null
  }
}
```

# Errors

A folder containing all recorded errors whilst completing the treatments.  
All files are named with a timestamp in the form `DD.MM.YYYY - hhmm`.  
It is a `JSON` dictionary where each key is structured in the following way.  
File names could be duplicated and hence a list of objects is used.

```json
{
  "files": [
    {
      "file name": "<file name>",
      "message": "<error message>",
      "error": "edits|renames|deletions",
      "data": "<information>"
    }
  ],
  "paths": {
    "source path": "<list of folders of the path where videos are sourced from>",
    "renames path": "<list of folders of the path where renames are to be placed>",
    "destination path": "<list of folders of the path where edits are to be placed>"
  }
}
```

Error files are re-appended to the configuration's remaining files so that they can be re-treated.
