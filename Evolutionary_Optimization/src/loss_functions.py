"""This module contains some basic implementations of simple fitness functions.

This module defines some basic fitness functions to use during the evolutionary
process.
"""
from typing import Union
import numpy as np

def MSE(x:Union[int,float]) -> Union[int,float]:
  """A basic implementation of Mean Squared Error.

  This function computes the Mean Squared Error between x and an objective_value
  defined through the configuration file.

  Args:
    x (float): The value to evaluate. This is most likely the individual's
      phenotype.

  Returns:
    fitness (float): The individual's Mean Squared Error on the optimization
      task.
  """
  from config import objective_value
  return (x - objective_value)**2

def L1(x:Union[int,float]) -> Union[int,float]:
  """A basic implementation of the L1 norm.

  This function computes the L1 norm between x and an objective_value
  defined through the configuration file.

  Args:
    x (float): The value to evaluate. This is most likely the individual's
      phenotype.

  Returns:
    fitness (float): The individual's L1 error on the optimization task.
  """
  from config import objective_value
  return np.abs(x - objective_value)

def Minimize(x:Union[int,float]) -> Union[int,float]:
  """The fitness to use when trying to minimize a function.

  This is the fitness to use in order to perform a minimization task. This is
  important so the evolution process can evaluate and compare individuals.

  Args:
    x (float): The value to evaluate. This is most likely the individual's
      phenotype.

  Returns:
    x (float): The individual's fitness on the optimization task.
  """
  return x

def Maximize(x:Union[int,float]) -> Union[int,float]:
  """The fitness to use when trying to maximize a function.

  This is the fitness to use in order to perform a maximization task. This is
  important so the evolution process can evaluate and compare individuals.

  Args:
    x (float): The value to evaluate. This is most likely the individual's
      phenotype.

  Returns:
    x (float): The individual's fitness on the optimization task.
  """
  return -x
