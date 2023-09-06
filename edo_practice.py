#!/usr/bin/env python3

import argparse

import numpy as np
from tabulate import tabulate

from algorithms.bounding_phase import bounding_phase
from algorithms.exhaustive_search import exhaustive_search
from constants import headers_dict, summary

# All possible algorithms that can be used
functions_dict = {
    "exhaustive_search": exhaustive_search,
    "bounding_phase": bounding_phase,
}

assert functions_dict.keys() == headers_dict.keys() # Sanity check

parser = argparse.ArgumentParser(description="Get the range and type of optimisation")
parser.add_argument(
    "minpt", metavar="min", type=int, help="Minimum possible value of x. aka lower bound of x"
)
parser.add_argument(
    "maxpt", metavar="max", type=int, help="Maximum possible value of x. aka upper bound of x"
)
parser.add_argument(
    "optimisation_type", metavar="func", type=str, help="Algorithm to be used for optimisation", choices=functions_dict.keys()
)
parser.add_argument(
    "--delta", type=float, help="Step size", default=0.02, required=False
)

args = parser.parse_args()
functions_dict[args.optimisation_type](args.minpt, args.maxpt, args.delta, is_minimising=True)
print(
    tabulate(
        np.array(summary), headers_dict[args.optimisation_type], tablefmt="fancy_grid"
    )
)
