import cmd
import threading
import readline
import sys
import socket
import queue

queue = queue.Queue()


class sender(cmd.Cmd):
    command_counter = 1

    def do_who(self, arg):
        s.sendall("0 who\n".encode())

    def do_login(self, args):
        s.sendall(f"0 login {args}\n".encode())

    def complete_login(self, text, line, begidx, endidx):
        s.sendall(f"{self.command_counter} cows\n".encode())
        self.command_counter += 1
        tokens = (line + ".").split()
        return [c for c in queue.get().split(", ") if c.startswith(tokens[-1][:-1])]

    def do_cows(self, args):
        s.sendall("0 cows\n".encode())

    def do_say(self, args):
        s.sendall(f"0 say {args}\n".encode())

    def complete_say(self, text, line, begidx, endidx):
        s.sendall(f"{self.command_counter} who\n".encode())
        self.command_counter += 1
        tokens = (line + ".").split()
        return [c for c in queue.get().split(", ") if c.startswith(tokens[-1][:-1])]

    def do_yield(self, args):
        s.sendall(f"0 yield {args}\n".encode())

    def do_quit(self, args):
        s.sendall("0 quit\n".encode())
        return True


def receive():
    while True:
        response = s.recv(1024).rstrip().decode()
        if response[0] == '0':
            print(f"\n{response[2:]}\n{cmdline.prompt}{readline.get_line_buffer() if readline.get_line_buffer()[-1] != "\n" else ""}",
                end="", flush=True)
        else:
            queue.put(response[2:])


host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
port = 1337 if len(sys.argv) < 3 else int(sys.argv[2])
readline.parse_and_bind("bind ^I rl_complete")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    cmdline = sender()
    receiver = threading.Thread(target=receive)
    receiver.start()
    cmdline.cmdloop()
