"""
The Main Menu environment.
Currently used for testing menu structure.
"""

from src.Elements.Menu import*
from src.Elements.Button import*
from src.Elements.Command import*
from src.Elements.save_load import*

# Initialize Menus #####################################
mainMenu = Menu('Main Menu')
unitsMenu = Menu('Units')
spiritsMenu = Menu('Spirits')
optionsMenu = Menu('Options')


    # Build Main Menu
menuArray = [unitsMenu, spiritsMenu, optionsMenu]
buttonArray = []

for i in range(0, len(menuArray)):
    c = ChangeMenuCommand(menuArray[i])
    b = Button(menuArray[i].getMenuName(), c)
    buttonArray.append(b)

mainMenu.setMenuItems(buttonArray)

    # Build sub-menus
game = newFile()

def MenuBuilder(items, menu):
    units = []
    for i in range(0, len(items)):
        unit = items[i].name
        c = PrintCommand(unit)
        b = Button(unit, c)
        units.append(b)
    menu.setMenuItems(units)


MenuBuilder(game.characters, unitsMenu)
MenuBuilder(game.spirits, spiritsMenu)



print mainMenu
print unitsMenu
print spiritsMenu

# Main Loop ##############################################
# This is way a user interfaces with the data structures.
# It's also going to be the first to go with the GUI upgrade.


