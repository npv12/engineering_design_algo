from constants import objective_function, summary


def interval_halving(
    min_pt: float,
    max_pt: float,
    delta: float | None = None,
    epsilon: float | None = None,
    iter: int | None = None,
    is_minimising: bool = False,
    iter_count=0,
) -> bool:
    """
    Working ->
        1. Calculate xm = (x1 + x2) / 2
        2. Start with x1 = min_pt + L / 4, x2 = max_pt - L / 4, where L = max_pt - min_pt
        3. If f(x1) < f(xm) then set x2 = xm else if f(x2) < f(xm) then set x1 = xm else set x1 = x1 and x2 = x2
        4. Repeat steps 1-3 until L < epsilon
    """
    mean_pt = (min_pt + max_pt) / 2
    L = max_pt - min_pt

    if not iter: iter = 100

    if epsilon and L < epsilon:
        if is_minimising:
            print("Found minima")
        else:
            print("Found maxima")
        return True
    
    if delta and delta > L:
        if is_minimising:
            print("Found minima")
        else:
            print("Found maxima")
        return True

    if iter_count > iter:
        print("Could not find minima/maxima")
        return False

    x1 = min_pt + L / 4
    x2 = max_pt - L / 4

    fx1 = objective_function(x1)
    fxm = objective_function(mean_pt)
    fx2 = objective_function(x2)

    iter_count += 1
    summary.append([iter_count, min_pt, max_pt, x1, mean_pt, x2, fx1, fxm, fx2])
    if is_minimising:
        if fx1 < fxm:
            max_pt = mean_pt
        elif fx2 < fxm:
            min_pt = mean_pt
        else:
            min_pt = x1
            max_pt = x2
    else:
        if fx1 > fxm:
            max_pt = mean_pt
        elif fx2 > fxm:
            min_pt = mean_pt
        else:
            min_pt = x1
            max_pt = x2
    return interval_halving(min_pt, max_pt, delta, epsilon, iter, is_minimising, iter_count)
