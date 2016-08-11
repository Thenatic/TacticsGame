"""
The Unit class [abstract].
Allows for many different unit sub-classes, including Character and Spirit.
"""


import copy
import math

from src.Elements.Skill import*

# LF = [[0,1,0,1], [0,2,0,1]]
# GA = [[1,0,0,1], [1,0,0,2]]
# SW = [[1,1,0,0], [2,1,0,0]]
#
#
# Titles = {'Lord of the Fishes':LF, 'Guardian of Ayn':GA, 'Swordsman of the West': SW}


class Unit:
    def __str__(self):
        return ''

    def __repr__(self):
        return self.__str__()


class UnitFactory:
    """
    An object that stores available skills and jobs for the game. Used to create character objects.
    Applies the Singleton and Factory design patterns.
    """
    def __init__(self, skillsDict, jobDict):
        """
        Cosntructor.
        :param skillsDict: A Python dictionary containing all possible skills for this game.
        :param jobDict: A Python dictionary containing all possible classes for this game.
        """
        self.skillsDict = skillsDict
        self.jobsDict = jobDict

    def createCharacter(self, name, job, level):
        """
        Generates a character object.
        :param name: Character name.
        :param job: Character class.
        :param level: Character level.
        :return: newCharacter [Character]
        """
        jobData = self.jobsDict[job]
        skills = jobData['skills']
        jobSkills = []

        # Fill in other actions
        for skill in skills:
            skillDict = self.skillsDict[skill]
            skillObject = Skill(skillDict)
            jobSkills.append(skillObject)
        newCharacter = Character(name, job, level, jobData, jobSkills)

        return newCharacter

    def createSpirit(self, name, title, level):
        pass

    def createObstacle(self):
        pass

class Character(Unit):
    '''
    The Character object contains data on a specific unit.
    '''

    def __init__(self, charName, charClass, charLevel, jobData, jobSkills):
        """
        Constructor
        """
        #Basic Info
        self.name = charName
        self.level = charLevel-1
        self.jobName = charClass
        self.jobData = jobData
        self.skills = jobSkills
        self.spirit = 'None'
        self.spiritName = 'None'

        #Base Primary Stats
        self.kine = self.jobData['baseStats'][0] + (self.level * self.jobData['growth'][0])
        self.grace = self.jobData['baseStats'][1] + (self.level * self.jobData['growth'][1])
        self.animus = self.jobData['baseStats'][2] + (self.level * self.jobData['growth'][2])
        self.health = self.jobData['baseStats'][3] + (self.level * self.jobData['growth'][3])

        #Base Secondary Stats
        self.maxHp = ((self.health * 2) + self.kine)

        if (self.animus >= self.grace):
            self.maxFp = (self.health + self.animus)
        else:
            self.maxFp = (self.health + self.grace)

        self.rt = math.ceil((self.grace + self.animus)/2)
        self.dr = math.ceil((self.kine + self.health)/2)
        self.mv = 5

    def __str__(self):
        """
        Returns unit's name.
        :return: Name [String]
        """
        return str(self.name)

    def data(self):
        """
        Returns a string containing the unit's stats.
        :return: Data [String]
        """
        string = (self.name + '\t' + self.jobName + "\n" +
                  '\n' +
                  'Level: ' + '\t' + str(self.level) + '\n' +
                  'Kinesthesis: ' + '\t' + str(self.kine) + '\n' +
                  'Grace: ' + '\t' + str(self.grace) + '\n' +
                  'Animus: ' + '\t' + str(self.animus) + '\n' +
                  'Health: ' + '\t' + str(self.health) + '\n' +
                  '\n'
                  'Hit Points: ' + '\t' + str(self.maxHp) + '\n' +
                  'Stamina Points: ' + '\t' + str(self.maxFp) + '\n' +
                  'Damage Reduction: ' + '\t' + str(self.dr) + '\n' +
                  'Reaction Time: ' + '\t' + str(self.rt) + '\n' +
                  'Movement Speed: ' + '\t' + str(self.mv) + '\n' +
                  '\n')

        if (self.spirit == 'None'):
            string = string + 'Spirit: ' + '\t' + 'None'
        else:
            string = string + 'Spirit: ' + '\t' + self.spirit

        return string

    def setSpirit(self, spirit=None):
        '''
        Links a spirit unit with this character
        '''
        if spirit is None:
            self.spirit = 'None'
            self.spiritName = 'None'

        else:
            self.spirit = spirit
            self.spiritName = spirit.name


