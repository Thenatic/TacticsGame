"""
The Roster class.
Used to determine turn order in battle.
Functions similarly to a list. Takes in lists of size two [unit, initiative].
"""


class Roster:
    def __init__(self):
        self.turnOrder = []     # List of pairs, containing Unit and Initiative [Anna, 8]
        self.bench = []         # List of units that are currently KO'ed or otherwise out of combat
        self.victory = False
        self.defeat = False

    def __str__(self):
        return str(self.turnOrder)

    def append(self, item):
        self.turnOrder.append(item)

    def sort(self):
        self.turnOrder.sort(key=lambda tup: tup[1], reverse=True)

    def peek(self):
        return self.turnOrder[0]

    def pop(self):
        unit = self.turnOrder.pop(0)
        unit[1] = 0
        self.turnOrder.append(unit)
        self.sort()

    def timePassed(self):
        for i in range(0, len(self.turnOrder)):
            unit = self.turnOrder[i][0]
            unit.gainInitiative()
            self.turnOrder[i][1] = unit.initiative

        self.sort()

    def set(self, battlemap):
        units = battlemap.condensedObjects()
        for unit in units:
            self.append([unit, unit.initiative])

    def remove(self, unit):
        self.turnOrder.remove(unit)
        self.bench.append(unit)

    def update(self):
        for unit in self.turnOrder:
            if 'KO' in unit[0].status:
                self.remove(unit)

        # Check for annihilation victory
        victory = True
        for unit in self.turnOrder:
            if not unit[0].ally:
                victory = False
                break

        if victory is True:
            print 'VICTORY!!'
            self.victory = True

        # Check for defeat
        defeat = True
        for unit in self.turnOrder:
            if unit[0].ally:
                defeat = False
                break

        if defeat is True:
            print 'DEFEAT!!'
            self.defeat = True

