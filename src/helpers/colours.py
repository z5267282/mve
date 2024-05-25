import constants.colour as clr

import constants.defaults as defaults


def generate_colour_code(colour: int, bold: bool) -> str:
    return f'\033[{1 if bold else 0};{colour}m'


def colour_format(colour: int, message: str, bold: bool = defaults.BOLD) -> str:
    return '{}{}{}'.format(
        generate_colour_code(colour, bold),
        message, generate_colour_code(clr.RESET, bold)
    )


def highlight(message: str) -> str:
    return colour_format(clr.BLUE, message)


def colour_box(colour: int, message: str):
    return f'[ {colour_format(colour, message)} ]'


def warning() -> str:
    return colour_box(clr.YELLOW, 'warning')
