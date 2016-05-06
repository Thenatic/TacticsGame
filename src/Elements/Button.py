"""
The Button class.
Contains a command object.
"""


class Button:
    def __init__(self, name, command=None):
        self.name = name
        self.command = command

    def __str__(self):
        return self.name

    def getName(self):
        return self.name

    def getCommand(self):
        return self.command

    def setName(self, name):
        self.name = name

    def setCommand(self, command):
        self.command = command
