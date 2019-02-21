import csv

TypeChart = {
    ("Bug", "Bug")      : 0,
    ("Bug", "Dark")     : 1,
    ("Bug", "Dragon")   : 0,
    ("Bug", "Electric") : 0,
    ("Bug", "Fairy")    : -1,
    ("Bug", "Fighting") : -1,
    ("Bug", "Fire")     : -1,
    ("Bug", "Flying")   : -1,
    ("Bug", "Ghost")    : -1,
    ("Bug", "Grass")    : 1,
    ("Bug", "Ground")   : 0,
    ("Bug", "Ice")      : 0,
    ("Bug", "Normal")   : 0,
    ("Bug", "Poison")   : -1,
    ("Bug", "Psychic")  : 1,
    ("Bug", "Rock")     : 0,
    ("Bug", "Steel")    : -1,
    ("Bug", "Water")    : 0,

    ("Dark", "Bug")      : 0,
    ("Dark", "Dark")     : -1,
    ("Dark", "Dragon")   : 0,
    ("Dark", "Electric") : 0,
    ("Dark", "Fairy")    : -1,
    ("Dark", "Fighting") : -1,
    ("Dark", "Fire")     : 0,
    ("Dark", "Flying")   : 0,
    ("Dark", "Ghost")    : 1,
    ("Dark", "Grass")    : 0,
    ("Dark", "Ground")   : 0,
    ("Dark", "Ice")      : 0,
    ("Dark", "Normal")   : 0,
    ("Dark", "Poison")   : 0,
    ("Dark", "Psychic")  : 1,
    ("Dark", "Rock")     : 0,
    ("Dark", "Steel")    : 0,
    ("Dark", "Water")    : 0,

    ("Dragon", "Bug")      : 0,
    ("Dragon", "Dark")     : 0,
    ("Dragon", "Dragon")   : 1,
    ("Dragon", "Electric") : 0,
    ("Dragon", "Fairy")    : -1,
    ("Dragon", "Fighting") : 0,
    ("Dragon", "Fire")     : 0,
    ("Dragon", "Flying")   : 0,
    ("Dragon", "Ghost")    : 0,
    ("Dragon", "Grass")    : 0,
    ("Dragon", "Ground")   : 0,
    ("Dragon", "Ice")      : 0,
    ("Dragon", "Normal")   : 0,
    ("Dragon", "Poison")   : 0,
    ("Dragon", "Psychic")  : 0,
    ("Dragon", "Rock")     : 0,
    ("Dragon", "Steel")    : -1,
    ("Dragon", "Water")    : 0,

    ("Electric", "Bug")      : 0,
    ("Electric", "Dark")     : 0,
    ("Electric", "Dragon")   : -1,
    ("Electric", "Electric") : -1,
    ("Electric", "Fairy")    : 0,
    ("Electric", "Fighting") : 0,
    ("Electric", "Fire")     : 0,
    ("Electric", "Flying")   : 1,
    ("Electric", "Ghost")    : 0,
    ("Electric", "Grass")    : -1,
    ("Electric", "Ground")   : -1,
    ("Electric", "Ice")      : 0,
    ("Electric", "Normal")   : 0,
    ("Electric", "Poison")   : 0,
    ("Electric", "Psychic")  : 0,
    ("Electric", "Rock")     : 0,
    ("Electric", "Steel")    : 0,
    ("Electric", "Water")    : 1,

    ("Fairy", "Bug")      : 0,
    ("Fairy", "Dark")     : 1,
    ("Fairy", "Dragon")   : 1,
    ("Fairy", "Electric") : 0,
    ("Fairy", "Fairy")    : 0,
    ("Fairy", "Fighting") : 1,
    ("Fairy", "Fire")     : -1,
    ("Fairy", "Flying")   : 0,
    ("Fairy", "Ghost")    : 0,
    ("Fairy", "Grass")    : 0,
    ("Fairy", "Ground")   : 0,
    ("Fairy", "Ice")      : 0,
    ("Fairy", "Normal")   : 0,
    ("Fairy", "Poison")   : -1,
    ("Fairy", "Psychic")  : 0,
    ("Fairy", "Rock")     : 0,
    ("Fairy", "Steel")    : -1,
    ("Fairy", "Water")    : 0,

    ("Fighting", "Bug")      : -1,
    ("Fighting", "Dark")     : 1,
    ("Fighting", "Dragon")   : 0,
    ("Fighting", "Electric") : 0,
    ("Fighting", "Fairy")    : 1,
    ("Fighting", "Fighting") : 0,
    ("Fighting", "Fire")     : 0,
    ("Fighting", "Flying")   : -1,
    ("Fighting", "Ghost")    : -1,
    ("Fighting", "Grass")    : 0,
    ("Fighting", "Ground")   : 0,
    ("Fighting", "Ice")      : 1,
    ("Fighting", "Normal")   : 1,
    ("Fighting", "Poison")   : -1,
    ("Fighting", "Psychic")  : -1,
    ("Fighting", "Rock")     : 1,
    ("Fighting", "Steel")    : 1,
    ("Fighting", "Water")    : 0,

    ("Fire", "Bug")      : 1,
    ("Fire", "Dark")     : 0,
    ("Fire", "Dragon")   : -1,
    ("Fire", "Electric") : 0,
    ("Fire", "Fairy")    : 0,
    ("Fire", "Fighting") : 0,
    ("Fire", "Fire")     : -1,
    ("Fire", "Flying")   : 0,
    ("Fire", "Ghost")    : 0,
    ("Fire", "Grass")    : 1,
    ("Fire", "Ground")   : 0,
    ("Fire", "Ice")      : 1,
    ("Fire", "Normal")   : 0,
    ("Fire", "Poison")   : 0,
    ("Fire", "Psychic")  : 0,
    ("Fire", "Rock")     : -1,
    ("Fire", "Steel")    : 1,
    ("Fire", "Water")    : -1,

    ("Flying", "Bug")      : 1,
    ("Flying", "Dark")     : 0,
    ("Flying", "Dragon")   : 0,
    ("Flying", "Electric") : -1,
    ("Flying", "Fairy")    : 0,
    ("Flying", "Fighting") : 1,
    ("Flying", "Fire")     : 0,
    ("Flying", "Flying")   : 0,
    ("Flying", "Ghost")    : 0,
    ("Flying", "Grass")    : 1,
    ("Flying", "Ground")   : 0,
    ("Flying", "Ice")      : 0,
    ("Flying", "Normal")   : 0,
    ("Flying", "Poison")   : 0,
    ("Flying", "Psychic")  : 0,
    ("Flying", "Rock")     : -1,
    ("Flying", "Steel")    : -1,
    ("Flying", "Water")    : 0,

    ("Ghost", "Bug")      : 0,
    ("Ghost", "Dark")     : -1,
    ("Ghost", "Dragon")   : 0,
    ("Ghost", "Electric") : 0,
    ("Ghost", "Fairy")    : 0,
    ("Ghost", "Fighting") : 0,
    ("Ghost", "Fire")     : 0,
    ("Ghost", "Flying")   : 0,
    ("Ghost", "Ghost")    : 1,
    ("Ghost", "Grass")    : 0,
    ("Ghost", "Ground")   : 0,
    ("Ghost", "Ice")      : 0,
    ("Ghost", "Normal")   : -1,
    ("Ghost", "Poison")   : 0,
    ("Ghost", "Psychic")  : 1,
    ("Ghost", "Rock")     : 0,
    ("Ghost", "Steel")    : 0,
    ("Ghost", "Water")    : 0,

    ("Grass", "Bug")      : -1,
    ("Grass", "Dark")     : 0,
    ("Grass", "Dragon")   : -1,
    ("Grass", "Electric") : 0,
    ("Grass", "Fairy")    : 0,
    ("Grass", "Fighting") : 0,
    ("Grass", "Fire")     : -1,
    ("Grass", "Flying")   : -1,
    ("Grass", "Ghost")    : 0,
    ("Grass", "Grass")    : -1,
    ("Grass", "Ground")   : 1,
    ("Grass", "Ice")      : 0,
    ("Grass", "Normal")   : 0,
    ("Grass", "Poison")   : -1,
    ("Grass", "Psychic")  : 0,
    ("Grass", "Rock")     : 1,
    ("Grass", "Steel")    : -1,
    ("Grass", "Water")    : 1,

    ("Ground", "Bug")      : -1,
    ("Ground", "Dark")     : 0,
    ("Ground", "Dragon")   : 0,
    ("Ground", "Electric") : 1,
    ("Ground", "Fairy")    : 0,
    ("Ground", "Fighting") : 0,
    ("Ground", "Fire")     : 1,
    ("Ground", "Flying")   : -1,
    ("Ground", "Ghost")    : 0,
    ("Ground", "Grass")    : -1,
    ("Ground", "Ground")   : 0,
    ("Ground", "Ice")      : 0,
    ("Ground", "Normal")   : 0,
    ("Ground", "Poison")   : 1,
    ("Ground", "Psychic")  : 0,
    ("Ground", "Rock")     : 1,
    ("Ground", "Steel")    : 1,
    ("Ground", "Water")    : 0,

    ("Ice", "Bug")      : 0,
    ("Ice", "Dark")     : 0,
    ("Ice", "Dragon")   : 1,
    ("Ice", "Electric") : 0,
    ("Ice", "Fairy")    : 0,
    ("Ice", "Fighting") : 0,
    ("Ice", "Fire")     : -1,
    ("Ice", "Flying")   : 1,
    ("Ice", "Ghost")    : 0,
    ("Ice", "Grass")    : 1,
    ("Ice", "Ground")   : 1,
    ("Ice", "Ice")      : -1,
    ("Ice", "Normal")   : 0,
    ("Ice", "Poison")   : 0,
    ("Ice", "Psychic")  : 0,
    ("Ice", "Rock")     : 0,
    ("Ice", "Steel")    : -1,
    ("Ice", "Water")    : -1,

    ("Normal", "Bug")      : 0,
    ("Normal", "Dark")     : 0,
    ("Normal", "Dragon")   : 0,
    ("Normal", "Electric") : 0,
    ("Normal", "Fairy")    : 0,
    ("Normal", "Fighting") : 0,
    ("Normal", "Fire")     : 0,
    ("Normal", "Flying")   : 0,
    ("Normal", "Ghost")    : -1,
    ("Normal", "Grass")    : 0,
    ("Normal", "Ground")   : 0,
    ("Normal", "Ice")      : 0,
    ("Normal", "Normal")   : 0,
    ("Normal", "Poison")   : 0,
    ("Normal", "Psychic")  : 0,
    ("Normal", "Rock")     : -1,
    ("Normal", "Steel")    : -1,
    ("Normal", "Water")    : 0,

    ("Poison", "Bug")      : 0,
    ("Poison", "Dark")     : 0,
    ("Poison", "Dragon")   : 0,
    ("Poison", "Electric") : 0,
    ("Poison", "Fairy")    : 1,
    ("Poison", "Fighting") : 0,
    ("Poison", "Fire")     : 0,
    ("Poison", "Flying")   : 0,
    ("Poison", "Ghost")    : -1,
    ("Poison", "Grass")    : 1,
    ("Poison", "Ground")   : -1,
    ("Poison", "Ice")      : 0,
    ("Poison", "Normal")   : 0,
    ("Poison", "Poison")   : -1,
    ("Poison", "Psychic")  : 0,
    ("Poison", "Rock")     : -1,
    ("Poison", "Steel")    : -1,
    ("Poison", "Water")    : 0,

    ("Psychic", "Bug")      : 0,
    ("Psychic", "Dark")     : -1,
    ("Psychic", "Dragon")   : 0,
    ("Psychic", "Electric") : 0,
    ("Psychic", "Fairy")    : 0,
    ("Psychic", "Fighting") : 1,
    ("Psychic", "Fire")     : 0,
    ("Psychic", "Flying")   : 0,
    ("Psychic", "Ghost")    : 0,
    ("Psychic", "Grass")    : 0,
    ("Psychic", "Ground")   : 0,
    ("Psychic", "Ice")      : 0,
    ("Psychic", "Normal")   : 0,
    ("Psychic", "Poison")   : 1,
    ("Psychic", "Psychic")  : -1,
    ("Psychic", "Rock")     : 0,
    ("Psychic", "Steel")    : -1,
    ("Psychic", "Water")    : 0,

    ("Rock", "Bug")      : 1,
    ("Rock", "Dark")     : 0,
    ("Rock", "Dragon")   : 0,
    ("Rock", "Electric") : 0,
    ("Rock", "Fairy")    : 0,
    ("Rock", "Fighting") : -1,
    ("Rock", "Fire")     : 1,
    ("Rock", "Flying")   : 1,
    ("Rock", "Ghost")    : 0,
    ("Rock", "Grass")    : 0,
    ("Rock", "Ground")   : -1,
    ("Rock", "Ice")      : 1,
    ("Rock", "Normal")   : 0,
    ("Rock", "Poison")   : 0,
    ("Rock", "Psychic")  : 0,
    ("Rock", "Rock")     : 0,
    ("Rock", "Steel")    : -1,
    ("Rock", "Water")    : 0,

    ("Steel", "Bug")      : 0,
    ("Steel", "Dark")     : 0,
    ("Steel", "Dragon")   : 0,
    ("Steel", "Electric") : -1,
    ("Steel", "Fairy")    : 1,
    ("Steel", "Fighting") : 0,
    ("Steel", "Fire")     : -1,
    ("Steel", "Flying")   : 0,
    ("Steel", "Ghost")    : 0,
    ("Steel", "Grass")    : 0,
    ("Steel", "Ground")   : 0,
    ("Steel", "Ice")      : 1,
    ("Steel", "Normal")   : 0,
    ("Steel", "Poison")   : 0,
    ("Steel", "Psychic")  : 0,
    ("Steel", "Rock")     : 1,
    ("Steel", "Steel")    : -1,
    ("Steel", "Water")    : -1,

    ("Water", "Bug")      : 0,
    ("Water", "Dark")     : 0,
    ("Water", "Dragon")   : -1,
    ("Water", "Electric") : 0,
    ("Water", "Fairy")    : 0,
    ("Water", "Fighting") : 0,
    ("Water", "Fire")     : 1,
    ("Water", "Flying")   : 0,
    ("Water", "Ghost")    : 0,
    ("Water", "Grass")    : -1,
    ("Water", "Ground")   : 1,
    ("Water", "Ice")      : 0,
    ("Water", "Normal")   : 0,
    ("Water", "Poison")   : 0,
    ("Water", "Psychic")  : 0,
    ("Water", "Rock")     : 1,
    ("Water", "Steel")    : 0,
    ("Water", "Water")    : -1
}

