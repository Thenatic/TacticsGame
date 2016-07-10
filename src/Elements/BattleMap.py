"""
The BattleMap class.
Represents a battlefield as a data structure.
"""

import copy

class BattleMap:
    def __init__(self):
        self.terrain = [[]]
        self.objects = [[]]
        self.dimension = [0, 0]
        self.name = 'map'
        self.victory_condition = ''

        self.grassTile = None
        self.hillTile = None
        self.waterTile = None

    def __str__(self):
        return self.name

    def data(self):
        string = ''
        for i in range(0, len(self.terrain)):
            string = string + '\n' + str(self.terrain[i]).strip('[]')
        return string

    def onTileData(self):
        string = ''
        for i in range(0, len(self.objects)):
            string = string + '\n' + str(self.objects[i]).strip('[]')
        return string

    def makeTile(self, c):
        """
        Returns a reference to the appropriate tile. Uses the Flyweight pattern to reduce memory usage.
        :param c: Specifies the type of tile to return.
        :return: The appropriate tile, given c.
        """
        if(c in 'g'):
            if(self.grassTile is None):
                self.grassTile = GrassTile()
            tile = self.grassTile
        elif(c in 'h'):
            if (self.hillTile is None):
                self.hillTile = HillTile()
            tile = self.hillTile
        elif (c in 'w'):
            if (self.waterTile is None):
                self.waterTile = WaterTile()
            tile = self.waterTile
        else:
            raise BadMapFormatException

        return tile

    def addObject(self, onTile, location):
        col = copy.copy(location[0])
        row = copy.copy(location[1])
        self.objects[row][col] = onTile


    def replaceObjects(self, originals, replacements):
        """
        Goes through the map's objects and replaces objects in originals with the corresponding object in replacements.
        :param originals:
        :param replacements:
        :return:
        """
        # "item" is (row, col, character)
        map_object_generator = nested_list_traversal(self.objects)
        while True:
            try:
                item = map_object_generator.next()
                if str(item[2]) in originals:
                    index = originals.index(item[2])
                    replacement = replacements.pop(index)
                    originals.remove(item[2])
                    self.objects[item[0]][item[1]] = replacement
                    replacement.setLocation( (item[0], item[1]) )
            except StopIteration:
                return 0
            except:
                raise

    def condensedObjects(self):
        map_object_generator = nested_list_traversal(self.objects)
        condensed_objects_list = []
        while True:
            try:
                item = map_object_generator.next()
                if 'empty' not in item:
                    condensed_objects_list.append(item[2])
            except StopIteration:
                return condensed_objects_list
            except:
                raise

    def setMap(self, nestedList):
        self.terrain = nestedList
        self.objects = copy.deepcopy(nestedList)

    def moveObject(self, onTile):

        # Remove unit from object grid
        for i in range(0, self.dimension[1]):
            for j in range(0, self.dimension[0]):
                if(onTile == self.objects[i][j]):
                    self.objects[i][j] = 'empty'

        # Place unit in new location on object grid
        newLocation = onTile.location
        newCol = newLocation[0]
        newRow = newLocation[1]
        self.objects[newRow][newCol] = onTile       #Remember, object array is (y, x)

    def getObject(self, location):
        col = location[0]
        row = location[1]
        # row = locationTile.location[0]
        # col = locationTile.location[1]
        return self.objects[row][col]

    def isOccupied(self, locationTile):
        col = locationTile.location[0]
        row = locationTile.location[1]
        if('empty' == self.objects[row][col]):
            return False
        else:
            return True

    def setVictory(self, boolean):
        self.victory_condition = boolean


class Tile:
    """
    The Tile class. Uses the Flyweight design pattern to minimize memory usage.

    At any given time, there exists only one of a particular tile type. All tiles of that type are just references to
    the single tile. This means that all grass tiles on a map are simply references to a single GrassTile object.
    """
    def __str__(self):
        return 'Tile'

    def __repr__(self):
        return self.__str__()

class GrassTile(Tile):
    def __init__(self):
        self.cross = 'normal'
        self.slow = 0
        self.defense = 0

    def __str__(self):
        return 'g'

class HillTile(Tile):
    def __init__(self):
        self.cross = 'normal'
        self.slow = 1
        self.defense = 5

    def __str__(self):
        return 'h'

class WaterTile(Tile):
    def __init__(self):
        self.cross = 'water'
        self.slow = 0
        self.defense = 0

    def __str__(self):
        return 'w'

class SolidTile(Tile):
    def __init__(self):
        self.cross = 'wall'
        self.slow = 0
        self.defense = 0

    def __str__(self):
        return 's'

class BadMapFormatException(Exception):
    def __str__(self):
        return 'BadMapFormatException'


def nested_list_traversal(list):
    """
    A python generator for nested lists.
    :param list: A nested list.
    :return: The row, column, and element occupying that spot in the list. Progresses forward each call.
    """
    try:
        for row in range(0, len(list)):
            for col in range(0, len(list[row])):
                yield (row, col, list[row][col])
    except TypeError:
        yield list