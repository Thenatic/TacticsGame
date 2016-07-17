"""
The Skill class.
A subclass of the Command class that specifically relates to combat actions.
"""

import copy
from Command import*

class Skill(Command):
    def __init__(self, skillDict):
        self.name = skillDict['name']
        self.cost = int(skillDict['cost'])
        self.target = skillDict['target']
        self.range = skillDict['range']
        self.area = skillDict['area']
        self.effect = skillDict['effect']

        self.user = None
        self.effects = []

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    def parseEffect(self):
        pass

    def execute(self, user=None, battlemap=None):
        """
        Takes in information about the user of the skill to determine effect,
        then outputs information about the type of target that the skill can be used on.

        :param user: A BattleCharacter object that specifies the user.
        :param battlemap: A BattleMap object that specifies the map.
        :return: Target type if the skill can be used, None if it can't.
        """
        self.user = user
        if(user.fp >= self.cost and user.canAct):
            effectList = self.effect.split(';')
            for effect in effectList:
                parsedEffect = Effect(user, effect)
                self.effects.append(parsedEffect)
            return self
        else:
            return None

    def activate(self, targetLocation, battlemap):
        """
        Executes the game logic behind a skill.

        :param targetLocation: An xy coordinate from the BattleMap that species the target location.
        :return: 0 if the skill can be used on that target, None if it can't.
        """
        target = battlemap.getObject(targetLocation)
        for effect in self.effects:
            effect.activate(target, targetLocation, battlemap)
        self.user.acted()
        return 0

    def withinDistance(self, userLocation, targetLocation, cmdRange):
        """
        Determines whether a target is within range for the given skill.

        :param target: A tile from the BattleMap that species the target location.
        :return: True if target is within range, false otherwise.
        """
        userX = userLocation[0]
        userY = userLocation[1]
        targetX = targetLocation[0]
        targetY = targetLocation[1]

        distance = abs(userX - targetX) + abs(userY - targetY)

        if(distance <= cmdRange):
            return True
        else:
            return False

    def isProperTargetType(self, target, targetType, battlemap):
        space = str(battlemap.getObject(target))
        print space
        print 'empty'

        if('OneEmpty' in targetType):
            if('empty' in space):
                return True
            else:
                return False

        # if(targetType is 'OneSelf'):
        #     # Build a way for map to check friendly/enemy status
        #     if(space is not 'empty'):
        #         return True
        #     else:
        #         return False
        #
        # if(targetType is 'OneEnemy'):
        #     if(space is not 'empty' and space.ally is False):
        #         return True
        #     else:
        #         return False
        #
        # if (targetType is 'OneAlly'):
        #     if (space is not 'empty' and space.ally is True):
        #         return True
        #     else:
        #         return False



class Move(Skill):
    def __init__(self):
        move = {'name': 'Move', 'cost': '10', 'target': 'OneEmpty', 'range': 'None', 'area': 'Single', 'effect': 'None'}
        Skill.__init__(self, move)

    def getTargetType(self):
        return 'OneEmpty'

    def execute(self, user=None, battlemap=None):
        #Check if user can move
        if(user.canMove):
            self.user = user
            self.cmdRange = user.mv
            return self
        else:
            return None

    def activate(self, targetLocation, battlemap):
        """

        :param targetLocation: An xy coordinate pair (1,2).
        :param battlemap:
        :return:
        """
        if(self.withinDistance(self.user.location, targetLocation, self.cmdRange) and self.isProperTargetType(targetLocation, self.target, battlemap)):
            self.oldLocation = copy.copy(self.user.location)
            self.user.location = copy.copy(targetLocation)
            self.user.moved()
            battlemap.moveObject(self.user)
            return 0

        else:
            return None


class EndTurn(Skill):
    def __init__(self):
        end = {'name': 'End Turn', 'cost': '0', 'target': 'Self', 'range': 'None', 'area': 'Single',
                'effect': 'None'}
        Skill.__init__(self, end)

    def execute(self, user=None, battlemap=None):
        self.user = user
        return self

    def activate(self, targetLocation, battlemap):
        self.user.moved()
        self.user.acted()
        return 0


class Effect():
    """
    A class for translating the "effect" attribute of a skill to game logic.
    Parses a string into various game effects.
    """
    def __init__(self, user, skillString):
        attributes = ['hp', 'fp', 'kine', 'grace', 'animus', 'health', 'rt', 'dr', 'mv']
        status = []

        skillTokens = skillString.lower().split()
        self.user = user
        self.target = None
        self.type = None

        # Attribute command values
        self.effectTarget = None
        self.attribute = None
        self.polarity = None
        self.expr = None

        # Determine target [user/not user]
        if 'user' in skillTokens[0]:
            self.effectTarget = 'user'
        elif 'target' in skillTokens[0]:
            self.effectTarget = 'target'
        else:
            raise BadEffectFormattingException

        # Determine effect type [attribute/status/movement]

        # Attribute
        if skillTokens[1] in attributes:
            self.type = 'attribute'
            self.attribute = skillTokens[1]
            if 'up' in skillTokens[2]:
                self.polarity = '+'
            elif 'down' in skillTokens[2]:
                self.polarity = '-'
            else:
                raise BadEffectFormattingException

            self.expr = ''.join(skillTokens[3:])


        # Status Effect

        # Movement

    def execute(self, user=None, battlemap=None):
        self.user = user

    def activate(self, target, targetLocation, battlemap):
        self.target = target

        if 'attribute' in self.type:
            stat = 'target.' + self.attribute
            effect = stat + self.polarity + self.expr
            self.evalEffectExpr(stat, effect)

            # target.stat = target.stat - expr

    def evalEffectExpr(self, stat, effect):

        # Create a list of all possible stats (i.e. user.hp, target.mv)
        # and map them to values (i.e. {user.hp, 50})
        attributes = ['hp', 'fp', 'kine', 'grace', 'animus', 'health', 'rt', 'dr', 'mv']
        statDict = {}

        for attribute in attributes:
            statDict['user.'+attribute] = str(getattr(self.user, attribute))
            statDict['target.'+attribute] = str(getattr(self.target, attribute))

        # Replace keywords in the expression with their values
        for stat in statDict.keys():
            effect = effect.replace(stat, statDict[stat])

        # Evaluate expression to get the value
        value = eval(effect)

        # Apply the relevant effect to the relevant stat
        setattr(self.target, self.attribute, value)
        return 0


class UnsupportedActionException(Exception):
    def __str__(self):
        return 'UnsupportedActionException'


class BadEffectFormattingException(Exception):
    def __str__(self):
        return 'BadEffectFormattingException'
