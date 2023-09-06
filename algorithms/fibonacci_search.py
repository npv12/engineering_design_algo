from functools import lru_cache

from constants import objective_function, summary


@lru_cache(None)
def fibonacci(num: int) -> int:
    if num < 0:
        raise ValueError("Cannot find fibonacci of negative numbers")

    elif num < 2:
        return num

    return fibonacci(num - 1) + fibonacci(num - 2)


def fibonnacci_seatch(
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

    lk = fibonacci(iter - k + 1) / fibonacci(iter + 1) * L

    if epsilon and lk < epsilon:
        if is_minimising:
            print("Found minima")
        else:
            print("Found maxima")
        return True

    x1 = min_pt + lk
    x2 = max_pt - lk

    fx1 = objective_function(x1)
    fx2 = objective_function(x2)

    iter_count += 1
    summary.append([iter_count, min_pt, max_pt, lk, x1, x2, fx1, fx2, k])

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

    return fibonnacci_seatch(
        min_pt, max_pt, delta, epsilon, iter, is_minimising, iter_count, k + 1, L
    )
