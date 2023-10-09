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
        1. Choose an initial guess for x0
        2. Compute x0 and f'(x0)
        3. Calculate x1 = x0 - f'(x0) / f''(x0)
        4. If |x1 - x0| < epsilon, then x1 is the solution
        5. Else, set x0 = x1 and go to step 2
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
        summary.append([iter_count, min_pt, max_pt, x, fa_derivative, fb_derivative, fx_derivative, objective_function(x)])
        
        assert fa_derivative < 0 and fb_derivative > 0, "f'(a) must be less than 0 and f'(b) must be greater than 0"

        if fx_derivative > 0:
            max_pt = x
        elif fx_derivative < 0:
            min_pt = x
        else:
            break

        iter_count += 1
    
    return True