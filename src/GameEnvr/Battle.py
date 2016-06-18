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
from src.Elements.Roster import*
from src.Utility.save_load import*
from src.Utility.file_parser import *


# Initialize Units #####################################

# Create and populate the battlefield
job_filename = "Jobs_Fantasy"
skills_filename = "Skills_Fantasy"
map_filename = 'Fields'
enc_filename = 'Fields_01'
job_file = open(os.path.join(os.getcwd() + '/data/Jobs', job_filename), 'r')
skill_file = open(os.path.join(os.getcwd() + '/data/Skills', skills_filename), 'r')
map_file = open(os.path.join(os.getcwd() + '/data/Maps', map_filename), 'r')
enc_file = open(os.path.join(os.getcwd() + '/data/Encounters', enc_filename), 'r')
jobs = jobs_parse(job_file)
skills = skills_parse(skill_file)
battlemap = map_parse(map_file)

unit_factory = UnitFactory(skills, jobs)
game = newFile(unit_factory)
encounter_parse(enc_file, game, battlemap, unit_factory)




# Sort roster by turn order
roster = Roster()
roster.set(battlemap)
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
        b = Button(str(action), action)
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
    if(row <= battlemap.dimension[0] and col <= battlemap.dimension[1]):
        return (row, col)
        #return battlemap.terrain[row][col]
    else:
        print 'Not in map dimensions.'
        return None


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
    print battlemap.data()
    print battlemap.onTileData()
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
        cmdHold = currMenu.select().execute(user=top, battlemap=battlemap)
        if(cmdHold is not None):
            target = raw_input("Target Location\n")
            if('x' in target):
                break
            else:
                target = ParseTarget(target)
                if(target is not None):
                    result = cmdHold.activate(target, battlemap)
                    if(result is 0):
                        print 'Success'
                    else:
                        print 'Failure'

    elif(user == 'x'):
        newMenu = currMenu.back().execute()
        if (newMenu is not None):
            currMenu = newMenu

    elif(user == 'q'):
        exit(0)
