"""
The Skill class.
A subclass of the Command class that specifically relates to combat actions.
"""

import copy
from Command import*

class Skill(Command):
    def __init__(self, skillDict):
        self.name = skillDict['name']
        self.cost = skillDict['cost']
        self.target = skillDict['target']
        self.range = skillDict['range']
        self.area = skillDict['area']
        self.effect = skillDict['effect']

        # Parse effect and make that into the execute action

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
        if(user.fp >= self.cost and user.canAct()):
            return self.target
        else:
            return None

    def activate(self, target, battlemap):
        """
        Executes the game logic behind a skill.

        :param target: A tile from the BattleMap that species the target location.
        :return: 0 if the skill can be used on that target, None if it can't.
        """
        pass

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
        space = battlemap.getObject(target)
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
        move = {'name': 'Move', 'cost': '10FP', 'target': 'OneEmpty', 'range': 'None', 'area': 'Single', 'effect': 'None'}
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
        end = {'name': 'End Turn', 'cost': '0FP', 'target': 'Self', 'range': 'None', 'area': 'Single',
                'effect': 'None'}
        Skill.__init__(self, end)

    def execute(self, user=None, battlemap=None):
        self.user = user
        return self

    def activate(self, targetTile, battlemap):
        self.user.moved()
        self.user.acted()
        return 0

class UnsupportedActionException(Exception):
    def __str__(self):
        return 'UnsupportedActionException'
