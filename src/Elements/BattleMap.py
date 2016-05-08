"""
The Map class.
Represents a battlefield as a data structure.
"""

class BattleMap:
    def __init__(self):
        self.map = [[]]
        self.row = 0
        self.col = 0
        self.name = 'map'

    def __str__(self):
        return self.name

    def data(self):
        string = ''
        for i in range(0, len(self.map)):
            string = string + '\n' + str(self.map[i]).strip('[]')
        return string

    def addTile(self, c):
        if(c in 'g'):
            tile = GrassTile((self.col, self.row))
        elif(c in 'h'):
            tile = HillTile((self.col, self.row))
        elif (c in 'w'):
            tile = WaterTile((self.col, self.row))
        else:
            raise BadMapFormatException
        self.map[self.col].insert(self.row, tile)
        self.col += 1

    def nextRow(self):
        self.row += 1
        self.col = 0

    def setMap(self, nestedList):
        self.map = nestedList

class Tile:
    def __init__(self, location):
        self.location = location

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

class BadMapFormatException(Exception):
    def __str__(self):
        return 'BadMapFormatException'