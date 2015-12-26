#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import matplotlib.pyplot as plt
import pandas as pd

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
        self.population = kwargs.pop('population')
        self.total_resources = kwargs.pop('resources', 100)
        self.exhaustion = kwargs.pop('exhaustion', 0)
        self.limited_resources = kwargs.pop('limited_resources', False)
        self.period = 0

    def advance(self):
        self.period += 1
        count = 0
        self.current_resources = self.total_resources
        while self.compete(self.population.random_individual, self.population.random_individual):
            count = count + 1

        while self.hurt(self.population.random_individual):
            pass

        self.population.clean()

    def hurt(self, species):
        if species is None:
            return False
        else:
            species.fitness -= self.exhaustion
            return True

    def compete(self, species1, species2):
        if self.current_resources < 0:
            return False
        elif species1 is None or species2 is None:
            return False
        else:
            payoff = self.rules.payoff(species1, species2)
            species1.fitness += payoff[0]
            species2.fitness += payoff[1]
            species1.fights += 1
            species2.fights += 1
            if self.limited_resources:
                self.current_resources -= payoff[0]
            return True

    def visualize(self, title='Case', special=False):
        if self.population.number_of_hawks == 0 or self.population.number_of_doves == 0:
            special=True

        if special:
            fig, axs = plt.subplots(1, 1, figsize=(16, 5))
            ax = axs
        else:
            fig, axs = plt.subplots(2, 1, figsize=(16, 10))
            ax = axs[0]

        df = pd.DataFrame(self.population.history, columns=['hawk', 'dove', '%hawk', '%dove'])

        df['hawk'].plot(label='number of hawks', legend=True, ax=ax)
        df['dove'].plot(label='number of doves', legend=True, ax=ax)
        ax.set_title(title)
        ax.set_ylim(0, ax.axis()[3]);

        if not special:
            ax = axs[1]
            df['%hawk'].plot(label='percent of hawks', legend=True, ax=ax)
            df['%dove'].plot(label='percent of doves', legend=True, ax=ax)
            ax.set_ylim(0, 1);

        return fig, axs

class Rules(object):
    def __init__(self, *args, **kwargs):
        self.payoff_matrix = kwargs.pop('payoff_matrix', PayoffMatrix())

    def payoff(self, species1, species2):
        return self.payoff_matrix[species1.species, species2.species]

class PayoffMatrix(object):

    def __init__(self, *args, **kwargs):
        self.species1_name = kwargs.pop('species1_name', 'Hawk')
        self.species2_name = kwargs.pop('species2_name', 'Dove')
        self.V = kwargs.pop('V', 2)
        self.C = kwargs.pop('C', -10)
        self.B = kwargs.pop('B', 4)
        self.payoff = {
                        (self.species1_name, self.species1_name): (-2, -2),
                        (self.species1_name, self.species2_name): (10, 0),
                        (self.species2_name, self.species1_name): (0, 10),
                        (self.species2_name, self.species2_name): (3, 3),
                    }

    def __getitem__(self, keys):

        species1_name = keys[0]
        species2_name = keys[1]
        return self.payoff[(species1_name, species2_name)]

