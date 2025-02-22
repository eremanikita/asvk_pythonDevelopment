from cowsay import cowsay
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-e", "--eyes", default="oo")
parser.add_argument("-f", "--cow", default="default")
parser.add_argument("-n", "--wrapper", action="store_true")
parser.add_argument("-T", "--tongue", default='  ')
parser.add_argument("-W", "--width", type=int, default=40)
parser.add_argument("message", default=None, nargs='?')

args = parser.parse_args()
print(cowsay(message=args.message,
             eyes=args.eyes,
             width=args.width,
             cow=args.cow,
             wrap_text=args.wrapper,
             tongue=args.tongue))
