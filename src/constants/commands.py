# command key mappings
END: str = 'e'
START: str = 's'
MIDDLE: str = 'm'
WHOLE: str = 'w'
RENAME: str = 'r'
DELETE: str = 'd'
CONTINUE: str = 'c'
QUIT: str = 'q'
HELP: str = 'h'

USAGE_MSGS: dict[str, str] = {
    END: '[e]nd      | [ start ] [ name ]',
    START: '[s]tart    | [ end ] [ name ]',
    MIDDLE: '[m]iddle   | [ start ] [ end ] [ name ]',
    WHOLE: '[w]hole    | [ name ]',
    RENAME: '[r]ename   | [ name ]',
    DELETE: '[d]elete   |',
    CONTINUE: '[c]ontinue |',
    QUIT: '[q]uit     |',
    HELP: '[h]elp     |',
}

# number of tokens expected by commands that need extra arguments
NUM_TOKENS: dict[str, int] = {
    END: 2,
    START: 2,
    MIDDLE: 3,
    WHOLE: 1,
    RENAME: 1
}

# help message
HELP_MESSAGE: str = f'''
{{{END}}}
    + edit from [ start ] to end of clip.
    + the time is in the form [ integer | timestamp in form <[hour]-min-sec> ]
    + the name can only contain upper and lowercase letters, digits and spacebars

{{{START}}}
    + edit from start to [ time ] of clip.
    + the time is in the form [ integer | timestamp in form <[hour]-min-sec> ]
    + the name can only contain upper and lowercase letters, digits and spacebars

{{{MIDDLE}}}
    + edit from [ start ] to [ end ]
    + start and end are the form [ natural number | timestamp in form <[hour]-min-sec> ]
    + the name can only contain upper and lowercase letters, digits and spacebars

{{{WHOLE}}}
    + edit the entire clip from start to end
    + like running [ s 0 ]
    + the name can only contain upper and lowercase letters, digits and spacebars

{{{RENAME}}}
    + rename the clip to [ name ]
    + the name can only contain upper and lowercase letters, digits and spacebars

{{{DELETE}}}
    + delete the clip

{{{CONTINUE}}}
    + re-add the current clip so it can be transformed twice

{{{QUIT}}}
    + quit the viewer and save a new treatment structured file to queue/

{{{HELP}}}
    + print this message
'''.format_map(USAGE_MSGS)
