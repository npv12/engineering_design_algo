import numpy as np

from constants import objective_function, summary
from utils import find_double_derivative, find_derivative, find_random_start


def newton_raphson(
    min_pt: float,
    max_pt: float,
    delta: float | None = None,
    epsilon: float | None = None,
    iter: int | None = None,
    is_minimising: bool = False,
) -> bool:
    """
    Working ->
        1. Choose an initial guess for x0
        2. Compute x0 and f'(x0)
        3. Calculate x1 = x0 - f'(x0) / f''(x0)
        4. If |x1 - x0| < epsilon, then x1 is the solution
        5. Else, set x0 = x1 and go to step 2
    """
    if not epsilon:
        raise ValueError("Must provide epsilon for newton raphson")

    x0 = find_random_start(min_pt, max_pt, epsilon)

    assert x0 > min_pt and x0 < max_pt, "x0 must be between min_pt and max_pt"

    iter_count = 0
    f_derivative = 1000

    while np.abs(f_derivative) > epsilon:
        f_value = objective_function(x0)
        f_derivative = find_derivative(objective_function, x0)
        f_double_derivative = find_double_derivative(objective_function, x0)

        x1 = x0 - (f_derivative / f_double_derivative)

        # Keep it bounded
        if x1 < min_pt:
            x1 = min_pt
        elif x1 > max_pt:
            x1 = max_pt

        summary.append(
            [iter_count, x0, f_value, f_derivative, f_double_derivative, x1 - x0]
        )
        x0 = x1
        iter_count += 1

    return True
