def bullscows(guess: str, secret: str):
    n_bulls = 0
    n_cows = len(set(guess) & set(secret))
    for i in range(len(guess)):
        if guess[i] == secret[i]:
            n_bulls += 1
    return n_bulls, n_cows
            

print(bullscows("ропот", "полип"))