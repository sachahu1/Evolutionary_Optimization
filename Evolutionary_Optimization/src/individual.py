"""This module defines the Individual class.

This module defines the Individual class, used to create inidividuals.
It defines the methods allowed on individuals, including the mutations
and evaluation of individuals.

Todo:
    * examples
    * doctest
"""
from __future__ import annotations
from typing import Union, Dict, Callable, Tuple, List, Optional

from copy import deepcopy

from gene import Gene

GenotypeConfig = Dict[str, Tuple[type, List[Union[int, float]]]]
Genotype = Dict[str, Gene]

class Individual:
  """The Individual class, used to define the individuals of a population.

  Defines an individual in a population, performs the mutations and
  evaluations of individuals.
  """
  def __init__(self,
    individual_genotype:GenotypeConfig,
    constraint:str="Soft",
  ) -> None:
    """Inits Individual given a genotype shape."""
    self.constraint:Optional[str] = constraint
    self.genotype:Genotype = self._init_genotype(individual_genotype)

  def _init_genotype(self, individual_genotype:GenotypeConfig) -> Genotype:
    """Inits an individuals genotype given a genotype shape.

    Args:
        individual_genotype (dict): The desired genotype shape.

    Returns:
        genotype (Dict): The individual's randomly initialized genotype.
    """
    genotype = {}
    for k, v in individual_genotype.items():
      gene_type, minimum, maximum = v[0], v[1][0], v[1][1]
      genotype[k] = Gene(
        gene_type=gene_type,
        minimum=minimum,
        maximum=maximum,
        constraint=self.constraint,
      )
    return genotype

  def _mutate_gene(self, gene:str) -> None:
    """Adds a random mutation to a given gene.

    Args:
        gene (str): The individual's gene to mutate.
    """
    self.genotype[gene].mutate()

  def copy(self) -> Individual:
    """Returns a deepcopy of the individual."""
    return deepcopy(self)

  def mutate(self) -> None:
    """Mutates the entire individual."""
    for gene, _ in self.genotype.items():
      self._mutate_gene(gene)

  def display(self) -> str:
    """Returns the individual's genotype in a readable fstring.
    """
    genotype_str = ""
    for k, v in self.genotype.items():
      genotype_str += f"     {k} : {v.value()}\n"
    return genotype_str

  def evaluate(
    self,
    optimization_func:Callable=lambda x:x,
    fitness:Callable=lambda x:x,
  ) -> Union[int,float]:
    """Evaluates the performance of an individual on the task to optimize.

    Args:
        optimization_func (Callable): The problem to optimize. This can be
        manually defined or can be one of the test functions.
        fitness (Callable): The fitness function to use to optimize the task.
          For example, this can be a minimization problem (fitness=minimize).
          This can be manually defined or can be one of the test functions.

    Returns:
        score (float): The individual's score on the optimization task.

    TODO:
        * Normalize scores between 0 and 1.
    """
    args = []
    for v in self.genotype.values():
      args.append(v.value())
    score = fitness(optimization_func(*args))
    return score

if __name__=="__main__":
  import doctest
  doctest.testmod(verbose=True, optionflags=doctest.ELLIPSIS)
