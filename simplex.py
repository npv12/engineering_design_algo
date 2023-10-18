# Description: This file contains the implementation of the simplex search algorithm submitted for EDO Assignment 1
# Author: Arka Pal (19ME02043), Mechanical Engineering, IIT Bhubaneswar
# Author: Nedungadi Pranav V (19ME02005), Mechanical Engineering, IIT Bhubaneswar
# Date: 15th October 2023

# Features
# 1. Uses the simplex search algorithm to find the global minima of the Himmelblau's function
# 2. Uses the tabulate library to print the summary table
# 3. Uses the matplotlib library to plot the points for each iteration
# 4. Uses the PIL library to generate the gif from the images
# 5. Uses multiple initial points to ensure that all the global minima are found
# 6. Takes into account the stopping criteria and terminates the algorithm when the points are too close to each other
# 7. Considers if the points are collinear and restarts the algorithm with different initial points
# 8. Dynamically plots the number of minima and gif according to the number of initial points

import os
import numpy as np
from random import uniform
from tabulate import tabulate
import matplotlib.pyplot as plt
import glob
from PIL import Image

# --------------------------------------------------------------------------------- #
# --------------------------------- Input variable -------------------------------- #
# --------------------------------------------------------------------------------- #

# These are the only values that should be changed for getting a different output
lb = [-5, -5]
ub = [5, 5]
gamma = 1.5  # Gamma value for the reflection. Taken from notes
beta = 0.5  # Beta value for the contraction. Taken from notes
epsilon = 0.000001  # Epsilon value for the stopping criteria. Taken from notes


# --------------------------------------------------------------------------------- #
# --------------------------------- Objective function ---------------------------- #
# --------------------------------------------------------------------------------- #
def himmelblau_function(x, y):
    """
    Himmelblau's function is a multi-modal function, used as a performance test problem for optimization algorithms.
    This has 4 global minima.
    The minima are found at
        f(3.0, 2.0) = 0.0
        f(-2.805118, 3.131312) = 0.0
        f(-3.779310, -3.283186) = 0.0
        f(3.584428, -1.848126) = 0.0

    Args:
        x (float): x coordinate
        y (float): y coordinate
    """
    return (x**2 + y - 11) ** 2 + (x + y**2 - 7) ** 2


# Folder name to store the frames used to generate the animation
frame_folder = "./Animation"

# Array which stores the points for each iteration. Used to plot the points in the animation and visualize the algorithm
summary = []


# --------------------------------------------------------------------------------- #
# --------------------------------- Helper functions ------------------------------ #
# --------------------------------------------------------------------------------- #
def add_to_summary(iteration, simplex):
    """
    Helper function to properly format the summary table.
    Convert the nd array into a proper printable string for great output
    Args:
        iteration (int): Iteration number
        simplex (ndarray): Simplex array

    Returns:
        None. Appends to the summary array
    """

    summary_item = [iteration]
    for point in simplex:
        str = "("
        for coordinate in point:
            str += f"{round(coordinate, 3)}, "

        str = str[:-2]
        str += ")"
        summary_item.append(str)

    summary_item.append(himmelblau_function(*simplex[0]))
    summary.append(summary_item)


def find_area(points):
    """
    There are cases where all the three points used might be colinear.
    To ensure the lines aren't colinear, we find the area of resultant rectangle.
    If the area is 0 then it is colinear.

    Args:
        points: 3 points in the simplex
    Returns:
        None: Plots the image and saves it in Animation folder
    """
    A = np.append(points.T, np.array([[1, 1, 1]]), axis=0)
    return abs(np.linalg.det(A))


def plot_function(pointsforplot, lb, ub, iteration=0):
    """
    Plot the function and the points for each iteration
    Args:
        pointsforplot: Points to plot
        lb: Lower bound
        ub: Upper bound
        iteration: Iteration number
    """
    x = np.linspace(lb[0], ub[0], 50)
    y = np.linspace(lb[1], ub[1], 50)

    X, Y = np.meshgrid(x, y)
    Z = himmelblau_function(X, Y)

    fig1, ax1 = plt.subplots()
    ax1.contour(X, Y, Z, cmap="coolwarm", levels=50)
    ax1.scatter(pointsforplot[0, 0], pointsforplot[0, 1], color="red", marker="*", s=50)
    ax1.scatter(pointsforplot[1, 0], pointsforplot[1, 1], color="red", marker="*", s=50)
    ax1.scatter(pointsforplot[2, 0], pointsforplot[2, 1], color="red", marker="*", s=50)
    ax1.plot(
        [pointsforplot[0, 0], pointsforplot[1, 0]],
        [pointsforplot[0, 1], pointsforplot[1, 1]],
        color="red",
        linewidth=1,
    )
    ax1.plot(
        [pointsforplot[1, 0], pointsforplot[2, 0]],
        [pointsforplot[1, 1], pointsforplot[2, 1]],
        color="red",
        linewidth=1,
    )
    ax1.plot(
        [pointsforplot[0, 0], pointsforplot[2, 0]],
        [pointsforplot[0, 1], pointsforplot[2, 1]],
        color="red",
        linewidth=1,
    )
    ax1.set(xlabel="x1", ylabel="x2")
    ax1.set_title("Iteration {}".format(iteration))
    plt.savefig(f"{frame_folder}/fig{str(iteration).zfill(3)}.png", dpi=400)
    plt.show()


def make_gif(frame_folder, count):
    """
    Uses all the images from the folder and creates a gif
    Args:
        frame_folder: Folder name
        count: Count of the gif

    """
    frames = [Image.open(image) for image in sorted(glob.glob(f"{frame_folder}/*.png"))]
    frame_one = frames[0]
    frame_one.save(
        "Simplex" + str(count) + ".gif",
        format="GIF",
        append_images=frames,
        save_all=True,
        duration=1000,
        loop=5,
    )


