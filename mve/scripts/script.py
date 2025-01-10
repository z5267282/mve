import abc


class Script(abc.ABC):
    '''The Script interface all runnable mve scripts are expected to implement.'''

    @abc.abstractmethod
    def main(self, argv: list[str]) -> None:
        pass
