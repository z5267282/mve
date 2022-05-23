# mve
A movie editing tool using multiprocessing.  

This program can only be run on Windows.  

# directory structure
```
src/
    + editor.py
    + viewer.py
    + helper.py
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
    + [ current/ - like structured folder ]
    ...
```
