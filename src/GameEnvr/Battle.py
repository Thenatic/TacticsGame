"""
The Battle environment.
Currently used for testing character and command classes.
"""


import os, argparse

from src.Elements.Menu import*
from src.Elements.Button import*
from src.Elements.Roster import*
from src.Utility.save_load import*
from src.Utility.file_parser import *




def parse_args():
    parser = argparse.ArgumentParser(description="Runs the battle environment.")
    parser.add_argument('job_filename', default="Jobs_Fantasy",
                        help="Name of file containing a JSON with all the classes in this game system.")
    parser.add_argument('skills_filename', default="Skills_Fantasy",
                        help="Name of file containing a JSON with all the skills in this game system.")
    parser.add_argument('map_filename', default="Fields",
                        help="Name of file containing a JSON with terrain information for this battle.")
    parser.add_argument('enc_filename', default="Fields_01",
                        help="Name of file containing a JSON with encounter information for this battle.")
    args = parser.parse_args()
    return args


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


# A temporary way to translate user input into a tile object
def ParseTarget(string, battlemap):
    """
    Determines the target location of an action by parsing a string.

    :param string:
    :return:
    """
    string = string.strip('()')
    string = string.replace(',', ' ')
    print string
    col = int(string[0])
    row = int(string[2])
    if(row <= battlemap.dimension[1] and col <= battlemap.dimension[0]):
        return (col, row)
        #return battlemap.terrain[row][col]
    else:
        print 'Not in map dimensions.'
        return None


def Battle(job_filename=None, skills_filename=None, map_filename=None, enc_filename=None):
    """
    The main function for the battle environment.

    :param job_filename:
    :param skills_filename:
    :param map_filename:
    :param enc_filename:
    :return:
    """

    # job_filename = "Jobs_Fantasy"
    # skills_filename = "Skills_Fantasy"
    # map_filename = 'Fields'
    # enc_filename = 'Fields_01'

    os.chdir('/home/roy/PycharmProjects/TacticsGame/')

    # Extract information from data files
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

    # Build a roster from the units
    roster = Roster()
    roster.set(battlemap)
    roster.sort()

    # Build empty menus
    actionMenu = ButtonMenu('Action Menu')
    utilityMenu = ButtonMenu('Utility Menu')
    currMenu = actionMenu

    # Main Game Loop [a temporary setup until GUI stuff is built]
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
        print top.data()
        print ''
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
                try:
                    targetLocation = raw_input("Target Location\n")
                    if('x' in targetLocation):
                        break
                    else:
                        targetLocation = ParseTarget(targetLocation, battlemap)
                        if(targetLocation is not None):
                            result = cmdHold.activate(targetLocation, battlemap)
                            if(result is 0):
                                print 'Success'
                            else:
                                print 'Failure'
                except Exception as e:
                    print 'Encountered Problem'
                    print str(e)
                    print ''

        elif(user == 'x'):
            newMenu = currMenu.back().execute()
            if (newMenu is not None):
                currMenu = newMenu

        elif(user == 'q'):
            exit(0)

if __name__ == '__main__':
    args = parse_args()
    Battle(args.job_filename, args.skills_filename, args.map_filename, args.enc_filename)
