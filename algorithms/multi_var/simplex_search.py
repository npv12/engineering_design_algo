import numpy as np

from constants import himmelblau_function, summary


def add_to_summary(iteration, simplex):
    """
    Helper function to properly format the summary table.
    Convert the nd array into a proper printable string for great output
    """

    summary_item = [iteration]
    for point in simplex:
        str = "("
        for coordinate in point:
            str += f"{round(coordinate, 3)}, "

        str = str[:-2]
        str += ")"
        summary_item.append(str)

    summary.append(summary_item)


def generate_initial_simplex(min_pt, max_pt, epsilon, n = 3):
    """
    Randomly generate n points and return a nd array. 
    """

    return np.random.uniform(min_pt + epsilon, max_pt - epsilon, size=(n, 2))


def simplex_search(
    min_pt: float,
    max_pt: float,
    delta: float | None = None,
    epsilon: float | None = None,
    iter: int | None = 100,
    is_minimising: bool = False,
) -> bool:
    """
    TODO: This doesn't use min_pt and max_pt. This is a todo. Randomly generate the initial simplex
    Working ->
    """
    if not epsilon:
        raise ValueError("Must provide epsilon for evolutionary search")

    # Initial simplex
    initial_simplex = generate_initial_simplex(min_pt, max_pt, epsilon)
    n = len(initial_simplex[0])
    simplex = np.array(initial_simplex)
    add_to_summary(0, simplex)

    for i in range(iter):
        simplex = simplex[
            np.argsort([himmelblau_function(x[0], x[1]) for x in simplex])
        ]
        centroid = np.mean(simplex[:-1], axis=0)

        x2 = centroid + (centroid - simplex[-1])
        if (
            himmelblau_function(*simplex[0])
            <= himmelblau_function(*x2)
            < himmelblau_function(*simplex[-2])
        ):
            simplex[-1] = x2
        else:
            if himmelblau_function(*x2) < himmelblau_function(*simplex[0]):
                x1 = centroid + 2 * (x2 - centroid)
                if himmelblau_function(*x1) < himmelblau_function(*x2):
                    simplex[-1] = x1
                else:
                    simplex[-1] = x2
            else:
                x0 = centroid + 0.5 * (simplex[-1] - centroid)
                if himmelblau_function(*x0) < himmelblau_function(*simplex[-1]):
                    simplex[-1] = x0
                else:
                    for i in range(1, n):
                        simplex[i] = simplex[0] + 0.5 * (simplex[i] - simplex[0])

        if np.all(
            np.abs(himmelblau_function(*simplex[0]) - himmelblau_function(*simplex[-1]))
            < epsilon
        ):
            break

        add_to_summary(i, simplex)
