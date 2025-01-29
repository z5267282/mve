from mve.src.constants.patterns import INTEGER_SECONDS, TIMESTAMP, \
    TREATED_FILE_NAME

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

INTEGER_SECONDS_OR_TIMESTAMP_DESCRIPTION: str = '[ {} ]'.format(
    " | ".join(
        [INTEGER_SECONDS.description, TIMESTAMP.description]
    )
)

# help message
HELP_MESSAGE: str = f'''{{{END}}}
    + edit from [ start ] to end of clip.
    + the time is in the form {INTEGER_SECONDS_OR_TIMESTAMP_DESCRIPTION} 
    + {TREATED_FILE_NAME.description}

{{{START}}}
    + edit from start to [ time ] of clip.
    + the time is in the form {INTEGER_SECONDS_OR_TIMESTAMP_DESCRIPTION} 
    + {TREATED_FILE_NAME.description}

{{{MIDDLE}}}
    + edit from [ start ] to [ end ]
    + start and end are the form {INTEGER_SECONDS_OR_TIMESTAMP_DESCRIPTION} 
    + {TREATED_FILE_NAME.description}

{{{WHOLE}}}
    + edit the entire clip from start to end
    + like running [ s 0 ]
    + {TREATED_FILE_NAME.description}

{{{RENAME}}}
    + rename the clip to [ name ]
    + {TREATED_FILE_NAME.description}

{{{DELETE}}}
    + delete the clip

{{{CONTINUE}}}
    + re-add the current clip so it can be transformed twice

{{{QUIT}}}
    + quit the viewer and save a new treatment structured file to queue/

{{{HELP}}}
    + print this message
'''.format_map(USAGE_MSGS)
