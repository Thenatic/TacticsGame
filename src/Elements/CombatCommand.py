"""
The CombatCommand class.
Represents the logic of all actions that can be taken during combat.
"""

from Command import*

class CombatCommand(Command):
    """
    Abstract class for
    """
    def __init__(self, cmdName):
        self.cmdName = cmdName

    def __str__(self):
        return self.cmdName

    def execute(self, user=None, target=None, distance=None, cmdRange=None, battlemap=None):
        if('move' in self.cmdName.lower()):
            cmd = MoveCommand()
            return cmd.execute(user=user, target=target, distance=distance, battlemap=battlemap)
        elif('end' in self.cmdName.lower()):
            cmd = EndTurnCommand()
            return cmd.execute(user, target, distance, battlemap)
        else:
            raise UnsupportedActionException

class MoveCommand(CombatCommand):
    def __init__(self):
        CombatCommand.__init__(self, 'move')

    def execute(self, user=None, target=None, distance=None, cmdRange=None, battlemap=None):
        #Check if user can move
        if(user.canMove):
            self.user = user
            self.battlemap = battlemap
            self.cmdRange = user.mv
            return self
        else:
            return None

    def sendTarget(self, target):
        user = self.user
        userX = user.location[0]
        userY = user.location[1]
        targetX = target.location[0]
        targetY = target.location[1]

        self.distance = abs(userX - targetX) + abs(userY - targetY)

        if (self.distance <= self.cmdRange and not self.battlemap.isOccupied(target)):
            self.oldLocation = copy.copy(user.location)
            user.location = copy.copy(target.location)
            user.moved()
            self.battlemap.moveObject(user)
            return 0

        else:
            return None

class MeleeCommand(CombatCommand):
    def __init__(self, attacker, defender):
        CombatCommand.__init__(self, 'melee')
        self.attacker = attacker
        self.defender = defender

    def execute(self, user=None, target=None, distance=None, cmdRange=None, battlemap=None):
        dmg = self.attacker.kine - self.defender.df
        self.defender.currHp -= dmg


class EndTurnCommand(CombatCommand):
    def __init__(self):
        CombatCommand.__init__(self, 'end')

    def execute(self, user=None, target=None, distance=None, cmdRange=None, battlemap=None):
        user.moved()
        user.acted()
        return self

class UnsupportedActionException(Exception):
    def __str__(self):
        return 'UnsupportedActionException'