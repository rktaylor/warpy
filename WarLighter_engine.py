"""
This is a minimalist implementation of Risk.
"""
import numpy as np
from pandas import read_csv


# Procedural functions


# Helper functions
def read_map(map_location):
    f = read_csv(map_location, header=None)
    return f.values


# Core classes
class Country(object):
    """
    Country
    """
    def __init__(self, tile, adjacents=None, init_armies=2):
        self.tile = tile  # in the heavy engine we can support multiple tiles
        self.adjacent_countries = adjacents
        self.owner = None
        self.continent = None
        self.armies = init_armies


class Map(object):
    """
    Composed of Countries.
    The csv document has 0s for water, and then integers for continents.
    """
    def __init__(self, csv_array):
        self.map_data = csv_array
        self.continents = None


    def populate(self):
        pass

    def changeOwner(self, country, faction):
        pass


class Faction(object):
    """
    Faction
    """
    def __init__(self, name):
        self.name = name
        self.alive = True
        self.color = None


class Game(object):
    """
    Has a map and players
    """
    def __init__(self, map, players):
        self.map = map
        self.players = players

    def resolveCombat(self):
        pass

    def calculateIncome(self):
        pass



    def nextTurn(self):
        pass