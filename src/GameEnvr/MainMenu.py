"""
The Main Menu environment.
Currently used for testing menu structure.
"""



import os
# import os, pygame, sys
# from pygame.locals import*

os.chdir('/home/roy/PycharmProjects/TacticsGame/src')

from src.Elements.Menu import*
from src.Elements.Button import*
from src.Elements.Command import*
from src.Elements.save_load import*

# Initialize Menus #####################################
mainMenu = ButtonMenu('Main Menu')
unitsMenu = ButtonMenu('Units', prevMenu=mainMenu)
spiritsMenu = ButtonMenu('Spirits', prevMenu=mainMenu)
optionsMenu = ButtonMenu('Options', prevMenu=mainMenu)


    # Build Main Menu
game = newFile()
menuArray = [unitsMenu, spiritsMenu, optionsMenu]

def ButtonMenuBuilder(items, menu, cmdType=''):
    units = []
    for i in range(0, len(items)):
        unit = items[i].name
        if(cmdType == 'menu'):
            c = ChangeMenuCommand(unit, items[i])
        else:
            c = PrintCommand(UnitMenu(unit, items[i]))
        b = Button(unit, c)
        units.append(b)
    menu.setMenuItems(units)


ButtonMenuBuilder(menuArray, mainMenu, 'menu')
ButtonMenuBuilder(game.characters, unitsMenu)
ButtonMenuBuilder(game.spirits, spiritsMenu)


# Main Loop ##############################################
# This is the way a user interfaces with the data structures.
# It's also going to be the first to go with the GUI upgrade.

currMenu = mainMenu

while(True):
    print '\n'
    print currMenu
    user = raw_input("UP[A], DOWN[S], SELECT[Z], BACK[X], EXIT[Q]\n")
    user = str(user).lower()

    if(user == 'a'):
        currMenu.up()

    elif(user == 's'):
        currMenu.down()

    elif(user == 'z'):
        newMenu = currMenu.select().execute()
        if(newMenu is not None):
            currMenu = newMenu

    elif(user == 'x'):
        newMenu = currMenu.back().execute()
        if (newMenu is not None):
            currMenu = newMenu

    elif(user == 'q'):
        exit(0)


# pygame.init()
# currMenu = mainMenu
#
# while(True):
#     for event in pygame.event.get():
#         if event.type == QUIT:
#             pygame.quit()
#             sys.exit()
#
#         elif event.type == KEYDOWN:
#             # Up Arrow
#             if event.key == K_UP:
#                 currMenu.up()
#
#             # Down Arrow
#             elif event.key == K_DOWN:
#                 currMenu.down();
#
#             # Accept Button (z)
#             elif event.key == K_z:
#                 currMenu.select().execute()
#
#             # Back Button (x)
#             elif event.key == K_x:
#                 currMenu.back().execute()
#
#         print currMenu
