import os

import constants.colours as colours


def generate_colour_code(colour: int, bold: bool) -> str:
    return f'\033[{1 if bold else 0};{colour}m'


def colour_format(colour: int, message: str, bold: bool) -> str:
    return '{}{}{}'.format(
        generate_colour_code(colour, bold),
        message, generate_colour_code(colours.RESET, bold)
    )


def highlight(message: str, bold: bool) -> str:
    return colour_format(colours.BLUE, message, bold)


def highlight_path(paths_list: list[str], bold: bool) -> str:
    return highlight(os.path.join(*paths_list), bold)


def colour_box(colour: int, message: str, bold: bool):
    return f'[ {colour_format(colour, message, bold)} ]'


def warning(bold: bool) -> str:
    return colour_box(colours.YELLOW, 'warning', bold)
