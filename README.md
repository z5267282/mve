# mve
A movie editing tool using multiprocessing.  

This program can only be run on Windows.  

# 0 - file structure

# 0.1 - `remaining.json`
A `JSON` list that stores the remaining files to be edited.  

Each list item is a file name without a leading directory in the `SOURCE` folder.  
```
[
    [ file path ]
]
```

## 0.1 

# 1 - viewer
The viewer is a program that will sequentially view all files in `remaining.json`.  

If `remaining.json` doesn't exist the program terminates with exit code 1.  
