#!/usr/bin/env python3

import argparse

import numpy as np
from tabulate import tabulate

from algorithms.multi_var.evolutionary_search import evolutionary_search
from algorithms.multi_var.simplex_search import simplex_search
from algorithms.single_var.bisection import bisection
from algorithms.single_var.bounding_phase import bounding_phase
from algorithms.single_var.exhaustive_search import exhaustive_search
from algorithms.single_var.fibonacci_search import fibonnacci_seatch
from algorithms.single_var.golden_section import golden_section
from algorithms.single_var.interval_halving import interval_halving
from algorithms.single_var.newton_raphson import newton_raphson
from constants import headers_dict, summary

# All possible algorithms that can be used
functions_dict = {
    "exhaustive_search": exhaustive_search,
    "bounding_phase": bounding_phase,
    "interval_halving": interval_halving,
    "fibonacci_search": fibonnacci_seatch,
    "golden_section_search": golden_section,
    "newton_raphson": newton_raphson,
    "bisection": bisection,
    "evo_search": evolutionary_search,
    "simplex_search": simplex_search,
}

assert functions_dict.keys() == headers_dict.keys()  # Sanity check

parser = argparse.ArgumentParser(description="Get the range and type of optimisation")
parser.add_argument(
    "minpt",
    metavar="min",
    type=int,
    help="Minimum possible value of x. aka lower bound of x",
)
parser.add_argument(
    "maxpt",
    metavar="max",
    type=int,
    help="Maximum possible value of x. aka upper bound of x",
)
parser.add_argument(
    "optimisation_type",
    metavar="func",
    type=str,
    help="Algorithm to be used for optimisation",
    choices=functions_dict.keys(),
)
parser.add_argument(
    "--delta", type=float, help="Step size", default=None, required=False
)
parser.add_argument(
    "--epsilon",
    type=float,
    help="Value below which to stop",
    default=None,
    required=False,
)
parser.add_argument(
    "--iter",
    type=int,
    help="Number of iteration to perform",
    default=100,
    required=False,
)
args = parser.parse_args()

if args.delta is None and args.epsilon is None and args.iter is None:
    raise ValueError("Must provide either delta, epsilon or iter")

functions_dict[args.optimisation_type](
    args.minpt, args.maxpt, args.delta, args.epsilon, args.iter, is_minimising=True
)

# Ensure that the summary is of the correct shape
assert len(summary) > 0 and len(summary[0]) == len(headers_dict[args.optimisation_type])

print(
    tabulate(
        np.array(summary), headers_dict[args.optimisation_type], tablefmt="fancy_grid"
    )
)
