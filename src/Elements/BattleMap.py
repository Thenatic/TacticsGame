"""
The BattleMap class.
Represents a battlefield as a data structure.
"""

import copy

class BattleMap:
    def __init__(self):
        self.terrain = [[]]
        self.objects = [[]]
        self.cursor = [0, 0]        # [column, row]  # [x, y]
        self.dimension = [0, 0]
        self.name = 'map'

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

    def addTile(self, c):
        if(c in 'g'):
            tile = GrassTile(self.cursor)
        elif(c in 'h'):
            tile = HillTile(self.cursor)
        elif (c in 'w'):
            tile = WaterTile(self.cursor)
        else:
            raise BadMapFormatException
        self.terrain[self.cursor[1]].insert(self.cursor[0], tile)
        self.objects[self.cursor[1]].insert(self.cursor[0], 'empty')
        self.cursor[0] += 1
        self.dimension = copy.copy(self.cursor)

    def addObject(self, onTile, location):
        col = copy.copy(location[0])
        row = copy.copy(location[1])
        self.objects[row][col] = onTile

    def nextRow(self):
        self.cursor[1] += 1     # Jump down a row
        self.cursor[0] = 0      # Set column back to 0

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

    def isOccupied(self, locationTile):
        row = locationTile.location[0]
        col = locationTile.location[1]
        if('empty' == self.objects[row][col]):
            return False
        else:
            return True

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