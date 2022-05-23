# description
Start a new session to log desired video transformations.  

A new folder in `queue/` is created with the timestamp `current`-like folder structure.  

# usage
```
python3 viewer.py 
```

# command structure
```
[e]nd      | [ time ] [ name ]          | edit from [ time ] to end of clip
[m]iddle   | [ start ] [ end ] [ name ] | edit from [ start ] to [ end ]
[r]ename   | [ name ]                   | rename the clip to [ name ]
[d]elete   |                            | delete the clip
[c]ontinue |                            | re-add the current clip so it can be transformed twice
[h]elp     |                            | print this message
```

# errors
In the case of an error, input is immediately asked again.  
The following errors are checked against