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
    def __init__(self, skillsDict, jobDict):
        self.skillsDict = skillsDict
        self.jobsDict = jobDict

    def createCharacter(self, name, job, level):
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
        '''
        Constructor
        '''

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
        self.hp = ((self.health*2) + self.kine)

        if (self.animus >= self.grace):
            self.fp = (self.health + self.animus)
        else:
            self.fp = (self.health + self.grace)

        self.rt = math.ceil((self.grace + self.animus)/2)
        self.dr = math.ceil((self.kine + self.health)/2)
        self.mv = 5


    def __str__(self):
        return str(self.name)

    def data(self):
        string = (self.name + '\t' + self.jobName + "\n" +
                  '\n' +
                  'Level: ' + '\t' + str(self.level) + '\n' +
                  'Kinesthesis: ' + '\t' + str(self.kine) + '\n' +
                  'Grace: ' + '\t' + str(self.grace) + '\n' +
                  'Animus: ' + '\t' + str(self.animus) + '\n' +
                  'Health: ' + '\t' + str(self.health) + '\n' +
                  '\n'
                  'Hit Points: ' + '\t' + str(self.hp) + '\n' +
                  'Stamina Points: ' + '\t' + str(self.fp) + '\n' +
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
    def __init__(self, character):
        Character.__init__(self, character.name, character.jobName, character.level, character.jobData, character.skills)
        self.currHp = copy.copy(self.hp)
        self.currFp = copy.copy(self.fp)
        self.initiative = copy.copy(self.rt)
        self.location = (0, 0)
        self.canMove = True
        self.canAct = True
        self.ally = True

        moveSkill = Move()
        endTurnSkill = EndTurn()

        self.actions = copy.deepcopy(self.skills)
        self.actions.insert(0, moveSkill)
        self.actions.append(endTurnSkill)

    def data(self):
        string = (self.name + '\t' + self.jobName + "\n" +
                  '\n' +
                  'Hit Points: ' + '\t' + str(self.currHp) + '\n' +
                  'Stamina Points: ' + '\t' + str(self.currFp) + '\n' +
                  'Movement Speed: ' + '\t' + str(self.mv) + '\n' +
                  'Location: ' + '\t' + str(self.location) + '\n' +
                  'Can Move: ' + '\t' + str(self.canMove) + '\n' +
                  'Can Act: ' + '\t' + str(self.canAct) + '\n' +
                  '\n')

        if (self.spirit == 'None'):
            string = string + 'Spirit: ' + '\t' + 'None'
        else:
            string = string + 'Spirit: ' + '\t' + self.spirit

        return string

    def setLocation(self, location):
        self.location = location

    def resetTurn(self):
        self.canMove = True
        self.canAct = True

    def moved(self):
        self.canMove = False

    def acted(self):
        self.canAct = False

    def endTurn(self):
        self.initiative = 0
        self.resetTurn()

    def gainInitiative(self):
        self.initiative += 1

    def setAlly(self, allyStatus):
        self.ally = allyStatus


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