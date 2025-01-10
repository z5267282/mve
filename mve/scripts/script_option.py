import enum


class ScriptOption(enum.Enum):
    '''Mapping of script name strings to enumerated options.'''

    DELETER = 'deleter'
    COMBINE = 'combine',
    FOCUS = 'focus'
    GENERATOR = 'generator'
    INTEGRITY = 'integrity'
    MAKE = 'make'
    TREATER = 'treater'
    VIEWER = 'viewer'
