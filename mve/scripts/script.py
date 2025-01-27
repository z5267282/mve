import abc


import mve.src.helpers.usage as usage


class Script(abc.ABC):
    '''The Script interface all runnable mve scripts are expected to
    implement.'''

    def __init__(self, name: str, logged: bool):
        self.name: str = name
        self.logged = logged

    @abc.abstractmethod
    def main(self, argv: list[str]) -> None:
        pass

    def generate_usage_name(self) -> str:
        logged = 'log' if self.logged else 'no-log'
        return f'{usage.generate_module_usage()} {logged} {self.name}'


class LoggedScript(Script):
    '''A Script that records logs.'''

    def __init__(self, name: str):
        super().__init__(name, True)


class NotLoggedScript(Script):
    '''A Script that does not record logs.'''

    def __init__(self, name: str):
        super().__init__(name, False)


class Legacy(LoggedScript):
    '''Legacy scripts did not use argparse and consider the first
    command-line argument to be the name of the script.'''

    def main(self, argv: list[str]) -> None:
        # as a hack, modifications to argv should be global
        argv.insert(0, self.name)
