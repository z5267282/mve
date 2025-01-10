import argparse

import mve.scripts.log.make as make

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('logged', type=str, choices=['log', 'no-log'])
    parser.add_argument('script', type=str)
    parser.add_argument('argv', nargs='*')
    args = parser.parse_args()

    match args.logged:
        case 'log':
            match args.script:
                case 'make':
                    print(args.argv)
                    # make.main(args.argv)

if __name__ == '__main__':
    main()
