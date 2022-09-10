# command key mappings
END      = 'e'
START    = 's'
MIDDLE   = 'm'
WHOLE    = 'w'
RENAME   = 'r'
DELETE   = 'd'
CONTINUE = 'c'
QUIT     = 'q'
HELP     = 'h'

USAGE_MSGS = {
    END      : '[e]nd      | [ start ] [ name ]',
    START    : '[s]tart    | [ end ] [ name ]',
    MIDDLE   : '[m]iddle   | [ start ] [ end ] [ name ]',
    WHOLE    : '[w]hole    | [ name ]',
    RENAME   : '[r]ename   | [ name ]',
    DELETE   : '[d]elete   |',
    CONTINUE : '[c]ontinue |',
    QUIT     : '[q]uit     |',
    HELP     : '[h]elp     |',
}

# number of tokens expected by commands that need extra arguments
NUM_TOKENS = {
    END    : 2,
    START  : 2,
    MIDDLE : 3,
    WHOLE  : 1,
    RENAME : 1
}

# help message
HELP_MESSAGE = '''
{}
    + edit from [ start ] to end of clip.
    + the time is in the form [ integer | timestamp in form <[hour]-min-sec> ]
    + the name can only contain upper and lowercase letters, digits and spacebars

{}
    + edit from start to [ time ] of clip.
    + the time is in the form [ integer | timestamp in form <[hour]-min-sec> ]
    + the name can only contain upper and lowercase letters, digits and spacebars

{}
    + edit from [ start ] to [ end ]
    + start and end are the form [ natural number | timestamp in form <[hour]-min-sec> ]
    + the name can only contain upper and lowercase letters, digits and spacebars

{}
    + edit the entire clip from start to end
    + like running [ s 0 ] 
    + the name can only contain upper and lowercase letters, digits and spacebars

{}
    + rename the clip to [ name ]
    + the name can only contain upper and lowercase letters, digits and spacebars

{}
    + delete the clip

{}
    + re-add the current clip so it can be transformed twice

{}
    + quit the viewer and save a new treatment structured file to queue/

{}
    + print this message
'''.format(
    *USAGE_MSGS.values()
)
