#!/usr/bin/env python3

import argparse

import numpy as np
from tabulate import tabulate

from algorithms.bounding_phase import bounding_phase
from algorithms.exhaustive_search import exhaustive_search
from algorithms.fibonacci_search import fibonnacci_seatch
from algorithms.golden_section import golden_section
from algorithms.newton_raphson import newton_raphson
from algorithms.interval_halving import interval_halving
from constants import headers_dict, summary

# All possible algorithms that can be used
functions_dict = {
    "exhaustive_search": exhaustive_search,
    "bounding_phase": bounding_phase,
    "interval_halving": interval_halving,
    "fibonacci_search": fibonnacci_seatch,
    "golden_section_search": golden_section,
    "newton_raphson": newton_raphson,
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
    default=None,
    required=False,
)
args = parser.parse_args()

if args.delta is None and args.epsilon is None and args.iter is None:
    raise ValueError("Must provide either delta, epsilon or iter")

functions_dict[args.optimisation_type](
    args.minpt, args.maxpt, args.delta, args.epsilon, args.iter, is_minimising=True
)
print(
    tabulate(
        np.array(summary), headers_dict[args.optimisation_type], tablefmt="fancy_grid"
    )
)
