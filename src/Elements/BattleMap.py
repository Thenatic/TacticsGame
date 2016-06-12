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

    def makeTile(self, c, location):
        if(c in 'g'):
            tile = GrassTile(location)
        elif(c in 'h'):
            tile = HillTile(location)
        elif (c in 'w'):
            tile = WaterTile(location)
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
        for i in range(0, self.dimension[1]):
            for j in range(0, self.dimension[0]):
                if(onTile == self.objects[i][j]):
                    self.objects[i][j] = 'empty'

        newLocation = onTile.location
        newCol = newLocation[0]
        newRow = newLocation[1]
        self.objects[newCol][newRow] = onTile

    def getObject(self, locationTile):
        row = locationTile.location[0]
        col = locationTile.location[1]
        return self.objects[row][col]

    def isOccupied(self, locationTile):
        row = locationTile.location[0]
        col = locationTile.location[1]
        if('empty' == self.objects[row][col]):
            return False
        else:
            return True

    def setVictory(self, boolean):
        self.victory_condition = boolean


class Tile:
    def __init__(self, location):
        self.location = copy.copy(location)

    def __str__(self):
        return 'Tile'

    def __repr__(self):
        return self.__str__()

class GrassTile(Tile):
    def __init__(self, location):
        Tile.__init__(self, location)
        self.cross = 'normal'
        self.slow = 0
        self.defense = 0

    def __str__(self):
        return 'g'

class HillTile(Tile):
    def __init__(self, location):
        Tile.__init__(self, location)
        self.cross = 'normal'
        self.slow = 1
        self.defense = 5

    def __str__(self):
        return 'h'

class WaterTile(Tile):
    def __init__(self, location):
        Tile.__init__(self, location)
        self.cross = 'water'
        self.slow = 0
        self.defense = 0

    def __str__(self):
        return 'w'

class SolidTile(Tile):
    def __init__(self, location):
        Tile.__init__(self, location)
        self.cross = 'wall'
        self.slow = 0
        self.defense = 0

    def __str__(self):
        return 's'

class BadMapFormatException(Exception):
    def __str__(self):
        return 'BadMapFormatException'


def nested_list_traversal(list):
    try:
        for i in range(0, len(list)):
            for j in range(0, len(list[i])):
                yield (i, j, list[i][j])
    except TypeError:
        yield list