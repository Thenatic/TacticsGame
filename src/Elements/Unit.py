"""
The Unit class [abstract].
Allows for many different unit sub-classes, including Character and Spirit.
"""

#Job Data
#
#JobName = [ [lvl1 kine, lvl1 grace, lvl1 animus, lvl1 health],
#            [lvl2 kine, lvl2 grace, lvl2 animus, lvl2 health] ]

AP = [[5,5,5,5], [6,6,6,6]]
MT = [[5,5,5,5], [6,6,6,6]]
NM = [[5,5,5,5], [6,6,6,6]]
TG = [[5,5,5,5], [6,6,6,6]]

LF = [[0,1,0,1], [0,2,0,1]]
GA = [[1,0,0,1], [1,0,0,2]]
SW = [[1,1,0,0], [2,1,0,0]]

Classes = {'Apostate':AP, 'Monster':MT, 'Necromancer':NM, 'Thug':TG}
Titles = {'Lord of the Fishes':LF, 'Guardian of Ayn':GA, 'Swordsman of the West': SW}



#Job Array
jobArray = [AP, MT, NM, TG]

class Unit:
    def __str__(self):
        return ''


class Character(Unit):
    '''
    The Character object contains data on a specific unit.
    '''

    def __init__(self, charName, charClass, charLevel):
        '''
        Constructor
        '''

        #Basic Info
        self.name = charName
        self.level = charLevel
        self.jobName = charClass
        self.job = Classes[charClass]
        self.spirit = 'None'
        self.spiritName = 'None'



        #Base Primary Stats
        self.kine = self.job[self.level][0]
        self.grace = self.job[self.level][1]
        self.animus = self.job[self.level][2]
        self.health = self.job[self.level][3]

        #Base Secondary Stats
            #HP
        self.hp = ((self.health*2) + self.kine)

            #FP
        if self.animus >= self.grace:
            self.fp = (self.health + self.animus)
        else:
            self.fp = (self.health + self.grace)

            #Reaction Time
        self.rt = (self.grace + self.animus)/2

            #Damage Reduction
        self.dr = (self.rt + self.health)/2

            #Movement
        self.mv = 5

    def setSpirit(self, spirit=None):
        '''
        Links a spirit unit with this unit
        '''
        if spirit == None:
            self.spirit = 'None'
            self.spiritName = 'None'

        else:
            self.spirit = spirit
            self.spiritName = spirit.name


class Spirit(Unit):
    '''
    The Spirit class contains data on a specific spirit.
    '''

    def __init__(self, charName, charClass, charLevel):
        '''
        Constructor
        '''

        #Basic Info
        self.name = charName
        self.level = charLevel
        self.jobName = charClass
        self.job = Titles[charClass]



        #Primary Stats
        self.kine = self.job[self.level][0]
        self.grace = self.job[self.level][1]
        self.animus = self.job[self.level][2]
        self.health = self.job[self.level][3]