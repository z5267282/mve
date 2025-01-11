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
            ScriptOption.COMBINE: Combine('combine'),
            ScriptOption.FOCUS: Focus('focus'),
            ScriptOption.DELETER: Deleter('deleter'),
            ScriptOption.GENERATOR: Generator('generator'),
            ScriptOption.INTEGRITY: Integrity('integrity'),
            ScriptOption.MAKE: Make('make'),
            ScriptOption.MOMENT: Moment('moment'),
            ScriptOption.TREATER: Treater('treater'),
            ScriptOption.VIEWER: Viewer('viewer')
        }

    def run(self) -> None:
        args, argv = self.parse_args()
        option = self.map_script_name_to_enum(args.script)
        script = self.lookup_script(option)

        script.main(argv)

    def parse_args(self) -> tuple[argparse.Namespace, list[str]]:
        # enable only for script-level parsers
        parser = argparse.ArgumentParser(add_help=False)
        logged = parser.add_subparsers(dest='logged')

        log = logged.add_parser('log')
        log.add_argument('script', choices=[
                         'deleter', 'generator', 'integrity', 'make', 'treater', 'viewer'])

        no_log = logged.add_parser('no-log')
        no_log.add_argument('script', choices=['combine', 'focus', 'moment'])

        return parser.parse_known_args()

    def map_script_name_to_enum(self, name: str) -> ScriptOption:
        return ScriptOption(name)

    def lookup_script(self,
                      option: ScriptOption
                      ) -> Script:
        return self.scripts[option]
