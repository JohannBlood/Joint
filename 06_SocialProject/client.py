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
        if not LOCK.locked():
            msg = s.recv(2048).decode().strip()
            # print('wtf', LOCK.locked(), msg)
            if not msg:
                break
            if msg.startswith('#'):
                # print('#', LOCK.locked(), msg)
                cmdline.cows = msg[1:]
                continue
            elif msg.startswith('\\'):
                cmdline.who = msg[1:]
                continue
            if msg == 'Leaving the chat':
                print('\nLeaving the chat')
                break
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
        self.cows = None
        self.who = None

    def do_who(self, arg):
        """Prints list of registered users. No arguments"""
        s.send('who\n'.encode())
        # reciever(s.recv(1024).decode().strip())

    def do_cows(self, arg):
        """Prints list of available usernames. No arguments"""
        s.send('cows\n'.encode())
        # reciever(s.recv(1024).decode().strip())
    
    def do_login(self, arg):
        """Connects client to server. Name - positional argument"""
        try:
            if arg:
                s.send(f'login {arg}\n'.encode())
            else:
                raise InvalidParams
        except InvalidParams:
            print('Invalid arguments')
        # reciever(s.recv(1024).decode().strip())

    def do_say(self, arg):
        """
Sends a private message to another user.
Args:
    name - recipient's username (positional)
    text - message to send (positional)
        """
        name, text = shlex.split(arg)
        s.send(f'say {name} "{text}"\n'.encode())
        # reciever(s.recv(1024).decode().strip())

    def do_exit(self, arg):
        """Exits the game"""
        s.send(f'quit\n'.encode())
        return 1
    
    def do_yield(self, args):
        """
Sends a message to all users in the chat.
Arguments:
    text - The message to send (positional)
        """
        s.send(f'yield "{args}"\n'.encode())
    
    def do_quit(self, arg):
        """Disconnect from server"""
        s.send(f'quit\n'.encode())
        return 1

    def complete_login(self, text, line, begidx, endidx):
        s.send(f'#cows\n'.encode())
        # print(cows)
        while not self.cows:
            pass
        cows = shlex.split(self.cows)
        self.cows = None
        return [s for s in cows if s.startswith(text)]
        
    def complete_say(self, text, line, begidx, endidx):
        if line[:begidx] == 'say ':
            s.send(f'#who\n'.encode())
            # print(cows)
            while not self.who:
                pass
            who = shlex.split(self.who)
            self.who = None
            return [s for s in who if s.startswith(text)]


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
            recive = threading.Thread(target=reciever, args=(cmdline,))
            recive.start()
            cmdline.cmdloop()
            readline.write_history_file()
        except InvalidCommand:
            print('Invalid command')
        except InvalidParams:
            print('Invalid argument')
        except Exception as e:
            print(e)