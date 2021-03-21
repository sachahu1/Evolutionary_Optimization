"""This module defines the Population class.

This module defines the Population class, used to create a population of
individuals. It defines the methods allowed on populations including:

  * Mutation
  * Crossover
  * Elitism
"""
from __future__ import annotations
from typing import Type, Dict, List, Union, Callable, Any, Tuple
import numpy as np

from individual import Individual

PopulationType = List[Individual]
Configuration = Dict[str, Any]
GenotypeConfig = Dict[str, Tuple[type, List[Union[int, float]]]]

class Population:
  """The Population class, used to define a population of individuals.

  Defines a population of individuals, performs the mutations, evaluations and
  selection of individuals.
  """
  def __init__(self, config:Configuration):
    """Inits a population given a population size and genotype shape."""
    self.Individual:Type[Individual] = Individual # pylint: disable=C0103

    self.config:Configuration = config
    if "elitism" in config:
      self.elitism:Union[int, float] = config["elitism"]
    else:
      self.elitism: None = None
    self.pop_size:int = self.config["pop_size"]
    self.indiv_shape:GenotypeConfig = self.config["indiv"]

    if "constraint" in self.config:
      if self.config["constraint"] not in ["Hard", "Soft"]:
        print("Constraint should be Hard or Soft. Defaulting to Soft")
        self.constraint:str = "Soft"
      else:
        self.constraint:str = self.config["constraint"]
    else:
      self.constraint:str = "Soft"

    self.fitness:Callable = self.config["fitness"]
    if "optimization function" in self.config:
      self.optimization_func:Callable = self.config["optimization function"]
    else:
      self.optimization_func:Callable = lambda x:x

    self.pop:List[Individual] = self._init_pop()


  def _init_pop(self) -> PopulationType:
    """Generate a random population of size pop_size."""
    pop = []
    for _ in range(self.pop_size):
      pop.append(self.Individual(self.indiv_shape, constraint=self.constraint))
    return pop

  def __len__(self):
    return len(self.pop)

  def select(self) -> None:
    """Performs the selection of elites and mutates the rest of the population.
    """
    new_pop = []
    if self.elitism is not None:
      elites = self._get_elites()
      new_pop += elites
    pop_idx_list = list(range(len(self)))
    mutants_idx = list(np.random.choice(pop_idx_list, len(self) - len(new_pop)))
    mutants = []
    for idx in mutants_idx:
      mutants.append(self._get_individual(idx))
    self.mutate(mutants)
    new_pop += mutants
    self.pop = new_pop

  def _get_individual(self, idx:int) -> Individual:
    """Returns a deepcopy of an individual in the population by index."""
    return self.pop[idx].copy()

  def evaluate(self) -> None:
    """Evaluates and sorts all individuals in the population from best to worst.
    """
    evaluation_func = lambda i:i.evaluate(self.optimization_func, self.fitness)
    self.pop = sorted(self.pop, key=evaluation_func)

  def scores(self) -> List[float]:
    """Returns a list of fitness scores of all individuals in the population."""
    evaluation_func = lambda i:i.evaluate(self.optimization_func, self.fitness)
    score_mapping = map(evaluation_func, self.pop)
    return list(score_mapping)

  def mutate(self, mutant_pop:Union[None, PopulationType]=None) -> None:
    """Performs random mutations on the population or a given subset.

    Args:
        mutant_pop (Optional): A list of individuals to mutate, generally a
        subset of the population.
    """
    if mutant_pop is not None:
      for individual in mutant_pop:
        individual.mutate()
    else:
      for individual in self.pop:
        individual.mutate()

  def crossover(self, crossover_rate:Union[int, float]) -> None:
    """Performs crossovers for a set of individuals in the population.

    Given a crossover rate, performs crossovers for a set of randomly selected
    individuals in the population. To avoid the population's score deprecating
    due to undesired crossovers, the best parent and the best child are kept
    (instead of removing both parents and adding both children).

    Args:
        crossover_rate (Union[int, float]): The crossover rate (percentage).
          This is the number of individuals in the population subject to
          crossovers.
    """
    parent_size = int(crossover_rate * len(self.pop))
    if parent_size%2 ==1:
      parent_size += 1
    pop_idx = list(range(len(self.pop)))

    parents = np.random.choice(pop_idx, parent_size, replace=False)
    male = []
    female = []
    for i, parent in enumerate(sorted(parents, reverse=True)):
      if i < int(parent_size/2):
        male.append(self.pop.pop(parent))
      else:
        female.append(self.pop.pop(parent))
    for i in range(len(male)):
      male_score = male[i].evaluate(self.optimization_func, self.fitness)
      female_score = female[i].evaluate(self.optimization_func, self.fitness)
      if male_score < female_score:
        best = male[i]
      else:
        best = female[i]
      self.pop.append(best)
    children = []

    for i in range(int(parent_size/2)):
      children.append(self._cross(male[i], female[i]))
    self.pop += children

  def _cross(self, parent1: Individual, parent2: Individual) -> Individual:
    """Performs crossovers between two individuals.

    Args:
        parent1 (Individual): The first parent used in the crossover.
        parent2 (Individual): The second parent used in the crossover.

    Returns:
        best_child (Individual): The best of the two children generated by the
        crossover.
    """
    keys = parent1.genotype.keys()
    # crossing over of the entire genotype makes no sense
    position = np.random.choice(list(range(len(keys)))[1:])
    child1 = Individual(self.indiv_shape)
    child2 = Individual(self.indiv_shape)
    for i, key in enumerate(keys):
      if i < position:
        child1.genotype[key] = parent1.genotype[key].copy()
        child2.genotype[key] = parent2.genotype[key].copy()
      else:
        child1.genotype[key] = parent2.genotype[key].copy()
        child2.genotype[key] = parent1.genotype[key].copy()

    child1_score = child1.evaluate(self.optimization_func, self.fitness)
    child2_score = child2.evaluate(self.optimization_func, self.fitness)
    if child1_score < child2_score:
      best_child = child1
    else:
      best_child = child2
    return best_child

  def _get_elites(self) -> PopulationType:
    """Returns the elites of the population.

    Returns the highest performing individuals in the population. The percentage
    of elites can be adjusted in the configuration.
    """
    elites = self.pop[:int(self.elitism*self.pop_size)]
    return elites

  def show(self) -> None:
    """Displays the populations 5 best and worst performing individuals."""
    for individual in self.pop[:5]:
      indiv_score = individual.evaluate(self.optimization_func, self.fitness)
      indiv_info = (f"fit: {indiv_score} \n"+
                    "indiv: \n"+
                    "{individual.display()}")
      print(indiv_info)
    print("...\n")
    for individual in self.pop[-5:]:
      indiv_score = individual.evaluate(self.optimization_func, self.fitness)
      indiv_info = (f"fit: {indiv_score} \n"+
                    "indiv: \n"+
                    "{individual.display()}")
      print(indiv_info)
