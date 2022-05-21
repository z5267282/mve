# description
Start a new session to log desired video transformations.  

A new folder in `queue/` is created with the timestamp `current`-like folder structure.  

Can be run cross-platform
* Mac can only view on drive
* Windows can be viewed on drive or pc as specified by flag

# usage
```
python3 viewer.py [ [m]ac | [d]rive for windows | [p]c for windows ]
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
