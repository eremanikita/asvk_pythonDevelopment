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
first_cow = cowsay(message=args.first_message,
                   eyes=args.first_eyes,
                   width=args.width,
                   cow=args.first_cow,
                   wrap_text=args.first_wrapper,
                   tongue=args.tongue).split("\n")
max_length = max(map(len, first_cow))
second_cow = cowsay(message=args.second_message,
                    eyes=args.second_eyes,
                    width=args.width,
                    cow=args.second_cow,
                    wrap_text=args.second_wrapper,
                    tongue=args.tongue).split("\n")
first_rows = len(first_cow)
second_rows = len(second_cow)
result = []
for i in range(max(len(first_cow), len(second_cow))):
    print(i, first_rows, second_rows)
    part_one = first_cow[first_rows - i - 1] if i < first_rows else ""
    part_two = second_cow[second_rows - i - 1] if i < second_rows else ""
    result.append(part_one + " " * (max_length - len(part_one)) + part_two + "\n")
print(*result[::-1])