# --------------------------------------------------------------------------------- #
# --------------------------------- Main function --------------------------------- #
# --------------------------------------------------------------------------------- #
def simplex_search(
    lb,
    ub,
    gamma=None,
    beta=None,
    epsilon=None,
    iter=500,
):
    """
    Uses the simplex search algorithm to find the global minima of the Himmelblau's function
    Args:
        lb: Lower bound - List of lower bounds for each dimension
        ub: Upper bound - List of upper bounds for each dimension
        gamma: Gamma value for the reflection
        beta: Beta value for the contraction
        epsilon: Epsilon value for the stopping criteria
        iter: Number of iterations

    ArgTypes:
        lb: list
        ub: list
        gamma: float
        beta: float
        epsilon: float
        iter: int

    Returns:
        solutions: List of solutions
        solutions_simplex: List of simplices for each solution
    """
    solutions = []
    solutions_simplex = []

    # Sanity checks. Ensure the inputs are valid
    assert epsilon, "Must provide epsilon for evolutionary search"
    assert gamma > 1, "Gamma must be greater than 1"
    assert 0 < beta < 1, "Beta must lie between 0 and 1"
    assert lb[0] < ub[0] and lb[1] < ub[1], "Lower bound must be less than upper bound"

    # Run the algorithm for 16 different initial points
    # This is done to ensure we find all the global minima
    for num in range(16):
        # Generate 3 random points within the search space
        # Ensure that the points are not collinear.
        # If colinear find new points
        while True:
            initial_simplex = np.array(
                [
                    [uniform(lb[0], ub[0]), uniform(lb[1], ub[1])],
                    [uniform(lb[0], ub[0]), uniform(lb[1], ub[1])],
                    [uniform(lb[0], ub[0]), uniform(lb[1], ub[1])],
                ]
            )

            if find_area(initial_simplex) > 1e-6:
                break

        # Sort the points based on the function value
        simplex = np.array(initial_simplex)
        add_to_summary(0, simplex)
        simplex_points = np.array([simplex])

        # Run the algorithm for the given number of iterations
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
                    # xnew = centroid + 2 * (x2 - centroid)
                    xnew = (1 + gamma) * centroid - gamma * simplex[-1]
                    simplex[-1] = xnew

                else:
                    if himmelblau_function(*simplex[-2]) < himmelblau_function(
                        *x2
                    ) and himmelblau_function(*x2) < himmelblau_function(*simplex[-1]):
                        xnew = (1 + beta) * centroid - beta * simplex[-1]
                    else:
                        xnew = (1 - beta) * centroid + beta * simplex[-1]
                    simplex[-1] = xnew

            # When the points go out of bound, we bring them back to the bound
            # Ensure that the points are within the search space
            if not (
                (lb[0] < simplex[-1][0] < ub[0]) and (lb[1] < simplex[-1][1] < ub[1])
            ):
                print("Out of bound!")
                for i in range(len(lb)):
                    if simplex[-1][i] < lb[i]:
                        simplex[-1][i] = lb[i]
                    elif simplex[-1][i] > ub[i]:
                        simplex[-1][i] = ub[i]

            # If the points are collinear, we restart the algorithm with different initial points
            if (
                find_area(simplex) < 0.01
                and np.sqrt(np.mean((simplex[0] - simplex[1]) ** 2)) > 1
            ):
                print("Points are collinear: Restaring with different initial points")
                simplex = np.array(
                    [
                        [uniform(lb[0], ub[0]), uniform(lb[1], ub[1])],
                        [uniform(lb[0], ub[0]), uniform(lb[1], ub[1])],
                        [uniform(lb[0], ub[0]), uniform(lb[1], ub[1])],
                    ]
                )

            # If the points are too close to each other, we stop the algorithm
            # This is the termination criteria
            if np.all(
                np.abs(
                    himmelblau_function(*simplex[0]) - himmelblau_function(*simplex[-1])
                )
                < epsilon
            ):
                print("Epsilon reached!")
                break

            add_to_summary(i, simplex)
            simplex_points = np.append(simplex_points, [simplex], axis=0)

        # Ensure that the solutions are unique.
        # If the distance between the points is less than 1e-2, then they are the same
        flag = True
        for i in range(len(solutions)):
            if np.sqrt(np.mean((simplex[0] - solutions[i]) ** 2)) < 1e-2:
                flag = False
                break

        if flag:
            solutions.append(simplex[0])
            solutions_simplex.append(simplex_points)
    return solutions, solutions_simplex


# --------------------------------------------------------------------------------- #
# --------------------------------- Setup ----------------------------------------- #
# --------------------------------------------------------------------------------- #

# Create a folder named frame_folder to store the images
if not os.path.exists(frame_folder):
    os.makedirs(frame_folder)

# --------------------------------------------------------------------------------- #
# --------------------------------- Run the algorithm ----------------------------- #
# --------------------------------------------------------------------------------- #
sol, sol_simplex = simplex_search(lb, ub, gamma, beta, epsilon)

# Print the summary table
print(
    tabulate(
        np.array(summary),
        ["iteration", "x0", "x1", "x2", "func"],
        tablefmt="fancy_grid",
    )
)


# Plot the points for each iteration
for i in range(len(sol)):
    # Plot the points for each iteration.
    # The points are stored in the sol_simplex array
    # The images are later used to generate the gif
    for j in range(sol_simplex[i].shape[0]):
        plot_function(sol_simplex[i][j], lb, ub, iteration=j)
    make_gif(frame_folder, i)
