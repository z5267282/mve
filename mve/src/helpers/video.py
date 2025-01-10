import re
import subprocess

import mve.src.helpers.time_handlers as time_handlers


def convert_integer_seconds_to_natural_number(seconds: str,
                                              duration: int) -> int:
    raw_seconds = time_handlers.get_seconds(seconds)
    return duration - raw_seconds if seconds.startswith('-') \
        else raw_seconds


def get_duration(joined_src_path: str) -> int:
    args = [
        'ffprobe',
        '-i',
        joined_src_path,
        '-v',
        'quiet',
        '-show_entries',
        'format=duration',
        '-hide_banner',
        '-of',
        'default=noprint_wrappers=1:nokey=1'
    ]
    result = subprocess.run(args, capture_output=True, text=True)
    return round_float(result.stdout)


def round_float(float_string: str) -> int:
    match = re.match(r'([(0-9)]+)\.([0-9])', float_string)
    if match is None:
        raise ValueError(f'could not round the time: {float_string}')
    whole_number: int = int(
        match.group(1)
    )
    tenths: int = int(
        match.group(2)
    )
    return whole_number + (tenths >= 5)
