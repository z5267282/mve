import argparse

import mve.scripts.log.make as make

import mve.scripts.script as script


def main():
    parser = argparse.ArgumentParser()
    logged = parser.add_subparsers(dest='logged')

    log = logged.add_parser('log')
    log.add_argument('script', choices=['make'])

    no_log = logged.add_parser('no-log')
    no_log.add_argument('script', choices=['focus'])

    args, argv = parser.parse_known_args()

    scripts: dict[str, script.Script] = {
        'make': make.Make()
    }

    # run chosen script
    scripts[args.script].main(argv)


if __name__ == '__main__':
    main()
