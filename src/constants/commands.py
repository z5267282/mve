# command key mappings
END      = 'e'
START    = 's'
MIDDLE   = 'm'
RENAME   = 'r'
DELETE   = 'd'
CONTINUE = 'c'
QUIT     = 'q'
HELP     = 'h'

# number of tokens expected by commands that need extra arguments
NUM_TOKENS = {
    END    : 2,
    START  : 2,
    MIDDLE : 3,
    RENAME : 1,
}

# help message
MESSAGE = '''
[e]nd      | [ time ] [ name ]
    + edit from [ time ] to end of clip.
    + the time is in the form [ integer | timestamp in form <[hour]-min-sec> ]
    + the name can only contain upper and lowercase letters, digits and spacebars

[s]tart    | [ time ] [ name ]
    + edit from start to [ time ] of clip.
    + the time is in the form [ integer | timestamp in form <[hour]-min-sec> ]
    + the name can only contain upper and lowercase letters, digits and spacebars

[m]iddle   | [ start ] [ end ] [ name ]
    + edit from [ start ] to [ end ]
    + start and end are the form [ natural number | timestamp in form <[hour]-min-sec> ]
    + the name can only contain upper and lowercase letters, digits and spacebars

[r]ename   | [ name ]
    + rename the clip to [ name ]
    + the name can only contain upper and lowercase letters, digits and spacebars

[d]elete   |
    + delete the clip

[c]ontinue |
    + re-add the current clip so it can be transformed twice

[q]uit     |
    + quit the viewer and save a new treatment structured file to queue/

[h]elp     |
    + print this message
'''
