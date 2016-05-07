"""
The Roster class.
Functions similarly to a list. Takes in lists of size two [unit, initiative].
"""


class Roster:
    def __init__(self):
        self.list = []

    def __str__(self):
        return str(self.list)

    def append(self, item):
        self.list.append(item)

    def sort(self):
        self.list.sort(key=lambda tup: tup[1], reverse=True)

    def peek(self):
        return self.list[0]

    def pop(self):
        unit = self.list.pop(0)
        unit[1] = 0
        self.list.append(unit)
        self.sort()
