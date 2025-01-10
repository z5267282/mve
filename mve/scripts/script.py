import abc


class Script(abc.ABC):
    '''The Script interface all runnable mve scripts are expected to implement.'''

    def __init__(self, name: str):
        self.name: str = name

    @abc.abstractmethod
    def main(self, argv: list[str]) -> None:
        pass
