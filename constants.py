# Our objective function
def objective_function(x: float) -> float:
    return x**2 / 2 + 125 / x


# Basic var meant for visualisation
summary = []

headers_dict = {
    "exhaustive_search": ["iteration", "x1", "x2", "x3", "f1", "f2", "f3"],
    "bounding_phase": ["iteration", "xkm1", "xk", "xkp1", "f(xk)", "f(xkp1)"],
    "interval_halving": ["iteration", "min_pt", "max_pt", "x1", "mean_pt", "x2", "f(x1)", "f(xm)", "f(x2)"],
}
