'''The Script interface all runnable mve scripts are expected to implement.'''
import abc


class Script(abc.ABC):
    @abc.abstractmethod
    def main(self, argv: list[str]) -> None:
        pass
