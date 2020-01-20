import os
import math

# we're defining the pokemon's traits here.
class Pokemon:
    def __init__(self, name=None, nat_dex=None, type=None, abilities=None,
                 weight=None, base_stats=None, can_dynamax=True,
                 can_gigantimax=False, attacks=None):
        self.name = name.casefold()
        self.nat_dex = str(int(nat_dex))
        self.type = [x for x in type if str(x) != 'nan']
        self.abilities = [x for x in abilities if str(x) != 'nan']
        self.weight = weight
        self.base_hp = base_stats[0]
        self.base_attack = base_stats[1]
        self.base_defense = base_stats[2]
        self.base_spattack = base_stats[3]
        self.base_spdefense = base_stats[4]
        self.base_speed = base_stats[5]
        self.can_dynamax = can_dynamax
        self.can_gigantimax = can_gigantimax
        self.attacks = attacks

    def print_info(self):
        print('Name: ' + self.name)
        print('Nat Dex: #' + self.nat_dex)
        if len(self.type) > 1:
            print('Type: %s / %s' %(self.type[0], self.type[1]))
        else:
            print('Type: ' + self.type[0])
        ability_list = ', '.join(self.abilities)
        print('Abilities: ' + ability_list)
        print('Weight: ' + str(self.weight) + 'kg')
        print('Stats\n[HP / Atk / Def / SpA / SpD / Spe]')
        base_stats = [str(int(self.base_hp)), str(int(self.base_attack)), str(int(self.base_defense)),
                      str(int(self.base_spattack)), str(int(self.base_spdefense)), str(int(self.base_speed))]
        print('[' + ' / '.join(base_stats) + ']')
        print('Can Dynamax? ' + self.can_dynamax)
        print('Can Gigantimax? ' + self.can_gigantimax)
        print('Attacks:')
        for attack in self.attacks:
            print('  ' + attack)

# we're reading in the database sets here.
class PokemonSet:
    def __init__(self, pokemon, dex, type, usage_tier, tags, item, ability,
                 ev_spread, nature, iv_spread, moves, dynamax=False,
                 gigantimax=False, level=100):
        self.name = pokemon.name.casefold()
        if dex != pokemon.nat_dex:
            sys.exit('Database has incorrect dex #.')
        self.dex = dex
        if type != pokemon.type:
            sys.exit('Database has incorrect type(s).')
        self.type = type
        self.item = item
        self.ability = ability
        self.level = level
        self.ev_spread = ev_spread
        self.nature = nature
        self.iv_spread = iv_spread

        self.usage_tier = usage_tier if usage_tier else ''
        self.tags = tags

        self.internal_name = pokemon.name.casefold()
        if dynamax:
            self.internal_name += '-dy.png'
        if gigantimax:
            if dynamax:
                self.internal_name = pokemon.name.casefold()
            self.internal_name += '-gi.png'
        self.icon_path = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), 'media', 'SwSh', self.internal_name)

#testing
#open a pokemon file
import pandas as pd
from pandas import ExcelFile

pokedex = pd.ExcelFile(os.path.join(os.path.dirname(os.path.realpath(__file__)),
    'data', 'Pokedex.xlsx'))
xl_pkmn = pd.read_excel(pokedex, 'Charmander')

test_pokemon = Pokemon(name=xl_pkmn['name'].values[0],
                       nat_dex=xl_pkmn['nat_dex'].values[0],
                       type=xl_pkmn['type'].tolist(),
                       abilities=xl_pkmn['abilities'].tolist(),
                       weight=xl_pkmn['weight'].values[0],
                       base_stats=xl_pkmn['base_stats'].tolist(),
                       can_dynamax=xl_pkmn['dynamax'].values[0],
                       can_gigantimax=xl_pkmn['gigantimax'].values[0],
                       attacks=xl_pkmn['attacks'].tolist())

test_pokemon.print_info()
