"""
file_parser.py
Contains functions for converting files into usable data.
"""

import json

from src.Elements.BattleMap import*
from src.Elements.Unit import*


def map_parse(input_file):
    """
    Parses a map file into a map object.
    :param input_file: A text file containing a map JSON.
    :return: battlemap [Map]
    """
    # Make a BattleMap object
    battlemap = BattleMap()

    # Convert map file into python dictionary
    mapDict = file_to_dict(input_file)

    # Pull the terrain data out of mapDict and convert it into a Tile grid
    objects_List_of_Dicts = mapDict['terrain']
    terrain = []
    for i in range(0, len(objects_List_of_Dicts)):
        row = objects_List_of_Dicts[i][str(i)]
        terrainRow = []
        for j in range(0, len(row)):
            tile = battlemap.makeTile(row[j])
            terrainRow.append(tile)
            battlemap.dimension = (j, i)    # Unnecessary overhead
        terrain.append(terrainRow)

    battlemap.terrain = terrain
    return battlemap


def encounter_parse(input_file, game, battlemap, unit_factory):
    """
    Parses an encounter file into an encounter objects.
    :param input_file: A text file containing an encounter JSON.
    :param battlemap: A map object to fill with data from the encounter.
    :return: 0 if it worked.
    """
    # Convert encounter file into python dictionary
    encDict = file_to_dict(input_file)

    # Pull the objects data out of encDict
        # Comes out of the JSON as a list of dicts, needs to be converted to nested list (map grid)
        # CLEAN THIS UP! It's awful.
    objects_List_of_Dicts = encDict['objects']
    objectsList = []


    for i in range(0, len(objects_List_of_Dicts)):
        objectsRow = []
        for j in range(0, len(objects_List_of_Dicts[i])):
            objectsRow.append(objects_List_of_Dicts[i][str(j)])
        objectsList.append(objectsRow)


    battlemap.objects = objectsList

    # Pull the enemy units out of encDict and into objects array
    i = 0
    enemy_id_list = []
    enemy_list = []
    out_of_enemies = False

    while out_of_enemies is False:
        try:
            # Convert json to unit object
            enemy_id = 'bad_' + str(i)
            enemy = encDict[enemy_id]
            enemy = unit_parse(enemy, unit_factory)

            # Convert unit object to battlecharacter object
            enemy = BattleCharacter(enemy)

            # Set alliance
            enemy.setAlly(False)

            # Record id and character objects
            enemy_id_list.append(enemy_id)
            enemy_list.append(enemy)

            i += 1

        except KeyError:
            out_of_enemies = True

    battlemap.replaceObjects(enemy_id_list, enemy_list)

    # Pull victory condition out of encDict and into battlemap
    battlemap.setVictory(encDict['victory_condition'])

    # Pull friendly units from save
    for i in range(0, len(game.characters)):
        unit = game.characters[i]
        unit = BattleCharacter(unit)
        unit.setLocation((i, 0))
        unit.setAlly(True)
        battlemap.addObject(unit, unit.location)

    return 0


def jobs_parse(input_file):
    """
    Runs a Jobs JSON file through the preprocessor and returns a python dictionary.
    :param input_file: Jobs JSON file.
    :return: jobs_dict
    """
    jobs_dict = file_to_dict(input_file)
    return jobs_dict

def skills_parse(input_file):
    """
    Runs a Skills JSON file through the preprocessor and returns a python dictionary.
    :param input_file: Skills JSON file.
    :return: skills_dict
    """
    skills_dict = file_to_dict(input_file)
    return skills_dict


# Auxiliary Functions#########################################
def unit_parse(unit_dict, unit_factory):
    """
    Parses a dictionary representing a unit into a unit object.
    :param unit_dict: {name: "Joe", job: "Thug", level: 3}
    :return: The unit object.
    """
    # Convert dictionary into unit object
    name = str(unit_dict['name'])
    job = str(unit_dict['job'])
    level = int(unit_dict['level'])
    unit = unit_factory.createCharacter(name, job, level)
    return unit


def preprocessor(input_file):
    """
    Cuts out the comments (marked by a '#") from a file and returns the remainder as a string.
    :param input_file: File object to process.
    :return: String object containing non-comments from the file.
    """
    fileString = input_file.read().splitlines()
    fileStringDone = []

    for i in range(0, len(fileString)):
        if('#' not in fileString[i]):
            fileStringDone.append(fileString[i])

    return fileStringDone


def file_to_dict(input_file):
    """
    Converts a file into a python dictionary.
    :param input_file: File containing a JSON and comments.
    :return: Python dictionary of file.
    """
    # File -> String with comments removed
    fileStringList = preprocessor(input_file)

    # String -> String with JSON formatting
    fileString = ' '.join(fileStringList)

    # JSON String -> Unicode formatted Dictionary
    fileDict = json.loads(fileString)

    # Unicode Dictionary -> UTF-8 Dictionary
    fileDict = unicode_to_utf(fileDict)

    return fileDict


def unicode_to_utf(x):
    """
    Converts a unicode dictionary to a UTF-8 dictionary. Also handles nested dictionaries.
    :param x: Unicode dictionary.
    :return: UTF-8 dictionary.
    """
    # Base case, check if it's a unicode string.
    if isinstance(x, unicode):
        return x.encode('utf-8')

    # Next case, check if it's a list.
    elif isinstance(x, list):
        return [unicode_to_utf(element) for element in x]

    # Next case, check if it's a dict.
    elif isinstance(x, dict):
        return {unicode_to_utf(key): unicode_to_utf(value) for key, value in x.iteritems()}

    # Otherwise it's a utf-8 string and we're done.
    else:
        return x

