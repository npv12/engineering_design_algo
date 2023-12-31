import numpy as np

from constants import objective_function, summary
from utils import find_derivative


def bisection(
    min_pt: float,
    max_pt: float,
    delta: float | None = None,
    epsilon: float | None = None,
    iter: int | None = None,
    is_minimising: bool = False,
) -> bool:
    """
    Working ->
        1. set x = (a + b) / 2 where f'(a) < 0 and f'(b) > 0
        2. If f'(x) > 0, then set b = x
        3. If f'(x) < 0, then set a = x
        4. If f'(x) = 0, then stop
        5. Repeat steps 1-4 until |f'(x)| < epsilon
    """
    if not epsilon:
        raise ValueError("Must provide epsilon for newton raphson")

    iter_count = 0
    fx_derivative = 1000

    while np.abs(fx_derivative) > epsilon:
        x = (min_pt + max_pt) / 2
        fa_derivative = find_derivative(objective_function, min_pt)
        fb_derivative = find_derivative(objective_function, max_pt)
        fx_derivative = find_derivative(objective_function, x)
        summary.append(
            [
                iter_count,
                min_pt,
                max_pt,
                x,
                fa_derivative,
                fb_derivative,
                fx_derivative,
                objective_function(x),
            ]
        )

        assert (
            fa_derivative < 0 and fb_derivative > 0
        ), "f'(a) must be less than 0 and f'(b) must be greater than 0"

        if fx_derivative > 0:
            max_pt = x
        elif fx_derivative < 0:
            min_pt = x
        else:
            break

        iter_count += 1

    return True
