"""
This package contains all map generation, qc, etc. utilities.
"""


import pandas as pd
import numpy as np

COLORS = {
    "land": "\x1b[7;32;47m",
    "seas": "\x1b[7;34;47m",
    "pass": "\x1b[7;35;47m",
    "null": "\x1b[7;30;47m",
    "city": "\x1b[7;33;47m",
    "TERM": "\x1b[0m",
}


def print_map(map_array):
    for j in map_array:
        print_string = ""
        for k in j:
            if k > 0 and k != 9:
                color = COLORS["land"]
            elif k == 0:
                color = COLORS["seas"]
            elif k == -1:
                color = COLORS["pass"]
            else:
                color = COLORS["null"]
            if k != -1 and k != 9:
                print_string += color + " {} ".format(int(k)) + COLORS["TERM"]
            elif k == 9:
                print_string += COLORS["city"] + " C " + COLORS["TERM"]
            else:
                print_string += color + " B " + COLORS["TERM"]
        print(print_string)


def printmap(map_array):
    for j in map_array:
        string = ""
        for k in j:
            if k > 0:
                color = COLORS["land"]
            elif k == 0:
                color = COLORS["seas"]
            elif k == -1:
                color = COLORS["pass"]
            else:
                color = COLORS["null"]
            if k != -1:
                string += color + " {0:0=2d} ".format(k) + COLORS["TERM"]
            else:
                string += color + " -- " + COLORS["TERM"]
        print(string)
    return


def load_csv(filesystem_location):
    d = pd.read_csv(filesystem_location, header=None)
    return d.values


class DesignConstraint(Exception):
    pass


def generate_map_basic(x, y, ocean=0.3, continents=3, cities=0):
    """
    :return:
    """
    #if continents > (x*y)/(50*ocean) or continents > (1-ocean)*10:
    #    raise DesignConstraint
    if continents > 8:  # Just say you can't have more than 7 continents.
        raise DesignConstraint
    # instantiate the output array
    output = np.array([[0 for m in range(x)] for n in range(y)])  # None or 0?
    # compute available tile resources
    area = int(x*y)
    land = int(area * (1.0-ocean))
    print(land)
    siz = np.random.randint(10, 100-10*continents, continents)
    pct = np.array(siz) / float(sum(siz))
    cot = [int(continent*land) for continent in pct]
    print("pct {} | cot {}".format(str(pct), str(cot)))
    cot[0] += land - sum(cot)  # add any leftovers from our method back onto a continent
    # begin partition
    continent_centers, landmass = [], []
    still_partitioning = True
    while still_partitioning:
        cx, cy = np.random.choice(range(x)), np.random.choice(range(y))
        if satisfies_centering_conditions(cx, cy, continent_centers):
            continent_centers.append([cx, cy])
        if len(continent_centers) == continents:
            still_partitioning = False
    for ct, continent in enumerate(continent_centers):
        print("ct = {}, cont = {}, cot[ct] = {}".format(ct, continent, cot[ct]))
        print("output.shape {}".format(output.shape))
        l = dummy_fill(output, continent[1], continent[0], ct+1, cot[ct])  # flipping 1<-->0
        landmass.append(l)  # I need this variable to determine paths / add bridges
    if cities:
        cities_list = []
        while len(cities_list) < cities:
            cx, cy = np.random.choice(range(output.shape[0])), \
                     np.random.choice(range(output.shape[1]))
            if output[cx, cy] != 0 and output[cx, cy] != -1:
                output[cx, cy] = '9'
                cities_list.append([cx, cy])
    return output, landmass


