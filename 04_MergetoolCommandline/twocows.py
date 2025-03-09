import cmd
import readline
import cowsay
import shlex


def show_two_cows(params, func):
    first_cow = func(message=params["text"],
                     eyes=params["eyes"] if "eyes" in params else "oo",
                     cow=params["cow"],
                     wrap_text=params["text"],
                     tongue=params["tongue"] if "tongue" in params else "  ").split("\n")
    max_length = max(map(len, first_cow))
    second_cow = func(message=params["text_reply"],
                      eyes=params["eyes_reply"] if "eyes_reply" in params else "oo",
                      cow=params["cow_reply"],
                      wrap_text=params["text_reply"],
                      tongue=params["tongue_reply"] if "tongue_reply" in params else "  ").split("\n")
    first_rows = len(first_cow)
    second_rows = len(second_cow)
    result = []
    for i in range(max(len(first_cow), len(second_cow))):
        part_one = first_cow[first_rows - i - 1] if i < first_rows else ""
        part_two = second_cow[second_rows - i - 1] if i < second_rows else ""
        result.append(part_one + " " * (max_length - len(part_one)) + part_two + "\n")
    print(*result[::-1])


def parse_args(line: str):
    tokens = shlex.split(line)
    params = dict()

    split_index = tokens.index("reply")
    first_part, second_part = tokens[:split_index], tokens[split_index + 1:]

    def parse_cow_params(tokens, params, reply_flag: bool):
        if tokens:
            params["text" + ("_reply" if reply_flag else "")] = tokens[0]
        params["cow" + ("_reply" if reply_flag else "")] = tokens[1] if len(tokens) > 1 else "default"
        for param in tokens[2:]:
            key, value = param.split("=")
            params[key + ("_reply" if reply_flag else "")] = value

    parse_cow_params(first_part, params, False)
    parse_cow_params(second_part, params, True)
    return params


class cows(cmd.Cmd):
    prompt = "twocows>> "

    def do_list_cows(self, arg):
        """Show list of all available cows if no parameters are given. Else check the provided name."""
        if arg:
            print("Yes" if arg in cowsay.list_cows() else "No")
        else:
            print(" ".join(cowsay.list_cows()))

    def do_make_bubble(self, args):
        """Make a bubble with provided text."""
        if args:
            print(cowsay.make_bubble(args))
        else:
            print("No args provided")

    def do_cowsay(self, args):
        """Show two cows with provided text and parameters.
        cowsay message [name [param=value …]] reply answer [name [[param=value …]]

        eyes and tongues ara available"""
        show_two_cows(parse_args(args), cowsay.cowsay)

    def complete_cowsay(self, text, line, begidx, endidx):
        tokens = shlex.split(line + ".")
        if len(tokens) == 3 or len(tokens) - tokens.index('reply') == 3:
            return [c for c in cowsay.list_cows() if c.startswith(tokens[-1][:-1])]

    def do_cowthink(self, args):
        """Show two thinking cows with provided text and parameters.
                cowthink message [name [param=value …]] reply answer [name [[param=value …]]

                eyes and tongues ara available"""
        show_two_cows(parse_args(args), cowsay.cowthink)

    def complete_cowthink(self, text, line, begidx, endidx):
        tokens = shlex.split(line + ".")
        if len(tokens) == 3 or len(tokens) - tokens.index('reply') == 3:
            return [c for c in cowsay.list_cows() if c.startswith(tokens[-1][:-1])]

    def do_exit(self, arg):
        """Выход из программы"""
        return True


if __name__ == '__main__':
    readline.parse_and_bind("bind ^I rl_complete")
    cows().cmdloop()
