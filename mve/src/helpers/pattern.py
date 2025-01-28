import dataclasses


@dataclasses.dataclass
class Pattern():
    '''Store an expected Regular Expression pattern and a description'''

    # store the pattern only so that specific regex functions can be called
    regex: str
    description: str
