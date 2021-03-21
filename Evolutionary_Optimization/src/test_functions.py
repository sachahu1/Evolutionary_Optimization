"""This module contains basic implementations of simple optimization problems.

This module defines some basic fitness functions to test the evolutionary
process.
"""
from typing import List, Union
import numpy as np

def easom_test(
    x:Union[int,float],
    y:Union[int,float]
) -> Union[int,float]:
  """The Easom function.

  This function computes the Easom function in 3D.

  Args:
    x (float): The value along the x-axis.
    y (float): The value along the y-axis.

  Returns:
    z (float): The value along the z-axis for the Easom function,
    i.e. Easom(x,y).
  """
  return -np.cos(x)*np.cos(y)*np.exp(-((x-np.pi)**2 + (y-np.pi)**2))

def booth_test(
  x:Union[int,float],
  y:Union[int,float]
) -> Union[int,float]:
  """The Booth function.

  This function computes the Booth function in 3D.

  Args:
    x (float): The value along the x-axis.
    y (float): The value along the y-axis.

  Returns:
    z (float): The value along the z-axis for the Booth function,
    i.e. Booth(x,y).
  """
  return (x+2*y -7)**2 + (2*x + y -5)**2

def bukin_test(
  x:Union[int,float],
  y:Union[int,float]
) -> Union[int,float]:
  """The Bukin function.

  This function computes the Bukin function in 3D.

  Args:
    x (float): The value along the x-axis.
    y (float): The value along the y-axis.

  Returns:
    z (float): The value along the z-axis for the Bukin function,
    i.e. Bukin(x,y).
  """
  return 100*np.sqrt(np.abs(y-(0.01*(x**2)))) + 0.01*np.abs(x+10)

def rosenbrock_test(
  *args: Union[int,float, List[Union[int, float]]]
) -> Union[int,float]:
  """The Rosenbrock function.

  This function computes the Rosenbrock function in 3D.

  Args:
    *args (float): The parameters of the Rosenbrock function.

  Returns:
    result (float): The value of the Rosenbrock function
    i.e. Rosenbrock(x, y, ...).
  """
  unpack_args = [*args]
  result = 0
  for i in range(len(unpack_args)-1):
    x = unpack_args[i]
    y = unpack_args[i+1]
    result += (1-x)**2 + 100*(y - x**2)**2
  return result

def gp_test(
  x: Union[int,float],
  y:Union[int,float]
) -> Union[int,float]:
  """The Goldstein-Price function.

  This function computes the Goldstein-Price function in 3D.

  Args:
    x (float): The value along the x-axis.
    y (float): The value along the y-axis.

  Returns:
    z (float): The value along the z-axis for the Goldstein-Price function,
    i.e. Goldstein-Price(x,y).
  """
  z = (1+((x+y+1)**2)*(19 - 14*x + 3*x**2 - 14*y + 6*x*y + 3*y**2))
  z *= (30 + ((2*x - 3*y)**2)*(18 - 32*x + 12*x**2 + 48*y - 36*x*y + 27*y**2))
  return z
