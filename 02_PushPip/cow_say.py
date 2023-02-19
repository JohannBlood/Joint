import sys
from cowsay import cowsay, list_cows
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('cowsay', default='', type=str, nargs='?')
parser.add_argument('-e', '--eye_string', default='oo', type=str)
parser.add_argument('-f', '--cowfile', default='')
parser.add_argument('-l', default='', action='store_true')
parser.add_argument('-T', '--tongue_string', default='', type=str)
parser.add_argument('-W', '--column', default=40, type=int)
args = parser.parse_args()
if args.l:
    print(list_cows())
elif args.cowfile:
    print(cowsay(message=args.cowsay, eyes=args.eye_string,
                    tongue=args.tongue_string, width=args.column))
else:
    try:
        if '/' in args.cowfile:
            with open(args.cowfile) as cowfile:
                print(cowsay(message=args.cowsay, eyes=args.eye_string,
                    tongue=args.tongue_string, width=args.column, cowfile=cowfile.read()))
        else:
            print(cowsay(message=args.cowsay, eyes=args.eye_string,
                        tongue=args.tongue_string, width=args.column, cow=args.cowfile))
    except FileNotFoundError:
            print('No such file or directory')
            sys.exit(1)