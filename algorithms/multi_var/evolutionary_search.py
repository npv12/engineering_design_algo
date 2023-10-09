import numpy as np

from constants import himmelblau_function, summary


def hyper_cube_points(x: float, delta: float):
    cubepoints = np.zeros((6, 3))
    cubepoints[0, 0:2] = [x[0] - delta[0] / 2, x[1] - delta[1] / 2]
    cubepoints[1, 0:2] = [x[0] + delta[0] / 2, x[1] - delta[1] / 2]
    cubepoints[2, 0:2] = [x[0] + delta[0] / 2, x[1] + delta[1] / 2]
    cubepoints[3, 0:2] = [x[0] - delta[0] / 2, x[1] + delta[1] / 2]

    cubepoints[4, 0:2] = cubepoints[0, 0:2]
    cubepoints[5, 0:2] = [x[0], x[1]]

    cubepoints[0, 2] = himmelblau_function(cubepoints[0, 0], cubepoints[0, 1])
    cubepoints[1, 2] = himmelblau_function(cubepoints[1, 0], cubepoints[1, 1])
    cubepoints[2, 2] = himmelblau_function(cubepoints[2, 0], cubepoints[2, 1])
    cubepoints[3, 2] = himmelblau_function(cubepoints[3, 0], cubepoints[3, 1])

    cubepoints[4, 2] = cubepoints[0, 2]
    cubepoints[5, 2] = himmelblau_function(cubepoints[5, 0], cubepoints[5, 1])

    return cubepoints


# def hyper_cube_points(x: float, delta: float):
#     cubepoints = np.zeros((6, 3))
#     x0, x1 = x[0], x[1]
#     d0, d1 = delta[0], delta[1]
#     cubepoints[0:4, 0:2] = [[x0-d0/2, x1-d1/2], [x0+d0/2, x1-d1/2], [x0+d0/2, x1+d1/2], [x0-d0/2, x1+d1/2]]
#     cubepoints[4:6, 0:2] = [[x0-d0/2, x1-d1/2], [x0, x1]]
#     cubepoints[:, 2] = himmelblau_function(cubepoints[:, 0], cubepoints[:, 1])
#     return cubepoints


def evolutionary_search(
    min_pt: float,
    max_pt: float,
    delta: float | None = None,
    epsilon: float | None = None,
    iter: int | None = 100,
    is_minimising: bool = False,
) -> bool:
    """
    Working ->
    """
    if not epsilon:
        raise ValueError("Must provide epsilon for newton raphson")

    x0 = np.array([1, 1])

    delta = np.array([2, 2])
    iter_count = 0

    delta_mag = np.lina.norm(delta)
    while delta_mag > epsilon and iter_count < iter:
        hcpts = hyper_cube_points(x0, delta)
        x1 = hcpts[np.argmin(hcpts[:, 2]), 0:2]

        summary.append(
            [
                iter_count,
                np.round(hcpts[5, :], 2),
                np.round(hcpts[0:], 2),
                np.round(hcpts[0:], 2),
                np.round(hcpts[1:], 2),
                np.round(hcpts[2:], 2),
                np.round(hcpts[3:], 2),
                delta,
                np.linalg.norm(delta),
            ]
        )

        if x0[0] == x1[0] and x0[1] == x1[1]:
            delta = delta / 2
        else:
            x0 = x1

        iter_count += 1
        delta_mag = np.linalg.norm(delta)

    return True
