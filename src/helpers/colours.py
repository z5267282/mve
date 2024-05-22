import constants.colour as clr

TODO_FIX = False


def generate_colour_code(colour: int, bold: bool) -> str:
    return f'\033[{1 if bold else 0};{colour}m'


def colour_format(colour: int, message: str) -> str:
    return f'{generate_colour_code(colour, TODO_FIX)}{message}{generate_colour_code(clr.RESET, TODO_FIX)}'


def highlight(message: str) -> str:
    return colour_format(clr.BLUE, message)


def colour_box(colour: int, message: str):
    return f'[ {colour_format(colour, message)} ]'


def warning() -> str:
    return colour_box(clr.YELLOW, 'warning')
