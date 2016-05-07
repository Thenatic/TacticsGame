"""
The Battle environment.
Currently used for testing character and command classes.
"""


import os
import operator
# import os, pygame, sys
# from pygame.locals import*

os.chdir('/home/roy/PycharmProjects/TacticsGame/src')

from src.Elements.Menu import*
from src.Elements.Button import*
from src.Elements.Command import*
from src.Elements.Roster import*
from src.Elements.save_load import*

# Initialize Units #####################################
game = newFile()
bads = tempFile()   #Replace later with encounter-specific stuff
roster = Roster()

# Pull friendly units from save
for i in range(0, len(game.characters)):
    unit = game.characters[i]
    unit = BattleCharacter(unit)
    rosterUnit = [unit, unit.initiative]
    roster.append(rosterUnit)


# Pull unfriendly units from map
for i in range(0, len(bads.characters)):
    unit = bads.characters[i]
    unit = BattleCharacter(unit)
    rosterUnit = [unit, unit.initiative]
    roster.append(rosterUnit)

# Sort roster by turn order
roster.sort()

# Build menus

actionMenu = ButtonMenu('Action Menu')
utilityMenu = ButtonMenu('Utility Menu')

    # Build Main Menu


# def ButtonMenuBuilder(items, menu, cmdType=''):
#     actions = []
#     for i in range(0, len(items)):
#         action = items[i]
#         c = MoveCommand()
#         if(cmdType == 'menu'):
#             c = ChangeMenuCommand(action, items[i])
#         else:
#             c = PrintCommand(UnitMenu(action, items[i]))
#         b = Button(action, c)
#         actions.append(b)
#     menu.setMenuItems(actions)
#
#
# top = roster.peek()
# ButtonMenuBuilder(top.actions, actionMenu)



# Main Loop ##############################################
# This is the way a user interfaces with the data structures.
# It's also going to be the first to go with the GUI upgrade.
#
# currMenu = mainMenu

print roster

# while(True):
#     print '\n'
#     print currMenu
#     user = raw_input("UP[A], DOWN[S], SELECT[Z], BACK[X], EXIT[Q]\n")
#     user = str(user).lower()
#
#     if(user == 'a'):
#         currMenu.up()
#
#     elif(user == 's'):
#         currMenu.down()
#
#     elif(user == 'z'):
#         newMenu = currMenu.select().execute()
#         if(newMenu is not None):
#             currMenu = newMenu
#
#     elif(user == 'x'):
#         newMenu = currMenu.back().execute()
#         if (newMenu is not None):
#             currMenu = newMenu
#
#     elif(user == 'q'):
#         exit(0)
