'''
Save_Load
A way to do read/writes with game data.
'''

import os
import pickle
from src.Elements.Unit import*

def create_file():
    curr = newFile()
    save_file = open(os.path.join('gameSaves', 'currSave'), 'w+')
    pickle.dump(curr, save_file)
    save_file.close()

def load_file():
    save_file = open(os.path.join('gameSaves', 'currSave'), 'r+')
    frank = pickle.load(save_file)
    save_file.close()
    print frank.characters

#def save_game():

class newFile():
    
    def __init__(self, unit_factory):
        self.characters = []
        self.spirits = []

        friendly1 = unit_factory.createCharacter('Steve', 'Thug', 1)
        friendly2 = unit_factory.createCharacter('Anna', 'Mage', 3)
        friendly3 = unit_factory.createCharacter('Frank', 'Thug', 2)
        self.characters = [friendly1, friendly2, friendly3]

        # Add initial spirits
        # Titles = {'Lord of the Fishes':LF, 'Guardian of Ayn':GA, 'Swordsman of the West': SW}
        #
        # spirit1 = Spirit('James', 'Lord of the Fishes', 1)
        # spirit2 = Spirit('Fred', 'Guardian of Ayn', 1)
        # spirit3 = Spirit('Nimrod', 'Swordsman of the West', 1)
        # self.spirits = [spirit1, spirit2, spirit3]



# print os.getcwd()
# os.chdir(r'G:\Dropbox\LiClipseWorkspace\LAON')
# print os.getcwd()
# create_file()
# load_file()
