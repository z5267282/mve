# mve
A movie editing tool using multiprocessing.

# directory structure
```
src/
    + editor.py
    + viewer.py
    + config.json

current/ # a folder named by a DD/MM/YYYY - HHMM timestamp
    + edits.json
    + renames.json
    + deletions.json

queue/
    + [ current/ structured folder ]
    ...

history/
    + [ current/ structured folder ]
    ...

errors/
    + [ current/ structured folder ]
    ...

```
