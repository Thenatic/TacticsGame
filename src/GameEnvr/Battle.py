"""
The Battle environment.
Currently used for testing character and command classes.
"""


import os

# import os, pygame, sys
# from pygame.locals import*

os.chdir('/home/roy/PycharmProjects/TacticsGame/')

from src.Elements.Menu import*
from src.Elements.Button import*
from src.Elements.CombatCommand import*
from src.Elements.Roster import*
from src.Utility.save_load import*
from src.Utility.map_parse import map_parse


# Initialize Units #####################################
game = newFile()
bads = tempFile()   #Replace later with encounter-specific stuff
roster = Roster()

filename = 'Fields'
map_file = open(os.path.join(os.getcwd() + '/data/Maps', filename), 'r')
battlefield = map_parse(map_file)

# Pull friendly units from save
for i in range(0, len(game.characters)):
    unit = game.characters[i]
    unit = BattleCharacter(unit)
    unit.setLocation((i, 0))
    battlefield.addObject(unit, unit.location)
    rosterUnit = [unit, unit.initiative]
    roster.append(rosterUnit)


# Pull unfriendly units from encounter
for i in range(0, len(bads.characters)):
    unit = bads.characters[i]
    unit = BattleCharacter(unit)
    unit.setLocation((i, 4))
    battlefield.addObject(unit, unit.location)
    rosterUnit = [unit, unit.initiative]
    roster.append(rosterUnit)

# Sort roster by turn order
roster.sort()

# Build empty menus
actionMenu = ButtonMenu('Action Menu')
utilityMenu = ButtonMenu('Utility Menu')


# Define useful functions

def ButtonMenuBuilder(items, menu, cmdType=''):
    """
    Builds a button menu out of a list

    :param items: Things that become buttons.
    :param menu:  Menu to put buttons in.
    :param cmdType:
    :return:
    """
    actions = []
    for i in range(0, len(items)):
        action = items[i]
        c = CombatCommand(action)
        b = Button(action, c)
        actions.append(b)
    menu.setMenuItems(actions)

#A temporary way to translate user input into a tile object
def ParseTarget(string):
    """
    Determines the target of an action by parsing a string.

    :param string:
    :return:
    """
    string = string.strip('()')
    string = string.replace(',', ' ')
    print string
    row = int(string[0])
    col = int(string[2])
    return battlefield.terrain[col][row]

#
#
# top = roster.peek()
# ButtonMenuBuilder(top.actions, actionMenu)



# Main Loop ##############################################
# This is the way a user interfaces with the data structures.
# It's also going to be the first to go with the GUI upgrade.
#
# currMenu = mainMenu

#print roster

currMenu = actionMenu

while(True):
    top = roster.peek()[0]

    # Check if unit turn is done, and rotate roster if so.
    if(top.canMove is False and top.canAct is False):
        top.endTurn()
        roster.timePassed()
        top = roster.peek()[0]

    # Print battlefield data.
    print '\n'
    print battlefield.data()
    print battlefield.onTileData()
    print '\n'
    print roster
    print '\n'

    # Setup the action menu.
    ButtonMenuBuilder(top.actions, actionMenu)
    print str(top)
    print actionMenu.data()

    # Act on user input.
    user = raw_input("UP[A], DOWN[S], SELECT[Z], BACK[X], EXIT[Q]\n")
    user = str(user).lower()

    if(user == 'a'):
        currMenu.up()

    elif(user == 's'):
        currMenu.down()

    elif(user == 'z'):
        cmdHold = currMenu.select().execute(user=top, battlemap=battlefield)
        if('end' not in cmdHold.cmdName):
            target = raw_input("Target Location\n")
            if('x' in target):
                break
            else:
                target = ParseTarget(target)
                cmdHold.sendTarget(target)

    elif(user == 'x'):
        newMenu = currMenu.back().execute()
        if (newMenu is not None):
            currMenu = newMenu

    elif(user == 'q'):
        exit(0)
