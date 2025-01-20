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

    SCRIPTS: dict[ScriptOption, Script] = {
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
        # enable --help for script-level parsers
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument('--info', action='help')

        logged = parser.add_subparsers(dest='logged')

        log = logged.add_parser('log', add_help=False)
        log.add_argument('--scripts', action='help')
        log.add_argument('script', choices=[
            str(l) for l in [ScriptOption.DELETER, ScriptOption.GENERATOR,
                             ScriptOption.INTEGRITY, ScriptOption.MAKE,
                             ScriptOption.TREATER, ScriptOption.VIEWER]
        ])

        no_log = logged.add_parser('no-log', add_help=False)
        no_log.add_argument('--scripts', action='help')
        no_log.add_argument('script', choices=[str(nl) for nl in [
                            ScriptOption.COMBINE, ScriptOption.FOCUS,
                            ScriptOption.MOMENT]])

        return parser.parse_known_args()

    def map_script_name_to_enum(self, name: str) -> ScriptOption:
        return ScriptOption(name)

    def create_script(self,
                      option: ScriptOption,
                      parser: argparse.ArgumentParser
                      ) -> Script:
        return Runner.SCRIPTS[option]
