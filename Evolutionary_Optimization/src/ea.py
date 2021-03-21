"""This module defines the Evolutionary Algorithm (EA) class.

This module defines the EA class, used to configure, create and train an
evolutionary algorithm. It defines the methods and processes currently
supported including:

  * Evolution of a EA
  * 4D visualisation of the evolution in the phenotype space.

Example:
  >>> import loss_functions
  >>> import test_functions
  >>> from gene import Gene
  >>> genotype = {
  ... "x": (float, [-100,100]),
  ... "y":(float, [-20,20]),
  ... }
  >>> config = {
  ...  "pop_size":100,
  ...  "elitism":0.3,
  ...  "indiv": genotype,
  ...  "generations": 100,
  ...  "crossover": True,
  ...  "crossover rate": 0.3,
  ...  "constraint":"Hard",
  ...  "fitness": loss_functions.Minimize,
  ...  "optimization function": test_functions.easom_test,
  ...  "verbose" : True,
  ...  "print rate" : 10,
  ...  }
  >>> ea = EA(config)
  >>> ea.evolve() #doctest: +ELLIPSIS
  ----- Begin Evolution -----
  ...
  ----- Evolution Over -----
  Best individual:
       fitness : ...
  Worst individual:
       fitness : ...
  >>> ea.visualise() #doctest: +ELLIPSIS
  ...
"""
import os

from typing import Dict, List, Callable, Any, Type

import numpy as np
from matplotlib import animation
from matplotlib import colors, cm
import matplotlib.pyplot as plt

from population import Population

Configuration = Dict[str, Any]

class EA:
  """The EA class, used to define an evolutionary process.

  Defines an evolutionary process, performs the evolution of a population and
  the visualisation of the process.
  """
  def __init__(self, config:Configuration):
    """Inits an evolutionary process given a configuration."""
    self.Population:Type[Population] = Population # pylint: disable=C0103
    self.config:Configuration = config
    self.Pop:Population = self.Population(self.config)# pylint: disable=C0103
    self.Gen:int = self.config["generations"]# pylint: disable=C0103
    self.evolution_process:List = []

    self.verbose:bool = self.config["verbose"]
    self.print_rate:int = self.config["print rate"]

    if "optimization function" in config:
      self.optimization_func:Callable = config["optimization function"]
    else:
      self.optimization_func:Callable = lambda x:x

    self.fitness:Callable = config["fitness"]

    if self.config["crossover"]:
      self.crossover_rate:float = self.config["crossover rate"]

      self.crossover:Callable = self._define_crossover()
    else:
      self.crossover:None = None

  def _define_crossover(self) -> Callable:
    """Defines the crossover function."""
    def crossover():
      return self.Pop.crossover(self.crossover_rate)
    return crossover

  def evolve(self) -> None:
    """Evolves a population using the desired configuration.

    Evolves a population of individuals with a given genotype through:

      * Random mutations
      * Crossovers (Optional)
      * Elitism (Optional)
    """
    print("----- Begin Evolution -----")
    for gen in range(self.Gen):
      if self.crossover is not None:
        self.crossover()

      self.Pop.evaluate()
      if self.verbose is True:
        if gen % self.print_rate == 0:
          print(f"{self.Pop.scores()[-1]} < pop < {self.Pop.scores()[0]}")

      self.evolution_process.append([
        [v.value() for k,v in self.Pop.pop[0].genotype.items()]+
        [self.Pop.pop[0].evaluate(self.optimization_func)],#, self.fitness)],
        [v.value() for k,v in self.Pop.pop[-1].genotype.items()]+
        [self.Pop.pop[-1].evaluate(self.optimization_func)],#, self.fitness)],
      ])
      self.Pop.select()
    print(("----- Evolution Over -----\n" +
           "Best individual:\n" +
           f"     fitness : {self.Pop.scores()[0]}\n" +
           self.Pop.pop[0].display())
    )

    print(("Worst individual:\n" +
          f"     fitness : {self.Pop.scores()[-1]}\n" +
          self.Pop.pop[-1].display())
    )

  def visualise(self, savefig:str="animation") -> None:
    """Visualise the evolutionary process in 4D.

    Makes a 4D (3d + time) visualisation of the evolutionary process by plotting
    the phenotype space. Saves the animation in a folder named
    ``Visualisations``.

    Args:
        savefig (str): Name under which the animation will be saved.
    """
    animation_directory = "Visualisations"
    if not os.path.exists(animation_directory):
      os.makedirs(animation_directory)

    axes = []
    for v in self.config["indiv"].values():
      axes.append(np.linspace(v[1][0], v[1][1], 100))

    if len(axes) > 2:
      warning_str = ("This module can only visualise in 3D at the moment."
      " Your genotype contains too many dimensions."
      " Only the first two dimensions will be plotted.")
      print(warning_str)
    x, y = axes[0], axes[1]

    x_array, y_array = np.meshgrid(x, y)
#         z_array = self.fitness(self.optimization_func(x_array, y_array))
    z_array = self.optimization_func(x_array, y_array)
    z_min, z_max = np.array(z_array).min(), np.array(z_array).max()
    z_min = min(np.array(self.evolution_process)[:,:,2].min(), z_min)
    z_max = max(np.array(self.evolution_process)[:,:,2].max(), z_max)
    if z_max-z_min > 10e2:
      if z_min<0<z_max:
        normalize = colors.SymLogNorm(
          linthresh=10e-10,
          base=np.e,
          vmin=z_min,
          vmax=z_max,
        )
      else:
        normalize = colors.LogNorm(vmin=z_min, vmax=z_max)
    else:
      normalize = colors.Normalize(vmin=z_min, vmax=z_max)

    fig, ax = plt.subplots(constrained_layout=True)
    ax = plt.axes(projection="3d")

    def animate(i):
      ax.clear()

      xmin = max(min(x)*(1-0.1), min(x) - 1)
      xmax = max(max(x)*(1+0.1), max(x) + 1)

      ymin = max(min(y)*(1-0.1), min(y) - 1)
      ymax = max(max(y)*(1+0.1), max(y) + 1)

      if z_min>=0:
        zmin = (1-0.1)*z_min
      else:
        zmin = (1+0.1)* z_min
      if z_max>=0:
        zmax = (1-0.1)*z_max
      else:
        zmax = (1+0.1)*z_max

      ax.set_xlim(xmin, xmax)
      ax.set_ylim(ymin, ymax)
      ax.set_zlim(zmin, zmax)
      # Plot gen
      ax.plot3D(
        self.evolution_process[i][0][0],
        self.evolution_process[i][0][1],
        self.evolution_process[i][0][2],
        marker="o", color="black",
      )
      ax.plot3D(
        self.evolution_process[i][1][0],
        self.evolution_process[i][1][1],
        self.evolution_process[i][1][2],
        marker="+", color="black",
      )

      ax.plot_surface(x_array, y_array, z_array, rstride=1, cstride=1,
        cmap=cm.nipy_spectral, edgecolor="none", alpha=0.7, norm=normalize)

    anim = animation.FuncAnimation(
      fig, animate,
      frames=len(self.evolution_process),
      interval=5000, repeat=True,
    )
    anim.save(
      f"{animation_directory}/{savefig}.gif",
      writer="imagemagick", fps=60,
    )
if __name__=="__main__":
  import doctest
  doctest.testmod(verbose=True, optionflags=doctest.ELLIPSIS)
