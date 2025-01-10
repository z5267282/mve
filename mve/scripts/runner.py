
import enum
import argparse

import mve.scripts.log.make as make

import mve.scripts.script as script
import mve.scripts.script_option as script_option


class Runner():
    '''Controller class for running all mve scripts'''

    def __init__(self):
        self.scripts: dict[script_option.ScriptOption, script.Script] = {
            script_option.ScriptOption.MAKE: make.Make()
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

    def map_script_name_to_enum(self, name: str) -> script_option.ScriptOption:
        return script_option.ScriptOption(name)

    def lookup_script(self,
                      option: script_option.ScriptOption
                      ) -> script.Script:
        return self.scripts[option]