def type_logic(attackingPokemon, defendingPokemon):
    matchup = 0
    if ("Delta Stream" in attackingPokemon.ability):
        return True
    if ("Multitype" in attackingPokemon.ability or
        "Multitype" in defendingPokemon.ability or
        "RKS System" in attackingPokemon.ability or
        "RKS System" in defendingPokemon.ability):
        return False
    for x in attackingPokemon.type:
        if x:
            for y in defendingPokemon.type:
                if y:
                    if (("Levitate" in defendingPokemon.ability and "Ground" in x) or
                        ("Flash Fire" in defendingPokemon.ability and "Fire" in x) or
                        ("Water Bubble" in defendingPokemon.ability and "Fire" in x) or
                        ("Water Absorb" in defendingPokemon.ability and "Water" in x) or
                        ("Storm Drain" in defendingPokemon.ability and "Water" in x) or
                        ("Dry Skin" in defendingPokemon.ability and "Water" in x) or
                        ("Lightningrod" in defendingPokemon.ability and "Electric" in x) or
                        ("Volt Absorb" in defendingPokemon.ability and "Electric" in x) or
                        ("Motor Drive" in defendingPokemon.ability and "Electric" in x) or
                        ("Sap Sipper" in defendingPokemon.ability and "Grass" in x) or
                        ("Desolate Land" in defendingPokemon.ability and "Water" in x) or
                        ("Primordial Sea" in defendingPokemon.ability and "Fire" in x) or
                        ("Prankster" in attackingPokemon.ability and "Dark" in y)):
                        matchup -= 1
                    elif (("Fluffy" in defendingPokemon.ability and "Fire" in x) or
                          ("Dry Skin" in defendingPokemon.ability and "Fire" in x) or
                          ("Steelworker" in attackingPokemon.ability and "Rock" in y) or
                          ("Steelworker" in attackingPokemon.ability and "Fairy" in y) or
                          ("Steelworker" in attackingPokemon.ability and "Ice" in y)):
                        matchup += 1
                    elif ("Scrappy" in attackingPokemon.ability and "Ghost" in y):
                        matchup += 0
                    elif (("Tinted Lens" in attackingPokemon.ability and "Bug" in x) and
                          ("Fairy" in y or "Fighting" in y or "Fire" in y or
                           "Flying" in y or "Ghost" in y or "Poison" in y or
                           "Steel" in y)):
                        matchup += 0
                    elif (("Tinted Lens" in attackingPokemon.ability and "Flying" in x) and
                          ("Electric" in y or "Rock" in y or "Steel" in y)):
                        matchup += 0
                    elif (("Tinted Lens" in attackingPokemon.ability and "Normal" in x) and
                          ("Rock" in y or "Steel" in y)):
                        matchup += 0
                    elif (("Tinted Lens" in attackingPokemon.ability and "Poison" in x) and
                          ("Ghost" in y or "Ground" in y or "Poison" in y or
                           "Rock" in y)):
                        matchup += 0
                    elif (("Tinted Lens" in attackingPokemon.ability and "Psychic" in x) and
                          ("Psychic" in y or "Steel" in y)):
                        matchup += 0
                    else:
                        matchup += TypeChart[(x, y)]
    if matchup > 0:
        return True
    else:
        return False

