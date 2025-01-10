'''Moviepy and FFMpeg timestamps require the ':' character for timestamps. It
is not the most ergonomic choice to type shift then ':' so we introduce a
shorthand instead, that is translated to ':'.'''

REQUIRED: str = ':'
SHORT_HAND: str = '-'
