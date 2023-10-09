from functools import lru_cache

# Our objective function
@lru_cache(None)
def objective_function(x: float) -> float:
    return x ** 2 / 2 + 125 / x

@lru_cache(None)
def himmelblau_function(x: float, y: float) -> float:
    return (x**2 + y - 11)**2 + (x + y**2 - 7)**2


# Basic var meant for visualisation
summary = []

headers_dict = {
    "exhaustive_search": ["iteration", "x1", "x2", "x3", "f1", "f2", "f3"],
    "bounding_phase": ["iteration", "xkm1", "xk", "xkp1", "f(xk)", "f(xkp1)"],
    "interval_halving": ["iteration", "min_pt", "max_pt", "x1", "mean_pt", "x2", "f(x1)", "f(xm)", "f(x2)"],
    "fibonacci_search": ["iteration", "min_pt", "max_pt", "lk", "x1", "x2", "f(x1)", "f(x2)", "k"],
    "golden_section_search": ["iteration", "min_pt", "max_pt", "L2", "x1", "x2", "f(x1)", "f(x2)"],
    "newton_raphson": ["iteration", "x0", "f(x0)", "f'(x0)", "f''(x0)", "dx"],
}

GAMMA = 1.618 # Golder ratio