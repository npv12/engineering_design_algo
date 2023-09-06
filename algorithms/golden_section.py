import numpy as np

from constants import GAMMA, objective_function, summary


def golden_section(
    min_pt: float,
    max_pt: float,
    delta: float | None = None,
    epsilon: float | None = None,
    iter: int | None = None,
    is_minimising: bool = False,
    iter_count=0,
    k=2,
    L=None,
) -> bool:
    """ """
    if not L:
        L = max_pt - min_pt
    if not iter:
        iter = 100

    if delta and delta > L:
        if is_minimising:
            print("Found minima")
        else:
            print("Found maxima")
        return True

    if k > iter:
        return True

    lk = L/(GAMMA ** k)

    if epsilon and lk < epsilon:
        if is_minimising:
            print("Found minima")
        else:
            print("Found maxima")
        return True

    tx1 = min_pt + lk
    tx2 = max_pt - lk

    # Ensure that x1 < x2
    x1 = np.min([tx1, tx2])
    x2 = np.max([tx1, tx2])

    fx1 = objective_function(x1)
    fx2 = objective_function(x2)

    iter_count += 1
    summary.append([iter_count, min_pt, max_pt, lk, x1, x2, fx1, fx2])

    if is_minimising:
        if fx1 < fx2:
            max_pt = x2
        elif fx1 > fx2:
            min_pt = x1
        else:
            min_pt = x1
            max_pt = x2
    else:
        if fx1 > fx2:
            max_pt = x2
        elif fx1 < fx2:
            min_pt = x1
        else:
            min_pt = x1
            max_pt = x2

    return golden_section(
        min_pt, max_pt, delta, epsilon, iter, is_minimising, iter_count, k + 1, L
    )
