import sys
import cowsay
from io import StringIO
import shlex
import cmd
import readline
import socket
import threading


BOARD_SIZE = 10


def reciever(cmdline):
    while True:
        if not LOCK:
            msg = s.recv(1024).decode().strip()
            print(f'\n{msg}\n{cmdline.prompt}{readline.get_line_buffer()}', end='', flush=True)

    

class InvalidCommand(Exception):
    pass


class InvalidParams(Exception):
    pass


class CmdLine(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = '> '
        self.intro = "<<< Social Project >>>\n"
        self.intro += 'Type help or ? to list commands\n'
        self.intro += 'Type exit to quit\n'

    def do_who(self, arg):
        """Prints list of registered users. No arguments"""
        s.send('who\n'.encode())
        reciever(s.recv(1024).decode().strip())

    def do_cows(self, arg):
        """Prints list of available usernames. No arguments"""
        s.send('down\n'.encode())
        reciever(s.recv(1024).decode().strip())
    
    def do_login(self, arg):
        """Connects client to server. Name - positional argument"""
        s.send('left\n'.encode())
        reciever(s.recv(1024).decode().strip())

    def do_say(self, arg):
        """
Sends a private message to another user.
Args:
    name - recipient's username (positional)
    text - message to send (positional)
        """
        s.send('right\n'.encode())
        reciever(s.recv(1024).decode().strip())

    def do_exit(self, arg):
        """Exits the game"""
        return 1
    
    def do_yield(self, args):
        """
Sends a message to all users in the chat.
Arguments:
    text - The message to send (positional)
        """
        try:
            name, *args = shlex.split(args)
            x, y = args[args.index('coords') + 1], args[args.index('coords') + 2]
            hp, hello = args[args.index('hp') + 1], args[args.index('hello') + 1]
            if int(x) not in range(BOARD_SIZE) or int(y) not in range(BOARD_SIZE) or int(hp) <= 0:
                raise InvalidParams
            s.send(f'addmon {int(x)} {int(y)} "{name}" "{hello}" {int(hp)}\n'.encode())
            print(s.recv(1024).decode().strip())
        except InvalidCommand:
            print('Invalid command')
        except InvalidParams:
            print('Invalid argument')
        except Exception as e:
            print(e)
    
    def do_quit(self, arg):
        """Disconnect from server"""
        try:
            if not arg:
                raise InvalidParams
            name, *arg = shlex.split(arg)
            if arg:
                weapon = arg[1]
                match weapon:
                    case 'sword':
                        s.send(f'attack {10} {name}\n'.encode())
                        print(s.recv(1024).decode().strip())
                    case 'spear':
                        s.send(f'attack {15} {name}\n'.encode())
                        print(s.recv(1024).decode().strip())
                    case 'axe':
                        s.send(f'attack {20} {name}\n'.encode())
                        print(s.recv(1024).decode().strip())
                    case _:
                        print("Unknown weapon")
            else:
                s.send(f'attack {10} {name}\n'.encode())
                print(s.recv(1024).decode().strip())
        except InvalidCommand:
            print('Invalid command')
        except InvalidParams:
            print('Invalid argument')
        except Exception as e:
            print(e)

    def complete_attack(self, text, line, begidx, endidx):
        if line[begidx - 7: begidx - 1] == 'attack':
            return [x for x in cowsay.list_cows() + ['jgsbat'] if x.startswith(text)]
        if line[begidx - 5: begidx - 1] == 'with':
            return [s for s in ['sword', 'spear', 'axe'] if s.startswith(text)]
        
    def complete_addmon(self, text, line, begidx, endidx):
        if line[begidx - 7: begidx - 1] == 'addmon':
            return [x for x in cowsay.list_cows() + ['jgsbat'] if x.startswith(text)]


if __name__ == '__main__':
    LOCK = threading.Lock()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # print(len(sys.argv))
        s.connect((sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 1337))
        try:
            try:
                readline.read_history_file()
            except:
                pass
            cmdline = CmdLine()
            recive = threading.Thread(target=reciever, args=(cmdline))
            recive.start()
            cmdline.cmdloop()
            readline.write_history_file()
        except InvalidCommand:
            print('Invalid command')
        except InvalidParams:
            print('Invalid argument')
        except Exception as e:
            print(e)