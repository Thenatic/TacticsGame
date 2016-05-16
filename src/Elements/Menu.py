"""
The Menu class.
A data structure that navigates around an array of buttons objects.
"""

from src.Elements.Command import*

class Menu:
    """
    Generic Menu class, used mainly as a base for other menu classes.
    """
    def __init__(self, name, prevMenu=None):
        self.name = name                #Menu Name
        self.prevMenu = prevMenu        #Previous Menu
        self.emptyCommand = NullCommand()

    def __str__(self):
        return self.name

    def getMenuName(self):
        return self.name

    def setMenuName(self, name):
        self.name = name

    def setPrevMenu(self, prevMenu):
        self.prevMenu = prevMenu

    def select(self):
        return self.emptyCommand

    def back(self):
        if(self.prevMenu is None):
            return self.emptyCommand
        else:
            cmd = ChangeMenuCommand(self.prevMenu.name, self.prevMenu)
            return cmd


class ButtonMenu(Menu):
    """
    The ButtonMenu class.
    A menu based around buttons, each of which contains a Command object.
    The menu allows users to navigate and access the buttons and their commands.
    """
    def __init__(self, name, menuItems=None, prevMenu=None):
        Menu.__init__(self, name)
        self.menuItems = menuItems  # Button Array
        self.prevMenu = prevMenu  # Menu
        self.cursorIndex = 0

        if (menuItems is not None):
            self.length = len(menuItems)-1
        else:
            self.length = 0

    def __str__(self):
        return self.name

    def data(self):
        string = self.name
        for i in range(0, len(self.menuItems)):
            # 1.) New Game
            string = string + '\n' + str(i+1) + '.) ' + str(self.menuItems[i])
            if (i == self.cursorIndex):
                string = string + ' *CURSOR*'
        return string

    def getMenuItems(self):
        return self.menuItems

    def setMenuItems(self, menuItems):
        self.menuItems = menuItems

        if (menuItems is not None):
            self.length = len(menuItems) - 1
        else:
            self.length = 0

    def down(self):
        if (self.cursorIndex < self.length):
            self.cursorIndex += 1

    def up(self):
        if (self.cursorIndex > 0):
            self.cursorIndex -= 1

    def select(self):
        selectButton = self.menuItems[self.cursorIndex]
        cmd = selectButton.getCommand()
        return cmd

class UnitMenu(Menu):
    """
    The UnitMenu class.
    In-progress.
    """
    def __init__(self, name, unit):
        Menu.__init__(self, name)
        self.unit = unit

    def __str__(self):
        return self.unit.__str__()

