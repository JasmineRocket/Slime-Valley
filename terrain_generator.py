# Website Citation: copied from https://learn.64bitdragon.com/articles/computer-science/procedural-generation/the-diamond-square-algorithm
from cmu_graphics import *
import random
import math

def wild_terrain_generator():
    heightmapWidth = 65

    # initialize the heightmap to 0's
    heightmap = [[0]*heightmapWidth for i in range(heightmapWidth)]

    # set the corner points to the same random value
    rand = random.randint(0, 8)
    heightmap[0][0] = rand
    heightmap[heightmapWidth - 1][0] = rand
    heightmap[0][heightmapWidth - 1] = rand
    heightmap[heightmapWidth - 1][heightmapWidth - 1] = rand

    # set the randomness bounds, higher values mean rougher landscapes
    randomness = 128
    tileWidth = heightmapWidth - 1

    # we make a pass over the heightmap
    # each time we decrease the side length by 2
    while tileWidth > 1:
        halfSide = tileWidth // 2

        # set the diamond values (the centers of each tile)
        for x in range(0, heightmapWidth - 1, tileWidth):
            for y in range(0, heightmapWidth - 1, tileWidth):
                cornerSum = heightmap[x][y] + \
                            heightmap[x + tileWidth][y] + \
                            heightmap[x][y + tileWidth] + \
                            heightmap[x + tileWidth][y + tileWidth]

                avg = cornerSum / 4
                avg += random.randint(-randomness, randomness)

                heightmap[x + halfSide][y + halfSide] = avg

        # set the square values (the midpoints of the sides)
        for x in range(0, heightmapWidth - 1, halfSide):
            for y in range((x + halfSide) % tileWidth, heightmapWidth - 1, tileWidth):
                avg = heightmap[(x - halfSide + heightmapWidth - 1) % (heightmapWidth - 1)][y] + \
                    heightmap[(x + halfSide) % (heightmapWidth - 1)][y] + \
                    heightmap[x][(y + halfSide) % (heightmapWidth - 1)] + \
                    heightmap[x][(y - halfSide + heightmapWidth - 1) % (heightmapWidth - 1)]

                avg /= 4.0
                avg += random.randint(-randomness, randomness)

                heightmap[x][y] = avg

                # because the values wrap round, the left and right edges are equal, same with top and bottom
                if x == 0:
                    heightmap[heightmapWidth - 1][y] = avg
                if y == 0:
                    heightmap[x][heightmapWidth - 1] = avg

        # reduce the randomness in each pass, making sure it never gets to 0
        randomness = max(randomness // 1.7, 1)
        tileWidth //= 2
    
    # reduce the graph into a single-integer level
    for i in range(len(heightmap)):
        for j in range(len(heightmap[0])):
                heightmap[i][j] = ((heightmap[i][j])+150)//25
    return heightmap


def optimizedTerrainGenerator():
    newMap = [[0]*15 for i in range(15)]
    heightmap = wild_terrain_generator()
    alteration = 0
    for i in range(len(heightmap)):
        for j in range(len(heightmap[0])):
            if (i >= 15) or (j >= 15):
                break
            else:
                integer = int((heightmap[i][j])//2)
                newMap[i][j] = integer
                if integer < 0:
                    alteration = integer
    if alteration != 0:
        for i in range(len(newMap)):
            for j in range(len(newMap[0])):
                newMap[i][j] -= alteration
    return newMap