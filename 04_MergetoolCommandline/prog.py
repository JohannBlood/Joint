import sys
from cowsay import cowsay, list_cows, make_bubble, cowthink
import cmd
import shlex
from dataclasses import dataclass


@dataclass
class Bubble:
    stem: str = '\\'
    l: str = '<'
    r: str = '>'
    tl: str = '/'
    tr: str = '\\'
    ml: str = '|'
    mr: str = '|'
    bl: str = '\\'
    br: str = '/'


THOUGHT_OPTIONS = {
    'cowsay': Bubble('\\', '<', '>', '/', '\\', '|', '|', '\\', '/'),
    'cowthink': Bubble('o', '(', ')', '(', ')', '(', ')', '(', ')'),
}


class Cmdline(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = '>>>>> '
        self.intro = 'Welcome to Cowsay! Type help or? to list commands.\n'

    def do_list_cows(self, arg):
        """Lists all the cow file names. No arguments."""
        print(*list_cows())

    def do_make_bubble(self, arg):
        """
        Wraps text is wrap_text is true, then pads text and sets inside a bubble.
        This is the text that appears above the cows  
        Arguments:
        text - The text to be wraped (positional argument);
        -b - Cowthink or cowsay (optional);
        -w - Width (optional);
        -t - Wrap or not (optional).
        """
        try:
            text, *args = shlex.split(arg)
            wrap_text = True
            width = 40
            brackets = THOUGHT_OPTIONS['cowsay']
            for ind, el in enumerate(args):
                if args[ind] == '-b':
                    brackets = THOUGHT_OPTIONS[args[ind + 1]]
                elif args[ind] == '-w':
                    width = int(args[ind + 1])
                elif args[ind] == '-t':
                    wrap_text = eval(args[ind + 1])
            print(make_bubble(text, brackets=brackets, width=width, wrap_text=wrap_text))
        except Exception as e:
            print('Wrong arguments')
        

    
    def do_cowsay(self, args):
        '''
        Cowsay  generates  an ASCII picture of a cow saying something provided by the user.  
        Arguments:
        message - The message to be cowsayed (positional argument);
        -c - Cow's name (optional);
        -e - The eyes of the cow (optional);
        -t - The tongue of the cow (optional).
        '''
        try:
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
        except Exception as e:
            print('Wrong arguments')
    
    def do_cowthink(self, args):
        '''
        Cowsay  generates  an ASCII picture of a cow saying something provided by the user.  
        Arguments:
        message - The message to be cowsayed (positional argument);
        -c - Cow's name (optional);
        -e - The eyes of the cow (optional);
        -t - The tongue of the cow (optional).
        '''
        try:
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
            print(cowthink(message, cow=cow, eyes=eyes, tongue=tongue))
        except Exception as e:
            print('Wrong arguments')
        
    def do_exit(self, arg):
        """Exits the program."""
        return 1
    
    def complete_cowsay(self, text, line, begidx, endidx):
        if line[begidx - 3: begidx - 1] == '-e':
            return [s for s in ['00', 'xx', 'oo', '||'] if s.startswith(text)]
        if line[begidx - 3: begidx - 1] == '-t':
            return [s for s in ['0 ', ' 0', ' v', 'v '] if s.startswith(text)]
        if line[begidx - 3: begidx - 1] == '-c':
            return [s for s in list_cows() if s.startswith(text)]
        return []
    
    def complete_cothink(self, text, line, begidx, endidx):
        if line[begidx - 3: begidx - 1] == '-e':
            return [s for s in ['00', 'xx', 'oo', '||'] if s.startswith(text)]
        if line[begidx - 3: begidx - 1] == '-t':
            return [s for s in ['0 ', ' 0', ' v', 'v '] if s.startswith(text)]
        if line[begidx - 3: begidx - 1] == '-c':
            return [s for s in list_cows() if s.startswith(text)]
        return []
    
    def complete_make_bubble(self, text, line, begidx, endidx):
        if line[begidx - 3: begidx - 1] == '-b':
            return [s for s in ['cowsay', 'cowthink'] if s.startswith(text)]
        if line[begidx - 3: begidx - 1] == '-t':
            return [s for s in ['True', 'False'] if s.startswith(text)]
        return []




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