# This will RANDOMLY break if cx != cy. TODO fix
def dummy_fill(map_array, cx, cy, cn, num_tiles, timeout=1000):
    """
    This time I have a runner tab of what cells are part of the continent,
    and populate while len(cells) < num_tiles.
    :return:
    """
    ms, continent = map_array.shape, []
    map_array[cx, cy] = cn
    continent.append([cx, cy])
    timeout_ct = 0
    while len(continent) != num_tiles and timeout_ct < timeout:
        timeout_ct += 1
        [dx, dy] = continent[np.random.choice(len(continent))]
        neighboring = [[dx, dy + 1], [dx, dy - 1], [dx + 1, dy], [dx - 1, dy]]
        bordercells = [n for n in neighboring if 0 < n[0] < ms[0] and 0 < n[1] < ms[1]]
        # I'm going to explain this now for future me.
        # np.random.choice is a shit about selecting items from a list if those
        # items are also lists. So I'm just choosing from a range defined by the length
        # of the thing I'm really chosing from, then indexing with that. It's gross.
        [tile_x, tile_y] = bordercells[np.random.choice(len(bordercells))]
        if [tile_x, tile_y] not in continent:
            map_array[tile_x, tile_y] = cn
            continent.append([tile_x, tile_y])
    return continent


def closest_points(coordinate_cloud_1, coordinate_cloud_2):
    """
    This is fun. Given two clouds of coordinates (for continents),
    return *A* pair of coordinates in each cloud such that the distance
    between those points is smallest out of the set of all distances between all pairs.
    That is, What two points define a shortest path?
    The brute force technique is O(N^2).
    I can make it memory okay but just storing variables best_distance_so_far
    and best_coordinates_so_far, and returning immediately if that value is ever 1.
    """
    pass


def build_bridge(map_array, point_a, point_b):
    make_these_bridges = cells_between(point_a, point_b)
    for cell in make_these_bridges:
        map_array[cell[0], cell[1]] = -1


def cells_between(point_a, point_b):
    output, vertex = [], [point_a[0], point_b[1]]
    displacement = np.array(point_a) - np.array(point_b)
    #output.append(vertex)
    x_i, y_i = min(point_a[0], point_b[0]), min(point_a[1], point_b[1])
    x_f, y_f = max(point_a[0], point_b[0]), max(point_a[1], point_b[1])
    for x in range(abs(displacement[0])):
        output.append([x_i + x, y_i])
    for y in range(abs(displacement[1])):
        output.append([x_f, y_i + y])
    if point_a in output:
        output.remove(point_a)
    if point_b in output:
        output.remove(point_b)
    return output





def satisfies_centering_conditions(x, y, o):
    # for some reason, [0,0] breaks numpy.choice... so. excluding that here.
    u, d, r, l = [x, y+1], [x, y-1], [x+1, y], [x-1, y]
    out = u not in o and d not in o and r not in o and \
          l not in o and [x, y] not in o and [x, y] != [0, 0]
    return out

# ---------------------------------------------------------------------------------------
# NOTES:
#
# http://www.geeksforgeeks.org/flood-fill-algorithm-implement-fill-paint/
# // A recursive function to replace previous color 'prevC' at  '(x, y)'
# // and all surrounding pixels of (x, y) with new color 'newC' and
# floodFil(screen[M][N], x, y, prevC, newC)
# 1) If x or y is outside the screen, then return.
# 2) If color of screen[x][y] is not same as prevC, then return
# 3) Recur for north, south, east and west.
#     floodFillUtil(screen, x+1, y, prevC, newC);
#     floodFillUtil(screen, x-1, y, prevC, newC);
#     floodFillUtil(screen, x, y+1, prevC, newC);
#     floodFillUtil(screen, x, y-1, prevC, newC);
#
# So we could do something similar, FindEdge(map, cx, cy, cn) for a map array `map`
# and a continent with center `[cx, cy]` numbered `cn`.
# findEdge(map, cx, cy, cn):
#       (1) if [cx, cy] not in map: return
#       (2) if map[cx, cy] != cn: return
#       (3) if ANY neighbor of [cx, cy] is 0 (ocean): return [cx, cy]
#       (4) edges = []
#       (5) edges.append(findEdge(map, cx+1, cy, cn))
#
# My function call for populating neighbors will have to be pretty much the same,
# only different operation at the end. In this case it will be
# "flip a weighted quarter (.8 true) on whether or not to convert this cell to cn,
# and if you do, decrement the remaining land to allocate for this given cn."
# I will need some logic for handling the case of "there's leftovers!"
#
#
#
# Also, For linking across channels, should probably do a list comprehension.
# and if self.neighbor = -1, self.neighbor = self.neighbor.neighbors. Recursively?
