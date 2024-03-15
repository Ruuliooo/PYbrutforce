import itertools
import random
import string
import timeit

import numpy

# Caractères autorisés pour la génération aléatoire de mots de passe
allowed_chars = string.ascii_lowercase + " "

# Base de données des mots de passe avec un exemple utilisateur initial
password_database = {"Jules": "bien joue tu as trouve le mdp"}

# Fonction pour vérifier si le mot de passe deviné correspond au mot de passe réel
def check_password(user, guess):
    actual = password_database[user]
    if len(guess) != len(actual):
        return False

    for i in range(len(actual)):
        if guess[i] != actual[i]:
            return False
    return True

# Fonction pour générer une chaîne de caractères aléatoire d'une certaine longueur
def random_str(size):
    return ''.join(random.choices(allowed_chars, k=size))

# Fonction pour estimer la longueur du mot de passe
def crack_length(user, max_len=32, verbose=False) -> int:
    trials = 2000
    times = numpy.empty(max_len)
    for i in range(max_len):
        i_time = timeit.repeat(stmt='check_password(user, x)',
                               setup=f'user={user!r};x=random_str({i!r})',
                               globals=globals(),
                               number=trials,
                               repeat=10)
        times[i] = min(i_time)

    if verbose:
        most_likely_n = numpy.argsort(times)[::-1][:5]
        print(most_likely_n, times[most_likely_n] / times[most_likely_n[0]])

    most_likely = int(numpy.argmax(times))
    return most_likely

# Fonction pour cracker le mot de passe avec une longueur estimée
def crack_password(user, length, verbose=False):
    guess = random_str(length)
    counter = itertools.count()
    trials = 1000
    while True:
        i = next(counter) % length
        for c in allowed_chars:
            alt = guess[:i] + c + guess[i + 1:]

            alt_time = timeit.repeat(stmt='check_password(user, x)',
                                     setup=f'user={user!r};x={alt!r}',
                                     globals=globals(),
                                     number=trials,
                                     repeat=10)
            guess_time = timeit.repeat(stmt='check_password(user, x)',
                                       setup=f'user={user!r};x={guess!r}',
                                       globals=globals(),
                                       number=trials,
                                       repeat=10)

            if check_password(user, alt):
                return alt

            if min(alt_time) > min(guess_time):
                guess = alt
                if verbose:
                    print(guess)


# Fonction principale
def main():
    user = "Jules"
    length = crack_length(user, verbose=True)
    print(f"using most likely length {length}")
    input("hit enter to continue...")
    password = crack_password(user, length, verbose=True)
    print(f"password cracked:'{password}'")

if __name__ == '__main__':
    main()
