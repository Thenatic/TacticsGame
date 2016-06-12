
import copy
from Command import*

targetTypes = ['OneAny', 'OneUnit', 'OneAlly', 'OneEnemy', 'OneSelf', 'OneEmpty',
               'Square', 'Line', 'Cross', 'Flower',
               'End']

skillDict= {}

class Skill(Command):
    def __init__(self, skillName):
        self.skillName = skillName
        self.targetType = None
        self.user = None
        self.battlemap = None
        self.cmdRange = None

    def __str__(self):
        return self.skillName

    def execute(self, user=None, battlemap=None):
        """
        Takes in information about the user of the skill to determine effect,
        then outputs information about the type of target that the skill can be used on.

        :param user: A BattleCharacter object that specifies the user.
        :param battlemap: A BattleMap object that specifies the map.
        :return: Target type if the skill can be used, None if it can't.
        """

        try:
            skill = skillDict[self.skillName.lower()]()
            return skill.execute(user=user, battlemap=battlemap)
        except:
            raise UnsupportedActionException

        pass

    def activate(self, target):
        """
        Executes the game logic behind a skill.

        :param target: A tile from the BattleMap that species the target location.
        :return: 0 if the skill can be used on that target, None if it can't.
        """
        pass

    def withinDistance(self, target, cmdRange):
        """
        Determines whether a target is within range for the given skill.

        :param target: A tile from the BattleMap that species the target location.
        :param cmdRange: The number of tiles from the user that the command can be executed from.
        :return: True if target is within range, false otherwise.
        """
        userX = self.user.location[0]
        userY = self.user.location[1]
        targetX = target.location[0]
        targetY = target.location[1]

        self.distance = abs(userX - targetX) + abs(userY - targetY)

        if(self.distance <= self.cmdRange):
            return True
        else:
            return False

    def isProperTargetType(self, target, targetType):
        space = self.battlemap.getObject(target)
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
        Skill.__init__(self, 'move')
        self.targetType = 'OneEmpty'

    def getTargetType(self):
        return 'OneEmpty'

    def execute(self, user=None, battlemap=None):
        #Check if user can move
        if(user.canMove):
            self.user = user
            self.battlemap = battlemap
            self.cmdRange = user.mv
            return self
        else:
            return None

    def activate(self, targetTile):
        if(self.withinDistance(targetTile, self.cmdRange) and self.isProperTargetType(targetTile, self.targetType)):
            self.oldLocation = copy.copy(self.user.location)
            self.user.location = copy.copy(targetTile.location)
            self.user.moved()
            self.battlemap.moveObject(self.user)
            return 0

        else:
            return None


class EndTurn(Skill):
    def __init__(self):
        Skill.__init__(self, 'end')
        self.targetType = 'OneSelf'

    def execute(self, user=None, battlemap=None):
        self.user = user
        return self

    def activate(self, targetTile):
        self.user.moved()
        self.user.acted()
        return 0


class Rend(Skill):
    def __init__(self):
        Skill.__init__(self, 'rend')
        self.targetType = 'OneEnemy'

    def execute(self, user=None, battlemap=None):
        if(user.canAct):
            self.user = user
            self.battlemap = battlemap
            self.cmdRange = 1
            return self
        else:
            return None

    def activate(self, targetTile):
        if (self.withinDistance(targetTile, self.cmdRange) and self.isProperTargetType(targetTile, self.targetType)):
            target = self.battlemap.getObject(targetTile)
            target.currHp = 1
            self.user.acted()
            return 0
        else:
            return None


class UnsupportedActionException(Exception):
    def __str__(self):
        return 'UnsupportedActionException'


skillDict = {'move': Move, 'end': EndTurn, 'rend': Rend}