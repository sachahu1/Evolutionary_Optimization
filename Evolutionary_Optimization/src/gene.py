"""This module defines the Gene class.

This module defines the Gene class, used to create each individual's genes.
It defines the methods allowed on genes, including the mutations.
"""
from __future__ import annotations
from typing import Union

from copy import deepcopy
import numpy as np

class Gene:
  """The Gene class, used to define an individual's genes.

  Defines an individual's gene, performs the mutations of an individual's genes.
  """
  def __init__(
    self,
    gene_type:type,
    minimum:Union[int, float],
    maximum:Union[int, float],
    constraint:str="Soft",
  ) -> None:
    """Inits Individual's gene given a gene type, minimum and maximum values."""
    self.type:type = gene_type
    self.gene:Union[int, float] = self._init_gene(minimum, maximum)
    self.minimum:Union[int, float] = minimum
    self.maximum:Union[int, float] = maximum
    self.constraint:str = constraint

  def _init_gene(
    self,
    minimum:Union[int, float],
    maximum:Union[int, float],
  ) -> Union[int, float]:
    """Inits Individual's gene given a gene type, minimum and maximum values."""
    if self.type == int:
      return np.random.randint(low=minimum, high=maximum)
    elif self.type == float:
      return np.random.uniform(low=minimum, high=maximum)
    else:
      print("Error: Type not recognized. Defaulting to float type")
      return np.random.uniform(low=minimum, high=maximum)

  def mutate(self) -> None:
    """Performs a random mutation on the gene."""
    if self.type == int:
      mutation = np.random.randn(1).astype(int)[0]
    elif self.type == float:
      mutation = np.random.randn(1)[0]
    if self.constraint == "Hard":
      if (
        self.gene+mutation < self.maximum and self.gene+mutation > self.minimum
      ):
        self.gene += mutation
    else:
      self.gene += mutation

  def value(self) -> Union[int, float]:
    """Returns the gene's value."""
    return self.gene

  def copy(self) -> Gene:
    """Returns a deepcopy of the gene."""
    return deepcopy(self)
