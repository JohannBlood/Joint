from random import choice
import argparse
import urllib.request


def my_ask(prompt: str, valid: list[str] = None):
    while True:
        a = input(prompt)
        if not valid or a in valid or a == 'qwerty':
            return a


def my_inform(format_string: str, bulls: int, cows: int):
    print(format_string.format(bulls, cows))


def bullscows(guess: str, secret: str):
    n_bulls = 0
    n_cows = len(set(guess) & set(secret))
    for i in range(len(guess)):
        if guess[i] == secret[i]:
            n_bulls += 1
    return n_bulls, n_cows


def gameplay(ask: callable, inform: callable, words: list[str]):
    secret = choice(words)
    tries = 0
    while True:
        guess = ask("Введите слово: ", words)
        if guess == 'qwerty':
            print(secret)
            continue
        tries += 1
        b, c = bullscows(guess, secret)
        inform("Быки: {}, Коровы: {}", b, c)
        if guess == secret:
            print(tries)
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('dictionary', type=str)
    parser.add_argument('length', type=int, nargs='?', default=5)
    args = parser.parse_args()
    if '/' in args.dictionary:
        my_open = urllib.request.urlopen
    else:
        my_open = open
    with my_open(args.dictionary) as data:
        # print(data.read().decode())
        data = data.read()
        if type(data) == str:
            d = list(filter(lambda x: len(x) == args.length, data.split()))
        else:
            d = list(filter(lambda x: len(x) == args.length, data.decode().split()))
    print(d[:10])
    gameplay(my_ask, my_inform, d)
# my_inform("Быки: {}, Коровы: {}", 1, 2)