ALL_POKEMON = []
ABILITIES = {}
MEGA_STONES = []
Z_CRYSTALS = []
BERRIES = []

class Pokemon:
    def __init__(self, row):
        self.name = row[0]
        self.dex = row[1]
        self.type = [row[2], row[3]]
        self.tier = row[4]
        self.rarity = row[5]
        self.tag = row[6]
        self.item = row[7]
        self.ability = row[8]
        self.evSpread = row[9]
        self.nature = row[10]
        self.ivSpread = row[11]
        self.moves = [row[12], row[13], row[14], row[15]]
        # statistics
        self.generated_draft = row[17]
        self.generated_nemesis = row[18]
        self.generated_random = row[19]
        self.generated_total = row[20]
        self.picked_draft = row[21]
        self.picked_nemesis = row[22]
        self.picked_total = row[23]
        self.banned_total = row[24]

with open('main_database.csv', 'r') as fileName:
    reader = csv.reader(fileName)
    next(reader, None)
    for row in reader:
        ALL_POKEMON.append(Pokemon(row))

with open('Abilities.csv', 'r') as fileName:
    reader = csv.reader(fileName)
    for row in reader:
        ABILITIES[row[0]] = [row[x] for x in range(1,4) if row[x] != '']

with open('Items.csv', 'r') as fileName:
    reader = csv.reader(fileName)
    for row in reader:
        if 'ite' in row[0] and (row[0] != 'Eviolite' or row[0] != 'White Herb'):
            MEGA_STONES.append(row[0])
        if 'ium Z' in row[0]:
            Z_CRYSTALS.append(row[0])
        if 'Berry' in row[0] and row[0] != 'Berry Juice':
            BERRIES.append(row[0])
