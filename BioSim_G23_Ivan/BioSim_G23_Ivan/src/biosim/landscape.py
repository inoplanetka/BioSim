# -*- coding: utf-8 -*-

"""
"""

__author__ = "Peter Langdalen & Ivan Cherednikov"
__email__ = "pelangda@nmbu.no & ivch@nmbu.no"

import numpy as np
from numpy import cumsum as cs
from src.biosim.animals import Herbivore
from src.biosim.animals import Carnivore
import operator


class Square:
    """
    Square superclass, a single cell on the map. Since it is a superclass,
    all types of cells are subclassed from it. This includes uninhabitable and
    landscapes and cells you can not migrate to, such as Mountain or Ocean.
    """
    parameters = {}

    def __init__(self):
        """
        The constructor for the Square superclass
        """

        self.animals_cell = {Herbivore: [], Carnivore: []}
        self.migrants = {Herbivore: [], Carnivore: []}
        self.fodder = 0

    def grow_food(self):
        """
        This is overridden in the subclasses so i just pass it here
        """
        pass

    def add_animal(self, list_of_animals):
        """
        The function adds animals of a given amount to a cell.
        """

        for animal in list_of_animals:
            if type(animal) in self.animals_cell:
                self.animals_cell[type(animal)].append(animal)
            else:
                raise TypeError("wrong species")

    def remove_animal(self, animal):

        list_type_animal = self.animals_cell[type(animal)]

        if type(animal) not in self.animals_cell or animal not in \
                list_type_animal:
            raise ValueError("can't retrieve animal")

        list_type_animal.remove(animal)

    def make_babies(self):
        """
        Function for the actual making of children.
        """
        for animals in self.animals_cell.values():
            amount_of_animals = len(animals)
            born_babies = []
            for animal in animals:
                if animal.give_birth(amount_of_animals):
                    baby = type(animal)()
                    animal.weight_loss_birth(baby.weight)
                    born_babies.append(baby)
            animals.extend(born_babies)

    def animal_aging(self):
        """
        Ages animals in a cell, one year
        """
        for animals in self.animals_cell.values():
            for animal in animals:
                animal.aging()

    def animal_weight_loss(self):
        """
        Yearly weight loss for animals in a cell. Both species.
        """
        for animals in self.animals_cell.values():
            for animal in animals:
                animal.weight_loss()

    def die_or_live(self):
        """
        Decides if animal in a cell dies or lives. items() method the same
         as viewitems() method, returns view object that shows a list.
        """
        for species, animals in self.animals_cell.items():
            still_living = []
            for animal in animals:
                if not animal.death():
                    still_living.append(animal)
            self.animals_cell[species] = still_living

    def herbivores_feed(self):
        """
        Function to feed herbivores. The operator module is used to fetch
        attr from fitness.
        """
        herbivores = sorted(self.animals_cell[Herbivore],
                            key=operator.attrgetter('fitness'), reverse=True)

        for herbivore in herbivores:
            if herbivore.parameters['F'] <= self.fodder:
                herbivore.eat(herbivore.parameters['F'])
                self.fodder -= herbivore.parameters['F']
            elif 0 < self.fodder < herbivore.parameters['F']:
                herbivore.eat(self.fodder)
                self.fodder = 0

    def carnivores_feed(self):
        """
        Function to feed carnivores. Operator module used again like in the
        herbivore_feed function. However, a variable is not used here and in-
        stead, it is sorted and used directly. A variable for the amount eaten
        is used, which is added to depending on the if statement. If the
        herbivore isn't killed and eaten successfully, it is added to the list
        with survived animals, "kill_failed"
        """
        self.animals_cell[Herbivore].sort(key=operator.attrgetter('fitness'))

        self.animals_cell[Carnivore].sort(key=operator.attrgetter('fitness'),
                                          reverse=True)

        for carnivore in self.animals_cell[Carnivore]:
            kill_failed = []
            eaten = 0
            for k, herb in enumerate(self.animals_cell[Herbivore]):
                if carnivore.parameters['F'] <= eaten:
                    kill_failed.extend(self.animals_cell[Herbivore][k:])
                    break
                elif carnivore.kill_carnivore(herb.fitness):
                    left_to_eat = carnivore.parameters['F'] - eaten
                    if left_to_eat >= herb.weight:
                        eaten += herb.weight
                    elif left_to_eat < herb.weight:
                        eaten += left_to_eat
                else:
                    kill_failed.append(herb)
            carnivore.eat(eaten)
            self.animals_cell[Herbivore] = kill_failed

    def actually_feed_the_animals(self):
        """
        Here the animals in a cell are actually fed. Both herbivores
        and carnivores.
        """
        self.grow_food()
        self.herbivores_feed()
        self.carnivores_feed()

    @classmethod
    def user_parameters(cls, set_parameters=None):
        """
        Sets parameters chosen by the user. Applies to all cells.
        """
        cls.parameters.update(set_parameters)

    @staticmethod
    def abundance(animal_amount, species_hunger, relevant):
        """
        Calculates the relative abundance of fodder in a cell as it is
        given in the task. "Animal_amount" is the amount of same specied
        animals, "species_hunger" is the hunger of the species and "relevant"
        is the amount of relevant fodder in the cell.
        Returns relative abundance of fodder in a cell.
        Done as a static method just like formula_fitness in animals.py
        """
        return relevant / ((animal_amount + 1) * species_hunger)

    def propensity_migration(self, species_):
        """
        Function that calculates the propensity for migrating from one cell
        to another. Does not apply for neighbouring cells that are diagonal.
        Propensity to move to impassable cells is 0.
        """

        animal_amount = len(self.animals_cell[species_]) + len(
            self.migrants[species_])

        relevant = self.fodder if species_ == Herbivore else np.sum(
            herbivore.weight for herbivore in self.animals_cell[Herbivore] +
            self.migrants[Herbivore])

        abundance_ = self.abundance(animal_amount, species_.parameters['F'],
                                    relevant)

        return np.exp(species_.parameters['lambda'] * abundance_)

    def migrate_animals(self, nearby):
        """
        Migrates the animal with the help of calculation of propensity,
        which exists the loop for non walkable terrain like Mountain and Ocean.
        Also using cumulative sum of the migration chance to each square.
        :param nearby:
        :return:
        """
        for species, cell_population in self.animals_cell.items():
            if len(cell_population) > 0:
                propensities = [neighbour_cell.propensity_migration(species)
                                for neighbour_cell in nearby]
                if sum(propensities) == 0:
                    self.migrants[species] = self.animals_cell[species].copy()
                    break
                probabilities = np.array([k / np.sum(propensities) for k in
                                          propensities])
                sum_migration_cells = np.cumsum(probabilities)
                for animal in cell_population:
                    if animal.migrate_chance():
                        c = 0
                        random_number = np.random.random()
                        while sum_migration_cells[c] <= random_number:
                            c += 1
                        nearby[c].migrants[species].append(animal)
                    else:
                        self.migrants[species].append(animal)

    def add_migrated_animals(self):
        """
        The function adds all the migrated animals to the cell they're moving
        to. Does not remove the other animals already in the cell.
        """
        for species in self.animals_cell:
            migrated_herb_carn = self.migrants[species].copy()
            self.animals_cell[species] = migrated_herb_carn
            self.migrants[species] = []

    def cell_reconstruct(self):
        """
        Function that resets the cell to default.
        """
        self.animals_cell = {Carnivore: [], Herbivore: []}


