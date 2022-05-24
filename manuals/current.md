# overview
a folder with 3 JSON files structured like so.  

## edits.json
```
[
    'name': {
        'new name': ' [ new name ] ',
        'times': [ time[s] in form <mm:ss> ]
    }
]
```

## renames.json
```
[
    'name': ' [ new name ] '
]
```

## deletions.json
```
[
    'name'
]
```

# errors.json
All errors are logged in the form:  
```
[
    'name': {
        'error': ' [ error ] ',
        'original': ( original data in whatever form it was stored as )
    }
]
