import csv

ALL_POKEMON = []
ABILITIES = {}

class Pokemon:
    def __init__(self, row):
        self.id = row[0]
        self.name = row[1]
        self.dex = row[2]
        self.type = [row[3], row[4]]
        self.tier = row[5]
        self.item = row[6]
        self.ability = row[7]
        self.evSpread = row[8]
        self.nature = row[9]
        self.ivSpread = row[10]
        self.moves = [row[11], row[12], row[13], row[14]]

with open('main_database.csv', 'r') as fileName:
    reader = csv.reader(fileName)
    next(reader, None)
    for row in reader:
        if row[1] == "Claydol":
            break
        else:
            ALL_POKEMON.append(Pokemon(row))

with open('Abilities.csv', 'r') as fileName:
    reader = csv.reader(fileName)
    for row in reader:
        ABILITIES[row[0]] = [row[x] for x in range(1,4) if row[x] != '']
