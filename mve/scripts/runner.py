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

import mve.src.constants.module as module

import mve.src.helpers.usage as usage


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
        parser = argparse.ArgumentParser(add_help=False,
                                         prog=usage.generate_module_usage())
        parser.add_argument('--info', action='help')

        logged = parser.add_subparsers(title='logging options', dest='logged')

        log = logged.add_parser('log',
                                description='scripts to run when logs are recorded',
                                add_help=False)
        log.add_argument('--scripts', action='help',
                         help='list all script choices where logs are recorded')
        log.add_argument('script', choices=[
            str(l) for l in [ScriptOption.DELETER, ScriptOption.GENERATOR,
                             ScriptOption.INTEGRITY, ScriptOption.MAKE,
                             ScriptOption.TREATER, ScriptOption.VIEWER]
        ], help='all script names that record logs')

        no_log = logged.add_parser('no-log',
                                   description='scripts to run when logs are not recorded',
                                   add_help=False)
        no_log.add_argument('--scripts', action='help',
                            help='list all script choices where logs are not recorded')
        no_log.add_argument('script', choices=[str(nl) for nl in [
                            ScriptOption.COMBINE, ScriptOption.FOCUS,
                            ScriptOption.MOMENT]],
                            help='all script names that do not record logs')

        return parser.parse_known_args()

    def map_script_name_to_enum(self, name: str) -> ScriptOption:
        return ScriptOption(name)

    def lookup_script(self,
                      option: ScriptOption
                      ) -> Script:
        return Runner.SCRIPTS[option]
