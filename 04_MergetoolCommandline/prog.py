import sys
from cowsay import cowsay, list_cows
import cmd
import shlex


class Cmdline(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = '>>>>> '
        self.intro = 'Welcome to Cowsay! Type help or? to list commands.\n'

    def do_list_cows(self, arg):
        """Lists all the cow file names. No arguments."""
        print(*list_cows())
    
    def do_cowsay(self, args):
        '''
        Cowsay  generates  an ASCII picture of a cow saying something provided by the user.  
        Arguments:
        message - The message to be cowsayed (positional argument);
        -c - Cow's name (optional);
        -e - The eyes of the cow (optional);
        -t - The tongue of the cow (optional).
        '''
        message, *args = shlex.split(args)
        cow = 'default'
        eyes = 'oo'
        tongue = '  '
        for ind, el in enumerate(args):
            if el == '-c':
                cow = args[ind+1]
            if el == '-e':
                eyes = args[ind+1]
            if el == '-t':
                tongue = args[ind+1]
        print(cowsay(message, cow=cow, eyes=eyes, tongue=tongue))



if __name__ == '__main__':
    Cmdline().cmdloop()
# parser = argparse.ArgumentParser()
# parser.add_argument('cowsay', default='', type=str, nargs='?')
# parser.add_argument('-e', '--eye_string', default='oo', type=str)
# parser.add_argument('-f', '--cowfile', default='')
# parser.add_argument('-l', default='', action='store_true')
# parser.add_argument('-T', '--tongue_string', default='', type=str)
# parser.add_argument('-W', '--column', default=40, type=int)
# args = parser.parse_args()
# # print(bool(args.cowfile))
# if args.l:
#     print(list_cows())
# elif not args.cowfile:
#     print(cowsay(message=args.cowsay, eyes=args.eye_string,
#                     tongue=args.tongue_string, width=args.column))
# else:
#     try:
#         if '/' in args.cowfile:
#             with open(args.cowfile) as cowfile:
#                 print(cowsay(message=args.cowsay, eyes=args.eye_string,
#                     tongue=args.tongue_string, width=args.column, cowfile=cowfile.read()))
#         else:
#             print(cowsay(message=args.cowsay, eyes=args.eye_string,
#                         tongue=args.tongue_string, width=args.column, cow=args.cowfile))
#     except FileNotFoundError:
#             print('No such file or directory')
#             sys.exit(1)