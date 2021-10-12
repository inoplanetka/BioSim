# -*- coding: utf-8 -*-

"""
"""

__author__ = "Peter Langdalen & Ivan Cherednikov"
__email__ = "pelangda@nmbu.no & ivch@nmbu.no"

import numpy as np


class Animal:
    """
    Animal superclass
    """
    parameters = {}

    def __init__(self, age=0, weight=None):
        """
        The constructor for the Animal superclass
        """
        self.age = age
        self.weight = self.weight_birth(self.parameters) if self.age is 0 \
            else weight
        self.fitness = self.count_fitness(self.age,
                                          self.weight, self.parameters)

    @staticmethod
    def formula_fitness(plusminone, x, x_half, big_phi):
        """
        The formula for fitness. This is then used in the count_fitness, where
        the different values are put in and the fitness is calculated. For the
        "plusminus" one parameter, a +1 or -1 is put in later, in the
        count_fitness function.
        """

        result = 1.0 / (1 + np.exp(plusminone * big_phi * (x - x_half)))
        return result

    @classmethod
    def count_fitness(cls, age, weight, p):
        """
        Here, the actual fitness is calculated using the formula_fitness static
        method.
        :param weight:
        :param age:
        :param p:
        :return:
        """
        ftn = cls.formula_fitness(+1, age, p['a_half'], p['phi_age']) * \
            cls.formula_fitness(-1, weight, p['w_half'], p['phi_weight'])

        return ftn

    def aging(self):
        """
        Adds 1 to the age of animals.
        """

        self.age += 1

    def migrate_chance(self):
        """
        Gives the probability for an animal to move. Here, only the chance is
        calculated. The propensity and abundance are calculated in the land-
        scape file.
        """

        move_probability = self.parameters['mu'] * self.fitness
        the_chance = np.random.random()

        return move_probability > the_chance

    def give_birth(self, cell_animals):
        """
        Function for birth giving. Calculating if the animal will give birth.
        The actual mating is done in the landscape file where this function
        is used.
        """

        rnd = np.random.random()
        p = self.parameters
        give_birth_chance = np.min([1, p['gamma'] * self.fitness *
                                    (cell_animals - 1)])
        return self.weight >= p['zeta'] * (p['w_birth'] + p[
            'sigma_birth']) and rnd < give_birth_chance

    def eat(self, eaten_fodder):
        """
        Animal eats. Fitness is then updated, afterwards.
        """
        self.weight += self.parameters['beta'] * eaten_fodder
        self.recount_fitness()

    def death(self):
        """
        This function calculates if the animal is going to die. The actual
        deciding of the removal of the animal is done in the landscape file.
        """
        if self.fitness == 0:
            return 0
        else:
            p = self.parameters['omega'] * (1 - self.fitness)
            rand_num = np.random.choice(2, p=[p, 1 - p])
            return rand_num

    def recount_fitness(self):
        """
        Function for recounting fitness. Needed in a lot of other places,hence
        why it is a function on it's own.
        """

        self.fitness = self.count_fitness(self.weight,
                                          self.age, self.parameters)

    def weight_loss(self):
        """
        Yearly weight loss of the animals.
        """

        self.weight -= self.parameters['eta'] * self.weight
        self.recount_fitness()

    def weight_loss_birth(self, weight):
        """
        Weight loss after an animal gives birth.
        """

        self.weight -= self.parameters['xi'] * weight
        self.recount_fitness()

    @classmethod
    def weight_birth(cls, par):
        """Decides the starting weight of the animal at birth using numpy
         random distribution. "Par" is the variable dict with params
        """

        return np.random.normal(par['w_birth'], par['sigma_birth'])

    @classmethod
    def user_parameters(cls, dict_parameters=None):
        """
        Sets parameters chosen by the user. Applies to all animals.
        """
        cls.parameters.update(dict_parameters)


class Herbivore(Animal):
    """
    Herbivore subclass
    """

    def __init__(self, age=0, weight=None):
        """
        The constructor for the Herbivore subclass
        """
        super().__init__(age, weight)

    parameters = {'w_birth': 8.0, 'sigma_birth': 1.5, 'beta': 0.9, 'eta': 0.05,
                  'a_half': 40.0, 'phi_age': 0.2, 'w_half': 10.0, 'phi_weight':
                      0.1, 'mu': 0.25, 'lambda': 1.0, 'gamma': 0.2,
                  'zeta': 3.5,
                  'xi': 1.2, 'omega': 0.4, 'F': 10.0}


class Carnivore(Animal):
    """
    Carnivore subclass
    """

    def __init__(self, age=0, weight=None):
        """
        The constructor for the Carnivore subclass
        """
        super().__init__(age, weight)

    parameters = {'w_birth': 6.0, 'sigma_birth': 1.0, 'beta': 0.75, 'eta':
                  0.125, 'a_half': 60.0, 'phi_age': 0.4, 'w_half': 4.0,
                  'phi_weight': 0.4, 'mu': 0.4, 'lambda': 1.0, 'gamma': 0.8,
                  'zeta': 3.5, 'xi': 1.1, 'omega': 0.9, 'F': 50.0,
                  'DeltaPhiMax': 10.0}

    def kill_carnivore(self, fitnessherb):
        """
        Function that decides if a carnivore kills a carnivore or not while
        trying to attack it
        """

        if self.fitness <= fitnessherb:
            kill_chance = 0
        elif 0 < self.fitness - fitnessherb < self.parameters['DeltaPhiMax']:
            kill_chance = (self.fitness - fitnessherb) / \
                          self.parameters['DeltaPhiMax']
        else:
            kill_chance = 1

        n = np.random.random()
        return kill_chance > n
