import argparse

from mve.scripts.log.deleter import Deleter
from mve.scripts.log.generator import Generator
from mve.scripts.log.integrity import Integrity
from mve.scripts.log.make import Make
from mve.scripts.log.treater import Treater
from mve.scripts.log.viewer import Viewer

from mve.scripts.no_log.combine import Combine
from mve.scripts.no_log.focus import Focus
from mve.scripts.no_log.moment import Moment

from mve.scripts.script import Script
from mve.scripts.script_option import ScriptOption


class Runner():
    '''Controller class for running all mve scripts'''

    def __init__(self):
        self.scripts: dict[ScriptOption, Script] = {
            ScriptOption.COMBINE: Combine(),
            ScriptOption.FOCUS: Focus(),
            ScriptOption.DELETER: Deleter(),
            ScriptOption.GENERATOR: Generator(),
            ScriptOption.INTEGRITY: Integrity(),
            ScriptOption.MAKE: Make(),
            ScriptOption.MOMENT: Moment(),
            ScriptOption.TREATER: Treater(),
            ScriptOption.VIEWER: Viewer()
        }

    def run(self) -> None:
        args, argv = self.parse_args()
        option = self.map_script_name_to_enum(args.script)
        script = self.lookup_script(option)

        script.main(argv)

    def parse_args(self) -> tuple[argparse.Namespace, list[str]]:
        parser = argparse.ArgumentParser()
        logged = parser.add_subparsers(dest='logged')

        log = logged.add_parser('log')
        log.add_argument('script', choices=['make'])

        no_log = logged.add_parser('no-log')
        no_log.add_argument('script', choices=['focus'])

        return parser.parse_known_args()

    def map_script_name_to_enum(self, name: str) -> ScriptOption:
        return ScriptOption(name)

    def lookup_script(self,
                      option: ScriptOption
                      ) -> Script:
        return self.scripts[option]
