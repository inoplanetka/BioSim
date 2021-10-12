# -*- coding: utf-8 -*-

"""
"""

__author__ = "Peter Langdalen & Ivan Cherednikov"
__email__ = "pelangda@nmbu.no & ivch@nmbu.no"

from src.biosim.animals import Herbivore
from src.biosim.animals import Carnivore
from src.biosim.island import Island
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import pandas as pd


class BioSim:
    def __init__(
            self,
            island_map,
            ini_pop,
            seed=None,
            ymax_animals=None,
            cmax_animals=None,
            img_base=None,
            img_fmt="png",
    ):
        """
        :param island_map: Multi-line string specifying island geography
        :param ini_pop: List of dictionaries specifying initial population
        :param seed: Integer used as random number seed
        :param ymax_animals: Number specifying y-axis limit for graph showing
        animal numbers
        :param cmax_animals: Dict specifying color-code limits for animal
         densities
        :param img_base: String with beginning of file name for figures,
        including path
        :param img_fmt: String with file type for figures, e.g. 'png'

        If ymax_animals is None, the y-axis limit should be adjusted
        automatically.

        If cmax_animals is None, sensible, fixed default values should be used.
        cmax_animals is a dict mapping species names to numbers, e.g.,
           {'Herbivore': 50, 'Carnivore': 20}

        If img_base is None, no figures are written to file.
        Filenames are formed as

            '{}_{:05d}.{}'.format(img_base, img_no, img_fmt)

        where img_no are consecutive image numbers starting from 0.
        img_base should contain a path and beginning of a file name.
        """
        self.island = Island(island_map)
        self.island.initial_animals(ini_pop)
        self.years = 0
        self.final_years = None

        self.map_colors = {
            "O": mcolors.to_rgba("blue"),
            "J": mcolors.to_rgba("green"),
            "S": mcolors.to_rgba("#c99a5b"),
            "D": mcolors.to_rgba("#edc9af"),
            "M": mcolors.to_rgba("#a9a9a9"),
        }

    def set_animal_parameters(self, species, params):
        """
        Set parameters for animal species.

        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species
        """
        if species == "Herbivore":
            Herbivore.user_parameters(params)
        elif species == "Carnivore":
            Carnivore.user_parameters(params)

    def set_landscape_parameters(self, landscape, params):
        """
        Set parameters for landscape type.

        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape
        """
        pass

    def simulate(self, num_years, vis_years=1, img_years=None):
        """
        Run simulation while visualizing the result.

        :param num_years: number of years to simulate
        :param vis_years: years between visualization updates
        :param img_years: years between visualizations saved to files
        (default: vis_years)

        Image files will be numbered consecutively.
        """
        self.final_years = self.years + num_years

        while self.years < self.final_years:
            if self.num_animals() == 0:
                break

            self.island.yearly_cycle()
            self.years += 1

    def add_population(self, population):
        """
        Add a population to the island

        :param population: List of dictionaries specifying population
        """
        self.island.initial_animals(population)

    @property
    def year(self):
        """Last year simulated."""
        pass

    def num_animals(self):
        """Total number of animals on island."""
        num_animals_island = self.num_animals_per_species().values()

        return np.sum(list(num_animals_island))

    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""

        per_species_count = self.animal_distribution()

        return {'Herbivores': per_species_count['Herbivores'].sum(),
                'Carnivores': per_species_count['Carnivores'].sum()}

    def animal_distribution(self):
        """Pandas DataFrame with animal count per species for each cell on
        island. The pandas dataframe comes out with x,y, herbivores and
        carnivores columns with positions and animal amounts."""

        island = self.island.cells
        distribution = []

        for pos, cell in island.items():
            distribution.append({'x': pos[0], 'y': pos[1], 'Herbivores': len(
                cell.animals_cell[Herbivore]), 'Carnivores': len(
                cell.animals_cell[Carnivore])})

        return pd.DataFrame(distribution, columns=['x', 'y', 'Herbivores',
                                                   'Carnivores'])

    def make_movie(self):
        """Create MPEG4 movie from visualization images saved."""
        pass