class BattleCharacter(Character):
    '''
    A temporary instance of the character that contains information for combat.
    Keeps track of things like current hp and location.
    '''
    def __init__(self, character):
        Character.__init__(self, character.name, character.jobName, character.level, character.jobData, character.skills)
        self.hp = copy.copy(self.maxHp)
        self.fp = copy.copy(self.maxFp)
        self.initiative = copy.copy(self.rt)
        self.location = (0, 0)
        self.canMove = True
        self.canAct = True
        self.ally = True
        self.status = []

        moveSkill = Move()
        endTurnSkill = EndTurn()

        self.actions = copy.deepcopy(self.skills)
        self.actions.insert(0, moveSkill)
        self.actions.append(endTurnSkill)

    def data(self):
        """
        Returns a string containing the unit's battle stats.
        :return: Data [String]
        """
        string = (self.name + '\t' + self.jobName + "\n" +
                  '\n' +
                  'Hit Points: ' + '\t' + str(self.hp) + '\n' +
                  'Stamina Points: ' + '\t' + str(self.fp) + '\n' +
                  'Movement Speed: ' + '\t' + str(self.mv) + '\n' +
                  'Location: ' + '\t' + str(self.location) + '\n' +
                  'Can Move: ' + '\t' + str(self.canMove) + '\n' +
                  'Can Act: ' + '\t' + str(self.canAct) + '\n' +
                  'Status: ' + '\t' + str(self.status) + '\n' +
                  '\n')

        if (self.spirit == 'None'):
            string = string + 'Spirit: ' + '\t' + 'None'
        else:
            string = string + 'Spirit: ' + '\t' + self.spirit

        return string

    def setLocation(self, location):
        """
        Sets a unit's location variable (does not set the location on a map).
        :param location:
        """
        self.location = location

    def resetTurn(self):
        """
        Resets a unit's turn, allowing them to move and act.
        """
        self.canMove = True
        self.canAct = True

    def moved(self):
        """
        Disables a unit's ability to move.
        """
        self.canMove = False

    def acted(self):
        """
        Disables a unit's ability to act.
        """
        self.canAct = False

    def endTurn(self):
        """
        Ends a unit's turn, setting them at the bottom of the roster and resetting their turn for the next round.
        """
        self.initiative = 0
        self.resetTurn()

    def gainInitiative(self):
        """
        Increments initiative.
        """
        self.initiative += 1

    def setAlly(self, allyStatus):
        """
        Makes a unit controllable or not.
        :param allyStatus:
        """
        self.ally = allyStatus

    def statusCheck(self):
        """
        Check for changes in status after an attacker
        :return:
        """
        if self.hp <= 0:
            self.status = ['KO']
        elif self.hp > 0 and 'KO' in self.status:
            pass

# class Spirit(Unit):
#     '''
#     The Spirit class contains data on a specific spirit.
#     '''
#
#     def __init__(self, charName, charClass, charLevel):
#         '''
#         Constructor
#         '''
#
#         #Basic Info
#         self.name = charName
#         self.level = charLevel
#         self.jobName = charClass
#         self.job = Titles[charClass]
#
#         #Primary Stats
#         self.kine = self.job[self.level][0]
#         self.grace = self.job[self.level][1]
#         self.animus = self.job[self.level][2]
#         self.health = self.job[self.level][3]
#
#     def __str__(self):
#         return str(self.name)
#
#     def data(self):
#         string = (self.name + '\t' + self.jobName + "\n" +
#                   '\n' +
#                   'Level: ' + '\t' + str(self.level) + '\n' +
#                   'Kinesthesis: ' + '\t' + str(self.kine) + '\n' +
#                   'Grace: ' + '\t' + str(self.grace) + '\n' +
#                   'Animus: ' + '\t' + str(self.animus) + '\n' +
#                   'Health: ' + '\t' + str(self.health) + '\n')
#
#         return string

#class Mook(Unit):