class Jungle(Square):
    """
    Jungle subclass. Fodder in the Jungle is set to the max value 'f_max' every
    annual cycle, so it is expected that a Jungle cell is where you will find
    most of the animals.
    """
    parameters = {'f_max': 800}

    def __init__(self):
        super().__init__()
        self.fodder = self.parameters['f_max']

    def grow_food(self):
        """
        Sets food amount for this landscape type.
        For Jungle, it is just f_max, max amount of fodder.
        """

        self.fodder = self.parameters['f_max']


class Savannah(Square):
    """
    Savannah subclass. Fodder in the Savannah is initially set to the max value
    'f_max', but in contrast to the Jungle, a Savannah does not just refill
    it's fodder supply every year. The amount of food is instead calculated
    using a formula, using an 'alpha' constant and the amount of fodder left
    in the Savannah cell. Savannah cells can not be destroyed by overgrazing.
    """
    parameters = {'f_max': 300.0, 'alpha': 0.3}

    def __init__(self):
        """
        The constructor for the Desert subclass
        """
        super().__init__()
        self.fodder = self.parameters['f_max']

    def grow_food(self):
        """
        Sets food amount for this landscape type.
        For Savannah, it is a set formula, where the new growth depends on
        the amount of food left.
        """
        self.fodder += self.parameters['alpha'] * (self.parameters['f_max'] -
                                                   self.fodder)


class Desert(Square):
    """
    Desert subclass. Deserts have no fodder for the herbivores, however
    carnivores can still hunt herbivores in here.
    """

    def __init__(self):
        """
        The constructor for the Desert subclass
        """
        super().__init__()


class Ocean(Square):
    """
    Ocean subclass. Animals can not walk in the Ocean (neither can they swim),
    hence why the propensity to migrate to it is 0. Since the simulation is of
    an island, the map is to be surrounded by cells with the Ocean class in it.
    If it is not, it is not as island.
    """

    def __init__(self):
        """
        The constructor for the Ocean subclass
        """
        super().__init__()

    def propensity_migration(self, species_):
        if species_:
            return 0.0


class Mountain(Square):
    """
    Mountain subclass. Mountains can not be walked on by any of the species,
    hence why the propensity to migrate is 0. There is no way to migrate to an
    island and if a mountain is one of the squares in the migration chance
    calculation process, it is taken into consideration in the formula.
    """

    def __init__(self):
        """
        The constructor for the Mountain subclass
        """
        super().__init__()

    def propensity_migration(self, species_):
        if species_:
            return 0.0
