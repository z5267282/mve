import argparse

import mve.scripts.log.make as make


def main():
    parser = argparse.ArgumentParser()
    logged = parser.add_subparsers(dest='logged')

    log = logged.add_parser('log')
    log.add_argument('script', choices=['make'])
    log.add_argument('argv', nargs='*')

    no_log = logged.add_parser('no-log')
    no_log.add_argument('script', choices=['focus'])
    no_log.add_argument('argv', nargs='*')

    args = parser.parse_args()

    match args.logged:
        case 'log':
            match args.script:
                case 'make':
                    make.main(args.argv)
        case 'no-log':
            pass


if __name__ == '__main__':
    main()
