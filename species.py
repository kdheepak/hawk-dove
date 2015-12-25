#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""
Evolutionary game theory

The strategy of the Hawk (a fighter strategy) is to first display aggression, then escalate into a fight until he either wins or is injured. 
The strategy of the Dove (fight avoider) is to first display aggression but if faced with major escalation by an opponent to run for safety. 

"""
from __future__ import absolute_import, division, print_function
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import random

class Bird(object):
    def __init__(self, *args, **kwargs):
        if self.strategy is None:
            self.strategy = kwargs.pop('strategy', None)
        self.fitness = kwargs.pop('fitness', 50)
        self.fights = kwargs.pop('fights', 0)
        self.species = kwargs.pop('species', self.__class__.__name__)

    def __str__(self):
        return("""{}\t{}\t{}""".format(self.species, self.fitness, self.fights))

class Hawk(Bird):
    def __init__(self, *args, **kwargs):
        self.strategy = kwargs.pop('strategy', 'Aggressive')
        super().__init__(*args, **kwargs)

class Dove(Bird):
    def __init__(self, *args, **kwargs):
        self.strategy = kwargs.pop('strategy', 'Passive')
        super().__init__(*args, **kwargs)

class Population(object):
    def __init__(self, *args, **kwargs):
        """
        Attribute
        ---------
            number_of_hawks (int)
            number_of_doves (int)
        """
        self.individuals = [Hawk() for _ in range(0, kwargs.pop('number_of_hawks', 10))] + [Dove() for _ in range(0, kwargs.pop('number_of_doves', 10))]
        self.THRESHOLD = kwargs.pop('THRESHOLD', 10000)
        self.total = len(self.individuals)
        self.history = []

    def describe(self):
        total = self.number_of_hawks + self.number_of_doves
        print("Number of hawks = {}".format(self.number_of_hawks))
        print("Number of doves = {}".format(self.number_of_doves))
        print("Percent of hawks = {}".format(self.number_of_hawks/total*100))
        print("Percent of doves = {}".format(self.number_of_doves/total*100))

    @property
    def random_individual(self):
        return random.choice(self.individuals)

    def clean(self):
        self.individuals = [bird for bird in self.individuals if bird.fitness >= 0]

        self.number_of_hawks = [bird.species for bird in self.individuals].count('Hawk')
        self.number_of_doves = [bird.species for bird in self.individuals].count('Dove')

        self.history.append([self.number_of_hawks, self.number_of_doves])
        self.breed()

    def breed(self):
        breed_pool = []
        for individual in self.individuals:
            if individual.fitness > self.THRESHOLD:
                individual.fitness = individual.fitness / 2
                breed_pool.append((individual.species, individual.fitness))

        for baby, fitness in breed_pool:
            if baby == 'Hawk':
                self.individuals.append(Hawk(fitness=fitness))
            if baby == 'Dove':
                self.individuals.append(Dove(fitness=fitness))
