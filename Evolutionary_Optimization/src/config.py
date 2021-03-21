"""A configuration file to configure your optimization task.

This module serves as a configuration file. It contains all the parameters
that can be modified for the purpose of the optimization task.

Todo:
    * Remove config file and make command line argument parser.
"""

from test_functions import booth_test
from loss_functions import Minimize

objective_value = 3

min_boundary = -10
max_boundary = 10

plot_name="Booth_function_test"

genotype = {
    "x": (float, [min_boundary, max_boundary]),
    "y": (float, [min_boundary, max_boundary]),
}

fitness = Minimize
test = booth_test

config = {
    "pop_size":100,
    "elitism":0.3,
    "indiv": genotype,
    "generations": 100,
    "crossover": True,
    "crossover rate": 0.3,
    "constraint":"Hard",

    "fitness": fitness,
    "optimization function": test,

    "verbose" : True,
    "print rate" : 10,
}
