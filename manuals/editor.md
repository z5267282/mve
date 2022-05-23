# description
Perform all transformations described in the earliest dated folder of `queue/` .  
The transformations are as follows:  
```
[e]dit
[r]ename
[d]elete
```
* Edit mode makes use of multiprocessing

If there are any folders in `errors/` , the earliest folder here is taken instead of any in `queue` .  

# usage
```
python3 editor.py 
```

# errors
Errors that occur in the editing phase are placed in a `current/` - structured folder in `errors/` .
