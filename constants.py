# Our objective function
def objective_function(x: float) -> float:
    return x ** 2 / 2 + 125 / x

# Basic var meant for visualisation
summary = []

headers_dict = {
    "exhaustive_search": ['iteration', 'x1', 'x2', 'x3', 'f1', 'f2', 'f3']
}