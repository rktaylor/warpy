"""
This is a minimalist implementation of Risk.
"""
import numpy as np
import collections
from pandas import read_csv


# Globally scoped other stuff
Tile = collections.namedtuple("Tile", ("x", "y"))


# Procedural functions
def generate_grid(map_data):
    grid = []
    for j in range(map_data.shape[0]):
        for k in range(map_data.shape[1]):
            grid.append(Tile(j,k))
    return grid


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
    I'll want to store both the csv array values as well as a grid of the tiles.
    Pre-allocating memory for this allows me to reference the data in both forms
    for methods later, and it is relatively cheap storage.
    """
    def __init__(self, csv_array):
        self.map_data = csv_array
        self.extremum = csv_array.shape
        countries = []  # for now we'll store the countries as an array
        for k in range(self.extremum[0]):
            for j in range(self.extremum[1]):  # still O(N), but N = len(csv)
                tile = Tile(k, j)
                countries.append(Country(tile=tile))


    def set_tile_adjacencies(self, country):
        """
        The graph traversal should, when it hits a -1 node, populate its neighbors
        first, then pull the pointer for those neighbors.
        :param country:
        :return:
        """
        cx, cy = country.tile.x, country.tile.y
        visited = []
        def neighbor_assign(map_data, cx, cy):
            if not self.on_screen([cx, cy]):
                return
            neighbors = [
                [cx + 1, cy],
                [cx - 1, cy],
                [cx, cy + 1],
                [cx, cy - 1]
            ]
            neighbors = [n for n in neighbors if self.on_screen(n)]
            if map_data[cx, cy] == -1:
                for n in neighbors:
                    neighbor_assign(n)



    def on_screen(self, coordinates):
        x, y = coordinates[0], coordinates[1]
        return 0 < x < self.extremum[0] and 0 < y < self.extremum[1]

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