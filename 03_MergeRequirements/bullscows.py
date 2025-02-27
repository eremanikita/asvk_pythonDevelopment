import random
import requests
import sys
import certifi
import cowsay


def bullscows(hunch: str, riddle: str) -> (int, int):
    count_cows = count_bulls = 0
    riddle_length = len(riddle)
    riddle_letters = set(riddle)
    for index, i in enumerate(hunch):
        if index < riddle_length and hunch[index] == riddle[index]:
            count_cows += 1
        elif i in riddle_letters:
            count_bulls += 1
    return count_cows, count_bulls


def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    riddle = random.choice(words)
    count_attempts = 1
    while (hunch := ask("Введите слово: ", words)) != riddle:
        bulls, cows = bullscows(hunch, riddle)
        inform("Быки: {}, Коровы: {}", bulls, cows)
        count_attempts += 1
    print(f"Right! You used{count_attempts} attempts.")


def custom_cowsay(message):
    bubble = f"""
  {'_' * (len(message) + 2)}
< {message} >
  {'-' * (len(message) + 2)}"""

    cow = r"""
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
    """
    return bubble + "\n" + cow


def ask(prompt: str, valid: list[str] = None) -> str:
    print(custom_cowsay(prompt))
    word = input()
    if valid is not None:
        while word not in valid:
            print(custom_cowsay(prompt))
            word = input()
    return word


def inform(format_string: str, bulls: int, cows: int) -> None:
    cowsay.cowsay(format_string.format(bulls, cows))


def load_words(source: str, length: int) -> list[str]:
    if source.startswith("http://") or source.startswith("https://"):
        words = requests.get(source, verify=certifi.where()).text.splitlines()
    else:
        with open(source, "r") as f:
            words = f.read().splitlines()
    return [word.strip() for word in words if len(word.strip()) == length]


def main():
    if len(sys.argv) < 2:
        print("Incorrect. Usage: `python -m bullscows dictionary [length]`")
    else:
        source = sys.argv[1]
        length = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        words = load_words(source, length)
        gameplay(ask, inform, words)


if __name__ == "__main__":
    main()
