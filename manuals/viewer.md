# description
Start a new session to log desired video transformations.  

A new folder in `queue/` is created with the timestamp `current`-like folder structure.  

# usage
```
python3 viewer.py
```

# command structure
```
[e]nd      | [ time <mm-ss> ]                   | edit from [ time ] to end of clip
[m]iddle   | [ start <mm-ss> ] [ end <mm-ss> ]  | edit from [ start ] to [ end ]
[c]ontinue |                                    | re-add the current clip so it can be transformed twice
[r]ename   | [ name ]                           | rename the clip to [ name ]
[d]elete   |                                    | delete the clip
[h]elp     |                                    | print this message
```
