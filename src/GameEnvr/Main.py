"""
The main game environment.

Manages the game loop and various states. Each state is represented by its own function.
"""

import os

import Main_Menu
import Battle
import World_Map

states = {'Main Menu': Main_Menu, 'Battle': Battle, 'World Map': World_Map}
# currState = 'Main Menu'
# kwargs = None
currState = 'Battle'
# kwargs =


os.chdir('/home/roy/PycharmProjects/TacticsGame/')

while True:
    currState, kwargs = states[currState](kwargs)
