"""
The Command class [abstract].
Allows for the creation of many different Command sub-classes.
"""


class Command:
    def execute(self):
        raise UnsupportedActionException

    def unexecute(self):
        raise UnsupportedActionException

    def copy(self):
        raise UnsupportedActionException

    def canUndo(self):
        raise UnsupportedActionException


class NullCommand:
    def __init__(self):
        self.name = 'None'

    def __str__(self):
        return self.name

    def execute(self):
        return None

    def unexecute(self):
        return None

    def copy(self):
        return None

    def canUndo(self):
        return None


class PrintCommand(Command):
    def __init__(self, output):
        self.output = output

    def __str__(self):
        return self.output

    def execute(self):
        print str(self.output)
        return None

    def unexecute(self):
        print 'Command Unworked'

    def copy(self):
        cmd = PrintCommand(self.output)
        return cmd

    def canUndo(self):
        return True


class ChangeMenuCommand(Command):
    def __init__(self, name, targetMenu):
        self.name = name
        self.targetMenu = targetMenu

    def __str__(self):
        return self.name

    def execute(self):
        return self.targetMenu

    def unexecute(self):
        return None

    def copy(self):
        cmd = ChangeMenuCommand(self.targetMenu)
        return cmd

    def canUndo(self):
        return True


# class Melee(Command):
#     def __init__(self, attacker, defender):
#         self.attacker = attacker
#         self.defender = defender
#
#     def execute(self):
#         dmg = self.attacker.kine - self.defender.df
#         self.defender.currHp -= dmg
#
# class MoveCommand(Command):
#     def __init__(self, mover):
#         self.range = mover.mv
#
#     #def execute(self):



class CommandHistory:

    def __init__(self):
        self.cmdHistory = []
        self.index = 0

    def addCommand(self, cmd):
        #If other command exist after the index, remove them
        size = len(self.cmdHistory)
        if size != 0 and self.index != size:
            for i in range (size-1, 0):
                self.cmdHistory.pop(i)

        #Add command and increment index
        self.cmdHistory.append(cmd)
        self.index += 1

    def undo(self):
        if self.index != 0:
            cmd = self.cmdHistory[self.index-1]
            self.index -= 1
            return cmd

    def redo(self):
        if self.index != len(self.cmdHistory):
            cmd = self.cmdHistory[self.index]
            self.index += 1
            return cmd

class UnsupportedActionException(Exception):
    def __str__(self):
        return 'UnsupportedActionException'