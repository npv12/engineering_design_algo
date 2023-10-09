import random


def find_derivative(f, x, h=0.01):
    return (f(x + h) - f(x)) / h

def find_double_derivative(f, x, h=0.01):
    return (f(x + h) - 2 * f(x) + f(x - h)) / (h**2)

def find_random_start(min_pt, max_pt, epsilon):
    tries = 100  # Max tries to initiliase x0
    while tries:
        x0 = round(random.uniform(min_pt, max_pt), 2)
        if (x0 - epsilon) > min_pt and (x0 + epsilon) < max_pt:
            return x0

        tries -= 1

    if tries == 0:
        raise Exception("Could not find a suitable x0")