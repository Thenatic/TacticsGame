"""
The Menu class.
A data structure that navigates around an array of buttons objects.
"""


class Menu:
    def __init__(self, name, menuItems=None, prevMenu=None):
        self.name = name                #Menu Name
        self.menuItems = menuItems      #Button Array
        self.prevMenu = prevMenu        #Menu
        self.cursorIndex = 0

        if(menuItems is not None):
            self.length = len(menuItems)
        else:
            self.length = 0

    def __str__(self):
        string = self.name
        for i in range(0, self.length):
            # 1.) New Game
            string = string + '\n' + str(i) + '.) ' + str(self.menuItems[i])
            if(i==self.cursorIndex):
                string = string + ' *CURSOR*'
        return string

    def getMenuName(self):
        return self.name

    def getMenuItems(self):
        return self.menuItems

    def setMenuName(self, name):
        self.name = name

    def setMenuItems(self, menuItems):
        self.menuItems = menuItems

        if(menuItems is not None):
            self.length = len(menuItems)
        else:
            self.length = 0

    def down(self):
        if(self.cursorIndex < self.length):
            self.cursorIndex += 1

    def up(self):
        if(self.cursorIndex > 0):
            self.cursorIndex -= 1

    def select(self):
        selectButton = self.menuItems[self.cursorIndex]
        cmd = selectButton.getCommand()
        return cmd
