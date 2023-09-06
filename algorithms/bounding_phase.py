import random

import numpy as np

from constants import objective_function, summary


def bounding_phase(
    min_pt: float,
    max_pt: float,
    delta: float | None = None,
    epsilon: float | None = None,
    iter: int | None = None,
    is_minimising: bool = False,
) -> bool:
    """
    Working ->
        1. Find x0 such that f(x0 - delta) >= f(x0) >= f(x0 + delta) or vice versa
        2. Start with k = 0
        3. Set x(k - 1) aka xkm1 = x0 and xk = x0. 
        4. Find x(k + 1) aka xkp1 = xk + 2^k * delta
        5. If f(xk) <= f(xkp1) then we have found the minima (and vice versa for maxima)
        6. Else, set xkm1 = xk and xk = xkp1 and go to step 4
    """
    x0 = -1
    k = 0

    if not delta:
        raise ValueError("Must provide delta for bounding phase")

    tries = 100  # Max tries to initiliase x0
    while tries:
        x0 = round(random.uniform(min_pt, max_pt), 2)
        if x0 - delta < min_pt or x0 + delta > max_pt:
            tries -= 1
            continue

        f0 = objective_function(x0 - np.abs(delta))
        f1 = objective_function(x0)
        f2 = objective_function(x0 + np.abs(delta))
        

        if f0 >= f1 and f1 >= f2:
            break
        elif f0 <= f1 and f1 <= f2:
            delta *= -1
            break

        tries -= 1

    if tries == 0:
        print("Could not find a suitable x0")
        return False

    xk = x0
    xkm1 = x0
    iter_count = 0
    while xkm1 > min_pt and xk < max_pt:
        iter_count += 1
        xkp1 = xk + 2**k * delta
        fxk = objective_function(xk)
        fxkp1 = objective_function(xkp1)

        summary.append([iter_count, xkm1, xk, xkp1, fxk, fxkp1])

        if is_minimising and fxk <= fxkp1:
            print("Found minima")
            return True

        elif not is_minimising and fxk >= fxkp1:
            print("Found maxima")
            return True

        k += 1
        xkm1 = xk
        xk = xkp1

    return False
