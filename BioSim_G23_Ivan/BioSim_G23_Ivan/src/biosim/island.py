# -*- coding: utf-8 -*-

"""
"""

__author__ = "Peter Langdalen & Ivan Cherednikov"
__email__ = "pelangda@nmbu.no & ivch@nmbu.no"

from src.biosim.animals import Herbivore
from src.biosim.animals import Carnivore
from src.biosim.landscape import Desert
from src.biosim.landscape import Jungle
from src.biosim.landscape import Mountain
from src.biosim.landscape import Ocean
from src.biosim.landscape import Savannah
import numpy as np
from numpy import concatenate as cnc
import textwrap


class Island:
    landscapes = {'D': Desert, 'J': Jungle, 'M': Mountain, 'O': Ocean,
                  'S': Savannah}
    walkable_landscape_types = (Desert, Jungle, Savannah)
    animal_species = {'Carnivore': Carnivore, 'Herbivore': Herbivore}

    def __init__(self, island_map):
        """
        Default constructor for the Island class. Concatenation joins a
        sequence of arrays along the row.
        :param island_map: Default map for the island.
        """
        island_map = np.array([list(row.strip()) for row in
                               island_map.splitlines()])
        edges = cnc(([island_map[:-1, -1],
                      island_map[-1, :-1],
                      island_map[:-1, 0],
                      island_map[0, :-1]]))

        if not np.all(edges == 'O'):
            raise ValueError("ERROR: Not an Island map")

        # initialize the island
        self.cells = {(i + 1, j + 1): self.landscapes[island_map[i, j]]()
                      for i in range(island_map.shape[0]) for j in
                      range(island_map.shape[1])}

    def get_non_diagonal_cells(self, cell_location):
        """
        The function gets the neighbour cells which are not diagonal.
        """
        i, j = cell_location

        non_diagonal_cells = [(i + 1, j), (i - 1, j), (i, j - 1), (i, j + 1)]
        return [self.cells[neighbour_cells] for neighbour_cells in
                non_diagonal_cells if neighbour_cells in self.cells.keys()]

    def make_babies(self):
        """
        Function to make children
        """
        for location, cell in self.cells.items():
            if isinstance(cell, self.walkable_landscape_types):
                cell.make_babies()

    def feed_everyone(self):
        """
        Function to feed animals on the island
        """
        for location, cell in self.cells.items():
            if isinstance(cell, self.walkable_landscape_types):
                cell.actually_feed_the_animals()

    def initial_animals(self, animals_init):
        """
        Initial animals are added to the island.
        """
        for animal_amount in animals_init:
            herbs_carns = []
            coordinates = animal_amount['loc']
            total_amount = animal_amount['pop']

            for herb_carn in total_amount:
                species = herb_carn['species']
                age = herb_carn['age']
                weight = herb_carn['weight']
                new_herb_or_carn = self.animal_species[species](age,
                                                                weight)
                herbs_carns.append(new_herb_or_carn)

            cell = self.cells[coordinates]
            cell.add_animal(herbs_carns)

    def move_the_animals(self):
        """
        Final migration function. Using functions from landscape.py
        """
        cell_location = list(self.cells.keys())

        for location in cell_location:
            cell = self.cells[location]

            if isinstance(cell, self.walkable_landscape_types):
                non_diagonal_cells = self.get_non_diagonal_cells(location)
                cell.migrate_animals(non_diagonal_cells)

    def add_migrated_animals_island(self):
        """Adds the migrated animals to all cells on the whole island"""

        for location, cell in self.cells.items():
            if isinstance(cell, self.walkable_landscape_types):
                cell.add_migrated_animals()

    def age_lose_weight(self):
        """
        Combined function with animals aging a year and losing weight.
        The next to last part of the yearly island cycle. Put into a single
        function since these calculations are simple.
        """
        for location, cell in self.cells.items():
            if isinstance(cell, self.walkable_landscape_types):
                cell.animal_aging()
                cell.animal_weight_loss()

    def die_off(self):
        """
        The last part of the yearly cycle on the island. Animals die off.
        """
        for location, cell in self.cells.items():
            if isinstance(cell, self.walkable_landscape_types):
                cell.die_or_live()

    def yearly_cycle(self):
        """
        Do this when everything else is done. Yearly cycle on the island.
        """
        self.feed_everyone()
        self.make_babies()
        self.move_the_animals()
        self.add_migrated_animals_island()
        self.age_lose_weight()
        self.die_off()
