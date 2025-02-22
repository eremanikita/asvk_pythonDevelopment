from cowsay import cowsay
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-e", "--first_eyes", default="oo")
parser.add_argument("-f", "--first_cow", default="default")
parser.add_argument("-n", "--first_wrapper", action="store_true")
parser.add_argument("-T", "--tongue", default='  ')
parser.add_argument("-W", "--width", type=int, default=40)
parser.add_argument("first_message", default=None, nargs='?')

parser.add_argument("-E", "--second_eyes", default="oo")
parser.add_argument("-F", "--second_cow", default="default")
parser.add_argument("-N", "--second_wrapper", action="store_true")
parser.add_argument("second_message", default=None, nargs='?')

args = parser.parse_args()
print(cowsay(message=args.first_message,
             eyes=args.first_eyes,
             width=args.width,
             cow=args.first_cow,
             wrap_text=args.first_wrapper,
             tongue=args.tongue))
print(cowsay(message=args.second_message,
             eyes=args.second_eyes,
             width=args.width,
             cow=args.second_cow,
             wrap_text=args.second_wrapper,
             tongue=args.tongue))
