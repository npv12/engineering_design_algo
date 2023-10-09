# Optimisation Algorithms

## Introduction
This repo consists of implementation of a few algorithms as they were taught in the course of Optimisation Algorithms. The algorithms are implemented in Python 3.11. The algorithms implemented are:

## Requirements
* Python 3.11
* Numpy
* Tabulate

You can install all dependency using 
```bash
pip install -r requirements.txt
```

## Uni Modal Functions

### Single variable optimisation
1. Direct Search Method
    * Exhaustive Search
    * Fibonacci Search
    * Golden Section Search
    * Interval Halving Method
    * Interval Methods
2. Gradient based methods
    * Newton-Raphson Method
    * Bisection Method

### Multi variable optimisation
1. Direct Search
    * Evolutionary Search
2. Gradient Search

## Usage
For entire list of possible arguments, run:
```bash
python main.py -h
```
You can run the main file as follows
```bash
python main,py <lower_bound> <upper_bound> <function_name> --delta <delta> --epsilon <epsilon> --iter <iteration count max>
```

For example, to run the exhaustive search method on the function f(x) = x^2 in the range [0, 10] with delta = 10, epsilon = 0.001 and max iterations = 20, run:
```bash
python main,py 0 10 exhaustive_search --delta 10 --epsilon 0.001 --iter 20
```

