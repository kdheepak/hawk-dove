#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import species


class Game(object):
    """
    The Game tests the strategies of the individuals under the “rules of the game”.
    These rules produce different payoffs – in units of Fitness (the production rate of offspring).
    The contesting individuals meet in pairwise contests with others, normally in a highly mixed distribution of the population.
    The mix of strategies in the population affects the payoff results by altering the odds that any individual may meet up in contests with various strategies.
    The individuals leave the game pairwise contest with a resulting fitness determined by the contest outcome – generally represented in a Payoff Matrix."""
    def __init__(self, *args, **kwargs):
        self.rules = Rules()
        self.population = kwargs.pop('population', species.Population())
        self.period = 0

    def advance(self):
        self.period += 1
        self.compete(self.population.random_individual, self.population.random_individual)
        self.population.clean()

    def compete(self, species1, species2):
        payoff = self.rules.payoff(species1, species2)
        species1.fitness += payoff[0]
        species2.fitness += payoff[1]
        species1.fights += 1
        species2.fights += 1

class Rules(object):
    def __init__(self, *args, **kwargs):
        self.payoff_matrix = kwargs.pop('payoff_matrix', PayoffMatrix())

    def payoff(self, species1, species2):
        return self.payoff_matrix[species1.species, species2.species]

class PayoffMatrix(object):

    def __init__(self, *args, **kwargs):
        self.species1_name = kwargs.pop('species1_name', 'Hawk')
        self.species2_name = kwargs.pop('species2_name', 'Dove')
        self.V = kwargs.pop('V', 50)
        self.C = kwargs.pop('C', -10)
        self.B = kwargs.pop('B', 4)
        self.payoff = {
                        (self.species1_name, self.species1_name): (self.V, self.C*10),
                        (self.species1_name, self.species2_name): (self.V, 0),
                        (self.species2_name, self.species1_name): (0, self.V),
                        (self.species2_name, self.species2_name): (self.V+self.C, self.C),
                    }

    def __getitem__(self, keys):

        species1_name = keys[0]
        species2_name = keys[1]

        return self.payoff[(species1_name, species2_name)]

