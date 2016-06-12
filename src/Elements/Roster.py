"""
The Roster class.
Used to determine turn order in battle.
Functions similarly to a list. Takes in lists of size two [unit, initiative].
"""


class Roster:
    def __init__(self):
        self.turnOrder = []     # List of pairs, containing Unit and Initiative [Anna, 8]

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
