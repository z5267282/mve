import abc


class Script(abc.ABC):
    '''The Script interface all runnable mve scripts are expected to implement.'''

    def __init__(self, name: str):
        self.name: str = name

    @abc.abstractmethod
    def main(self, argv: list[str]) -> None:
        pass


class Legacy(Script):
    '''Legacy scripts did not use argparse and consider the first
    command-line argument to be the name of the script.'''

    def main(self, argv: list[str]) -> None:
        # as a hack, modifications to argv should be global
        argv.insert(0, self.name)
