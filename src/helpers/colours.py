import constants.colour as clr


def colour_format(colour, string):
    return f'{colour}{string}{clr.RESET}'

def highlight(string):
    return colour_format(clr.BLUE, string)

def colour_box(colour, message):
    return f'[ {colour_format(colour, message)} ]'
