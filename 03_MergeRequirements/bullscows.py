from random import choice


def my_ask(prompt: str, valid: list[str] = None):
    while True:
        a = input(prompt)
        if not valid or a in valid:
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
        tries += 1
        b, c = bullscows(guess, secret)
        inform("Быки: {}, Коровы: {}", b, c)
        if guess == secret:
            print(tries)
            break


gameplay(my_ask, my_inform, ['asd', 'wdr'])
# my_inform("Быки: {}, Коровы: {}", 1, 2)