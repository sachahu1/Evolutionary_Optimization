#!/usr/bin/env python
# coding: utf-8
"""Main module to run the Evolutionary algorithm on a optimization problem.

This module is used to define the steps of the optimization process.

Todo:
    * Remove config, make argparse
"""

from ea import EA
from config import config, plot_name

if __name__ == "__main__":
  ea = EA(config)
  ea.evolve()
  ea.visualise(plot_name)
