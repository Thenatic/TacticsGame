"""
map_parse
Takes in map files (.txt) and parses them into Map objects.
"""

from src.Elements.BattleMap import*


def map_parse(file):
    map = BattleMap()
    mapString = preprocessor(file)

    # This is a list comprehension that lets me create a nested list
    # [[], [], [], []] <-- Looks like this
    map.setMap([[] for _ in range(len(mapString))])

    for i in range(0, len(mapString)):
        line = mapString[i].split(' ')
        for j in range(0, len(line)):
            map.addTile(line[j])
        map.nextRow()

    return map

def preprocessor(file):
    mapString = file.read().splitlines()
    mapStringDone = []

    for i in range(0, len(mapString)):
        if('#' not in mapString[i]):
            mapStringDone.append(mapString[i])

    return mapStringDone
