import os
import math
import sys
import random
import pandas as pd
from pandas import ExcelFile

TypeChart = {
    ('Bug', 'Bug')      : 1.0,
    ('Bug', 'Dark')     : 2.0,
    ('Bug', 'Dragon')   : 1.0,
    ('Bug', 'Electric') : 1.0,
    ('Bug', 'Fairy')    : 0.5,
    ('Bug', 'Fighting') : 0.5,
    ('Bug', 'Fire')     : 0.5,
    ('Bug', 'Flying')   : 0.5,
    ('Bug', 'Ghost')    : 0.5,
    ('Bug', 'Grass')    : 2.0,
    ('Bug', 'Ground')   : 1.0,
    ('Bug', 'Ice')      : 1.0,
    ('Bug', 'Normal')   : 1.0,
    ('Bug', 'Poison')   : 0.5,
    ('Bug', 'Psychic')  : 2.0,
    ('Bug', 'Rock')     : 1.0,
    ('Bug', 'Steel')    : 0.5,
    ('Bug', 'Water')    : 1.0,

    ('Dark', 'Bug')      : 1.0,
    ('Dark', 'Dark')     : 0.5,
    ('Dark', 'Dragon')   : 1.0,
    ('Dark', 'Electric') : 1.0,
    ('Dark', 'Fairy')    : 0.5,
    ('Dark', 'Fighting') : 0.5,
    ('Dark', 'Fire')     : 1.0,
    ('Dark', 'Flying')   : 1.0,
    ('Dark', 'Ghost')    : 2.0,
    ('Dark', 'Grass')    : 1.0,
    ('Dark', 'Ground')   : 1.0,
    ('Dark', 'Ice')      : 1.0,
    ('Dark', 'Normal')   : 1.0,
    ('Dark', 'Poison')   : 1.0,
    ('Dark', 'Psychic')  : 2.0,
    ('Dark', 'Rock')     : 1.0,
    ('Dark', 'Steel')    : 1.0,
    ('Dark', 'Water')    : 1.0,

    ('Dragon', 'Bug')      : 1.0,
    ('Dragon', 'Dark')     : 1.0,
    ('Dragon', 'Dragon')   : 2.0,
    ('Dragon', 'Electric') : 1.0,
    ('Dragon', 'Fairy')    : 0.0,
    ('Dragon', 'Fighting') : 1.0,
    ('Dragon', 'Fire')     : 1.0,
    ('Dragon', 'Flying')   : 1.0,
    ('Dragon', 'Ghost')    : 1.0,
    ('Dragon', 'Grass')    : 1.0,
    ('Dragon', 'Ground')   : 1.0,
    ('Dragon', 'Ice')      : 1.0,
    ('Dragon', 'Normal')   : 1.0,
    ('Dragon', 'Poison')   : 1.0,
    ('Dragon', 'Psychic')  : 1.0,
    ('Dragon', 'Rock')     : 1.0,
    ('Dragon', 'Steel')    : 0.5,
    ('Dragon', 'Water')    : 1.0,

    ('Electric', 'Bug')      : 1.0,
    ('Electric', 'Dark')     : 1.0,
    ('Electric', 'Dragon')   : 0.5,
    ('Electric', 'Electric') : 0.5,
    ('Electric', 'Fairy')    : 1.0,
    ('Electric', 'Fighting') : 1.0,
    ('Electric', 'Fire')     : 1.0,
    ('Electric', 'Flying')   : 2.0,
    ('Electric', 'Ghost')    : 1.0,
    ('Electric', 'Grass')    : 0.5,
    ('Electric', 'Ground')   : 0.0,
    ('Electric', 'Ice')      : 1.0,
    ('Electric', 'Normal')   : 1.0,
    ('Electric', 'Poison')   : 1.0,
    ('Electric', 'Psychic')  : 1.0,
    ('Electric', 'Rock')     : 1.0,
    ('Electric', 'Steel')    : 1.0,
    ('Electric', 'Water')    : 2.0,

    ('Fairy', 'Bug')      : 1.0,
    ('Fairy', 'Dark')     : 2.0,
    ('Fairy', 'Dragon')   : 2.0,
    ('Fairy', 'Electric') : 1.0,
    ('Fairy', 'Fairy')    : 1.0,
    ('Fairy', 'Fighting') : 2.0,
    ('Fairy', 'Fire')     : 0.5,
    ('Fairy', 'Flying')   : 1.0,
    ('Fairy', 'Ghost')    : 1.0,
    ('Fairy', 'Grass')    : 1.0,
    ('Fairy', 'Ground')   : 1.0,
    ('Fairy', 'Ice')      : 1.0,
    ('Fairy', 'Normal')   : 1.0,
    ('Fairy', 'Poison')   : 0.5,
    ('Fairy', 'Psychic')  : 1.0,
    ('Fairy', 'Rock')     : 1.0,
    ('Fairy', 'Steel')    : 0.5,
    ('Fairy', 'Water')    : 1.0,

    ('Fighting', 'Bug')      : 0.5,
    ('Fighting', 'Dark')     : 2.0,
    ('Fighting', 'Dragon')   : 1.0,
    ('Fighting', 'Electric') : 1.0,
    ('Fighting', 'Fairy')    : 2.0,
    ('Fighting', 'Fighting') : 1.0,
    ('Fighting', 'Fire')     : 1.0,
    ('Fighting', 'Flying')   : 0.5,
    ('Fighting', 'Ghost')    : 0.0,
    ('Fighting', 'Grass')    : 1.0,
    ('Fighting', 'Ground')   : 1.0,
    ('Fighting', 'Ice')      : 2.0,
    ('Fighting', 'Normal')   : 2.0,
    ('Fighting', 'Poison')   : 0.5,
    ('Fighting', 'Psychic')  : 0.5,
    ('Fighting', 'Rock')     : 2.0,
    ('Fighting', 'Steel')    : 2.0,
    ('Fighting', 'Water')    : 1.0,

    ('Fire', 'Bug')      : 2.0,
    ('Fire', 'Dark')     : 1.0,
    ('Fire', 'Dragon')   : 0.5,
    ('Fire', 'Electric') : 1.0,
    ('Fire', 'Fairy')    : 1.0,
    ('Fire', 'Fighting') : 1.0,
    ('Fire', 'Fire')     : 0.5,
    ('Fire', 'Flying')   : 1.0,
    ('Fire', 'Ghost')    : 1.0,
    ('Fire', 'Grass')    : 2.0,
    ('Fire', 'Ground')   : 1.0,
    ('Fire', 'Ice')      : 2.0,
    ('Fire', 'Normal')   : 1.0,
    ('Fire', 'Poison')   : 1.0,
    ('Fire', 'Psychic')  : 1.0,
    ('Fire', 'Rock')     : 0.5,
    ('Fire', 'Steel')    : 2.0,
    ('Fire', 'Water')    : 0.5,

    ('Flying', 'Bug')      : 2.0,
    ('Flying', 'Dark')     : 1.0,
    ('Flying', 'Dragon')   : 1.0,
    ('Flying', 'Electric') : 0.5,
    ('Flying', 'Fairy')    : 1.0,
    ('Flying', 'Fighting') : 2.0,
    ('Flying', 'Fire')     : 1.0,
    ('Flying', 'Flying')   : 1.0,
    ('Flying', 'Ghost')    : 1.0,
    ('Flying', 'Grass')    : 2.0,
    ('Flying', 'Ground')   : 1.0,
    ('Flying', 'Ice')      : 1.0,
    ('Flying', 'Normal')   : 1.0,
    ('Flying', 'Poison')   : 1.0,
    ('Flying', 'Psychic')  : 1.0,
    ('Flying', 'Rock')     : 0.5,
    ('Flying', 'Steel')    : 0.5,
    ('Flying', 'Water')    : 1.0,

    ('Ghost', 'Bug')      : 1.0,
    ('Ghost', 'Dark')     : 0.5,
    ('Ghost', 'Dragon')   : 1.0,
    ('Ghost', 'Electric') : 1.0,
    ('Ghost', 'Fairy')    : 1.0,
    ('Ghost', 'Fighting') : 1.0,
    ('Ghost', 'Fire')     : 1.0,
    ('Ghost', 'Flying')   : 1.0,
    ('Ghost', 'Ghost')    : 2.0,
    ('Ghost', 'Grass')    : 1.0,
    ('Ghost', 'Ground')   : 1.0,
    ('Ghost', 'Ice')      : 1.0,
    ('Ghost', 'Normal')   : 0.0,
    ('Ghost', 'Poison')   : 1.0,
    ('Ghost', 'Psychic')  : 2.0,
    ('Ghost', 'Rock')     : 1.0,
    ('Ghost', 'Steel')    : 1.0,
    ('Ghost', 'Water')    : 1.0,

    ('Grass', 'Bug')      : 0.5,
    ('Grass', 'Dark')     : 1.0,
    ('Grass', 'Dragon')   : 0.5,
    ('Grass', 'Electric') : 1.0,
    ('Grass', 'Fairy')    : 1.0,
    ('Grass', 'Fighting') : 1.0,
    ('Grass', 'Fire')     : 0.5,
    ('Grass', 'Flying')   : 0.5,
    ('Grass', 'Ghost')    : 1.0,
    ('Grass', 'Grass')    : 0.5,
    ('Grass', 'Ground')   : 2.0,
    ('Grass', 'Ice')      : 1.0,
    ('Grass', 'Normal')   : 1.0,
    ('Grass', 'Poison')   : 0.5,
    ('Grass', 'Psychic')  : 1.0,
    ('Grass', 'Rock')     : 2.0,
    ('Grass', 'Steel')    : 0.5,
    ('Grass', 'Water')    : 2.0,

    ('Ground', 'Bug')      : 0.5,
    ('Ground', 'Dark')     : 1.0,
    ('Ground', 'Dragon')   : 1.0,
    ('Ground', 'Electric') : 2.0,
    ('Ground', 'Fairy')    : 1.0,
    ('Ground', 'Fighting') : 1.0,
    ('Ground', 'Fire')     : 2.0,
    ('Ground', 'Flying')   : 0.0,
    ('Ground', 'Ghost')    : 1.0,
    ('Ground', 'Grass')    : 0.5,
    ('Ground', 'Ground')   : 1.0,
    ('Ground', 'Ice')      : 1.0,
    ('Ground', 'Normal')   : 1.0,
    ('Ground', 'Poison')   : 2.0,
    ('Ground', 'Psychic')  : 1.0,
    ('Ground', 'Rock')     : 2.0,
    ('Ground', 'Steel')    : 2.0,
    ('Ground', 'Water')    : 1.0,

    ('Ice', 'Bug')      : 1.0,
    ('Ice', 'Dark')     : 1.0,
    ('Ice', 'Dragon')   : 2.0,
    ('Ice', 'Electric') : 1.0,
    ('Ice', 'Fairy')    : 1.0,
    ('Ice', 'Fighting') : 1.0,
    ('Ice', 'Fire')     : 0.5,
    ('Ice', 'Flying')   : 2.0,
    ('Ice', 'Ghost')    : 1.0,
    ('Ice', 'Grass')    : 2.0,
    ('Ice', 'Ground')   : 2.0,
    ('Ice', 'Ice')      : 0.5,
    ('Ice', 'Normal')   : 1.0,
    ('Ice', 'Poison')   : 1.0,
    ('Ice', 'Psychic')  : 1.0,
    ('Ice', 'Rock')     : 1.0,
    ('Ice', 'Steel')    : 0.5,
    ('Ice', 'Water')    : 0.5,

    ('Normal', 'Bug')      : 1.0,
    ('Normal', 'Dark')     : 1.0,
    ('Normal', 'Dragon')   : 1.0,
    ('Normal', 'Electric') : 1.0,
    ('Normal', 'Fairy')    : 1.0,
    ('Normal', 'Fighting') : 1.0,
    ('Normal', 'Fire')     : 1.0,
    ('Normal', 'Flying')   : 1.0,
    ('Normal', 'Ghost')    : 0.0,
    ('Normal', 'Grass')    : 1.0,
    ('Normal', 'Ground')   : 1.0,
    ('Normal', 'Ice')      : 1.0,
    ('Normal', 'Normal')   : 1.0,
    ('Normal', 'Poison')   : 1.0,
    ('Normal', 'Psychic')  : 1.0,
    ('Normal', 'Rock')     : 0.5,
    ('Normal', 'Steel')    : 0.5,
    ('Normal', 'Water')    : 1.0,

    ('Poison', 'Bug')      : 1.0,
    ('Poison', 'Dark')     : 1.0,
    ('Poison', 'Dragon')   : 1.0,
    ('Poison', 'Electric') : 1.0,
    ('Poison', 'Fairy')    : 2.0,
    ('Poison', 'Fighting') : 1.0,
    ('Poison', 'Fire')     : 1.0,
    ('Poison', 'Flying')   : 1.0,
    ('Poison', 'Ghost')    : 0.5,
    ('Poison', 'Grass')    : 2.0,
    ('Poison', 'Ground')   : 0.5,
    ('Poison', 'Ice')      : 1.0,
    ('Poison', 'Normal')   : 1.0,
    ('Poison', 'Poison')   : 0.5,
    ('Poison', 'Psychic')  : 1.0,
    ('Poison', 'Rock')     : 0.5,
    ('Poison', 'Steel')    : 0.0,
    ('Poison', 'Water')    : 1.0,

    ('Psychic', 'Bug')      : 1.0,
    ('Psychic', 'Dark')     : 0.0,
    ('Psychic', 'Dragon')   : 1.0,
    ('Psychic', 'Electric') : 1.0,
    ('Psychic', 'Fairy')    : 1.0,
    ('Psychic', 'Fighting') : 2.0,
    ('Psychic', 'Fire')     : 1.0,
    ('Psychic', 'Flying')   : 1.0,
    ('Psychic', 'Ghost')    : 1.0,
    ('Psychic', 'Grass')    : 1.0,
    ('Psychic', 'Ground')   : 1.0,
    ('Psychic', 'Ice')      : 1.0,
    ('Psychic', 'Normal')   : 1.0,
    ('Psychic', 'Poison')   : 2.0,
    ('Psychic', 'Psychic')  : 0.5,
    ('Psychic', 'Rock')     : 1.0,
    ('Psychic', 'Steel')    : 0.5,
    ('Psychic', 'Water')    : 1.0,

    ('Rock', 'Bug')      : 2.0,
    ('Rock', 'Dark')     : 1.0,
    ('Rock', 'Dragon')   : 1.0,
    ('Rock', 'Electric') : 1.0,
    ('Rock', 'Fairy')    : 1.0,
    ('Rock', 'Fighting') : 0.5,
    ('Rock', 'Fire')     : 2.0,
    ('Rock', 'Flying')   : 2.0,
    ('Rock', 'Ghost')    : 1.0,
    ('Rock', 'Grass')    : 1.0,
    ('Rock', 'Ground')   : 0.5,
    ('Rock', 'Ice')      : 2.0,
    ('Rock', 'Normal')   : 1.0,
    ('Rock', 'Poison')   : 1.0,
    ('Rock', 'Psychic')  : 1.0,
    ('Rock', 'Rock')     : 1.0,
    ('Rock', 'Steel')    : 0.5,
    ('Rock', 'Water')    : 1.0,

    ('Steel', 'Bug')      : 1.0,
    ('Steel', 'Dark')     : 1.0,
    ('Steel', 'Dragon')   : 1.0,
    ('Steel', 'Electric') : 0.5,
    ('Steel', 'Fairy')    : 2.0,
    ('Steel', 'Fighting') : 1.0,
    ('Steel', 'Fire')     : 0.5,
    ('Steel', 'Flying')   : 1.0,
    ('Steel', 'Ghost')    : 1.0,
    ('Steel', 'Grass')    : 1.0,
    ('Steel', 'Ground')   : 1.0,
    ('Steel', 'Ice')      : 2.0,
    ('Steel', 'Normal')   : 1.0,
    ('Steel', 'Poison')   : 1.0,
    ('Steel', 'Psychic')  : 1.0,
    ('Steel', 'Rock')     : 2.0,
    ('Steel', 'Steel')    : 0.5,
    ('Steel', 'Water')    : 0.5,

    ('Water', 'Bug')      : 1.0,
    ('Water', 'Dark')     : 1.0,
    ('Water', 'Dragon')   : 0.5,
    ('Water', 'Electric') : 1.0,
    ('Water', 'Fairy')    : 1.0,
    ('Water', 'Fighting') : 1.0,
    ('Water', 'Fire')     : 2.0,
    ('Water', 'Flying')   : 1.0,
    ('Water', 'Ghost')    : 1.0,
    ('Water', 'Grass')    : 0.5,
    ('Water', 'Ground')   : 2.0,
    ('Water', 'Ice')      : 1.0,
    ('Water', 'Normal')   : 1.0,
    ('Water', 'Poison')   : 1.0,
    ('Water', 'Psychic')  : 1.0,
    ('Water', 'Rock')     : 2.0,
    ('Water', 'Steel')    : 1.0,
    ('Water', 'Water')    : 0.5
}

RandomNumbers = [x/100 for x in range(85, 101)]

nature_dex = {'Adamant' : ('attack', 'spattack'),
              'Bashful' : None,
              'Bold'    : ('defense', 'attack'),
              'Brave'   : ('attack', 'speed'),
              'Calm'    : ('spdefense', 'attack'),
              'Careful' : ('spdefense', 'spattack'),
              'Docile'  : None,
              'Gentle'  : ('spdefense', 'defense'),
              'Hardy'   : None,
              'Hasty'   : ('speed', 'defense'),
              'Impish'  : ('defense', 'spattack'),
              'Jolly'   : ('speed' 'spattack'),
              'Lax'     : ('defense', 'spdefense'),
              'Lonely'  : ('attack', 'defense'),
              'Mild'    : ('spattack', 'defense'),
              'Modest'  : ('spattack', 'attack'),
              'Naive'   : ('speed', 'spdefense'),
              'Naughty' : ('attack', 'spdefense'),
              'Quiet'   : ('spattack', 'speed'),
              'Quirky'  : None,
              'Rash'    : ('spattack', 'spdefense'),
              'Relaxed' : ('defense', 'speed'),
              'Sassy'   : ('spdefense', 'speed'),
              'Serious' : None,
              'Timid'   : ('speed', 'attack')}

stat_conversion = {'atk' : 'attack',
                   'def' : 'defense',
                   'spa' : 'spattack',
                   'spd' : 'spdefense',
                   'spe' : 'speed',
                   1 : 'attack',
                   2 : 'defense',
                   3 : 'spattack',
                   4 : 'spdefense',
                   5 : 'speed'}

attack_item_file = pd.ExcelFile(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'attacks_items.xlsx'))
attack_dex = {}
item_dex = []
xl_atk = pd.read_excel(attack_item_file, 'Attacks')
xl_item = pd.read_excel(attack_item_file, 'Items')
for i in range(724):
    if str(xl_atk['power'].values[i]) == '*':
        attack_dex[str(xl_atk['name'].values[i])] = (str(xl_atk['type'].values[i]), str(xl_atk['category'].values[i]), str(xl_atk['power'].values[i]))
    else:
        attack_dex[str(xl_atk['name'].values[i])] = (str(xl_atk['type'].values[i]), str(xl_atk['category'].values[i]), int(xl_atk['power'].values[i]))
for i in range(145):
    item_dex.append(str(xl_item['name'].values[i]))

class Pokemon:
    def __init__(self, name=None, nat_dex=None, type=None, abilities=None,
                 weight=None, base_stats=None, can_dynamax=True,
                 can_gigantimax=False, attacks=None):
        self.name = name.casefold()
        self.nat_dex = str(int(nat_dex))
        self.type = [x for x in type if str(x) != 'nan']
        self.abilities = [x for x in abilities if str(x) != 'nan']
        self.weight = weight
        self.base_hp = int(base_stats[0])
        self.base_attack = int(base_stats[1])
        self.base_defense = int(base_stats[2])
        self.base_spattack = int(base_stats[3])
        self.base_spdefense = int(base_stats[4])
        self.base_speed = int(base_stats[5])
        self.can_dynamax = can_dynamax
        self.can_gigantimax = can_gigantimax
        self.attacks = [x for x in attacks if str(x) != 'nan']

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

class PokemonSet:
    def __init__(self, pokemon, dex, type, usage_tier, tags, item, ability,
                 ev_spread, nature, iv_spread, moves, dynamax=False,
                 gigantimax=False, level=100):
        self.pokemon = pokemon
        self.name = pokemon.name.casefold().capitalize()
        if str(dex) != pokemon.nat_dex:
            sys.exit('Database has incorrect dex #.')
        self.dex = str(int(dex))
        ctype = [x for x in type if str(x) != 'nan']
        if ctype != pokemon.type:
            sys.exit('Database has incorrect type(s).')
        self.type = ctype
        if str(item) != 'nan':
            self.item = item
        else:
            self.item = ''
        self.ability = ability
        if usage_tier == 'LC' or usage_tier == 'LC Uber':
            self.level = 5
        else:
            self.level = level
        self.ev_spread = ev_spread
        self.nature = nature
        if str(iv_spread) != 'nan':
            self.iv_spread = iv_spread
        else:
            self.iv_spread = ''
        self.usage_tier = usage_tier if usage_tier else ''
        self.tags = tags
        self.moves = [x for x in moves if str(x) != 'nan']

        self.internal_name = pokemon.name.casefold()
        if dynamax:
            self.internal_name += '-dy.png'
        if gigantimax:
            if dynamax:
                self.internal_name = pokemon.name.casefold()
            self.internal_name += '-gi.png'
        self.icon_path = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), 'media', 'SwSh', self.internal_name)

    def print_set(self):
        if self.item:
            print(self.name + ' @ ' + self.item)
        else:
            print(self.name)
        print('Ability: ' + self.ability)
        print('EVs: ' + self.ev_spread)
        print(self.nature + ' Nature')
        if self.iv_spread:
            print('IVs: ' + self.iv_spread)
        for move in self.moves:
            print('- ' + move)

def get_stat(pkmn_name, stat_name, iv, ev, nature, level='100'):
    # Note: stat_name can be a name or an index, and all other params are casted for safety.
    stat = str(stat_name)
    if ev.replace('+', '').replace('-', '').replace(' ', '') == '':
        ev = 0
    print(ev)
    if stat.casefold() == 'hp' or stat == '0':
        if pkmn_name.casefold() == 'shedinja':
            return 1
        base_stat = POKEMON_LIST[pkmn_name].base_hp
        value = math.floor((((2 * int(base_stat) + int(iv) + math.floor(int(ev) / 4)) * int(level)) / 100)) + int(level) + 10
    else:
        if stat.casefold() == 'atk' or stat.casefold() == 'attack' or stat == '1':
            stat = 'attack'
            base_stat = POKEMON_LIST[pkmn_name].base_attack
        elif stat.casefold() == 'def' or stat.casefold() == 'defense' or stat == '2':
            stat = 'defense'
            base_stat = POKEMON_LIST[pkmn_name].base_defense
        elif stat.casefold() == 'spa' or stat.casefold() == 'spattack' or stat == '3':
            stat = 'spattack'
            base_stat = POKEMON_LIST[pkmn_name].base_spattack
        elif stat.casefold() == 'spd' or stat.casefold() == 'spdefense' or stat == '4':
            stat = 'spdefense'
            base_stat = POKEMON_LIST[pkmn_name].base_spdefense
        elif stat.casefold() == 'spe' or stat.casefold() == 'speed' or stat == '5':
            stat = 'speed'
            base_stat = POKEMON_LIST[pkmn_name].base_speed
        else:
            print('Unknown parameter stat_name:', stat_name)
            return -1
        if nature_dex[nature]:
            if nature_dex[nature][0] == stat:
                nature_multiplier = 1.1
            elif nature_dex[nature][1] == stat:
                nature_multiplier = 0.9
            else:
                nature_multiplier = 1.0
        else:
            nature_multiplier = 1.0
        value = math.floor(math.floor((((2 * int(base_stat) + int(iv) + math.floor(int(ev) / 4)) * int(level)) / 100) + 5) * nature_multiplier)
    return int(value)

def _extract_iv_stat(pokemon_set, stat):
    if stat in pokemon_set.iv_spread:
        stat_index = pokemon_set.iv_spread.find(stat) - 2
        if stat_index - 1 >= 0:
            if pokemon_set.iv_spread[stat_index-1].isnumeric():
                return int(pokemon_set.iv_spread[stat_index-1:stat_index+1])
            else:
                return int(pokemon_set.iv_spread[stat_index])
        else:
            return int(pokemon_set.iv_spread[0])
    else:
        return 31

def _extract_ev_stat(pokemon_set, stat):
    if stat in pokemon_set.ev_spread:
        stat_index = pokemon_set.ev_spread.find(stat) - 2
        if stat_index - 1 >= 0:
            if stat_index - 2 >= 0:
                if pokemon_set.ev_spread[stat_index - 2].isnumeric():
                    value = int(pokemon_set.ev_spread[stat_index-2:stat_index+1])
                elif pokemon_set.ev_spread[stat_index - 1].isnumeric():
                    value = int(pokemon_set.ev_spread[stat_index-1:stat_index+1])
                else:
                    value = int(pokemon_set.ev_spread[stat_index])
            else:
                if pokemon_set.ev_spread[stat_index - 1].isnumeric():
                    value = int(pokemon_set.ev_spread[stat_index-1:stat_index+1])
                else:
                    value = int(pokemon_set.ev_spread[stat_index])
        else:
            value = int(pokemon_set.ev_spread[stat_index])
    else:
        value = 0
    return value

def _get_nature_multiplier(pokemon_set, stat):
    if pokemon_set.nature not in nature_dex.keys():
        sys.exit('Set has invalid Nature.')
    if nature_dex[pokemon_set.nature]:
        if nature_dex[pokemon_set.nature][0] == stat:
            multiplier = 1.1
        elif nature_dex[pokemon_set.nature][1] == stat:
            multiplier = 0.9
        else:
            multiplier = 1.0
    else:
        multiplier = 1.0
    return multiplier

def _get_other_multipliers(attacking_pokemon, defending_pokemon, attack, critical, effectiveness, aurora_veil, light_screen, reflect):
    other = 1.0
    category = attack_dex[attack][1]
    attack_type = attack_dex[attack][0]

    # abilities
    if attacking_pokemon.ability == 'Tinted Lens' and effectiveness < 1.0:
        other *= 2.0
    # fix this in the future
    if attacking_pokemon.ability == 'Sniper' and critical > 1.0:
        other *= 1.5
    if attacking_pokemon.ability == 'Mold Breaker' or attacking_pokemon.ability == 'Teravolt' or attacking_pokemon.ability == 'Turboblaze':
        pass
    if attacking_pokemon.ability != 'Mold Breaker':
        if defending_pokemon.ability == 'Water Bubble' and attacking_type == 'Fire':
            other *= 0.5
        if ((defending_pokemon.ability == 'Levitate' and (attack != 'Thousand Arrows' or defending_pokemon.item != 'Iron Ball')) or
            (defending_pokemon.ability == 'Damp' and (attack == 'Explosion' or attack == 'Self-Destruct')) or
            ((defending_pokemon.ability == 'Dry Skin' or defending_pokemon.ability == 'Storm Drain') and attacking_type == 'water') or
            ((defending_pokemon.ability == 'Motor Drive' or defending_pokemon.ability == 'Lightning Rod' or defending_pokemon.ability == 'Volt Absorb') and attacking_type == 'electric') or
            (defending_pokemon.ability == 'Flash Fire' and attacking_type == 'fire') or
            (defending_pokemon.ability == 'Sap Sipper' and attacking_type == 'grass')):
            return 0.0
        if ((defending_pokemon.ability == 'Filter' or defending_pokemon.ability == 'Prism Armor' or defending_pokemon.ability == 'Solid Rock') and effectiveness > 1.0):
            other *= 0.75
        if defending_pokemon.ability == 'Water Bubble' and attacking_type == 'Fire':
            other *= 0.5
        if defending_pokemon.ability == 'Thick Fat' and (attacking_type == 'Fire' or attacking_type == 'Ice'):
            other *= 0.5
        if defending_pokemon.ability == 'Punk Rock' and attack in ['Boomburst', 'Bug Buzz', 'Chatter', 'Clanging Scales',
                                                                   'Disarming Voice', 'Echoed Voice', 'Hyper Voice', 'Overdrive',
                                                                   'Relic Song', 'Round', 'Snarl', 'Snore', 'Uproar']:
            other *= 0.5

        # assume full HP
        if defending_pokemon.ability == 'Multiscale' or defending_pokemon.ability == 'Shadow Shield':
            other *= 0.5
        if defending_pokemon.ability == 'Fluffy':
            if category== 'special' and attack_type != 'fire':
                other *= 2.0
            elif category == 'physical' and attack_type != 'fire':
                other *= 0.5
            else:
                other *= 1.0
        if defending_pokemon.ability == 'Wonder Guard':
            if effectiveness > 1.0:
                other *= 1.0
            else:
                other *= 0.0

    # items
    if attacking_pokemon.item == 'Expert Belt' and effectiveness > 1.0:
        other *= 1.2
    if attacking_pokemon.item == 'Life Orb':
        other *= 1.3
    if ((defending_pokemon.item == 'Babiri Berry' and attack_type == 'steel' and effectiveness > 1.0) or
        (defending_pokemon.item == 'Charti Berry' and attack_type == 'rock' and effectiveness > 1.0) or
        (defending_pokemon.item == 'Chilan Berry' and attack_type == 'normal') or
        (defending_pokemon.item == 'Chople Berry' and attack_type == 'fighting' and effectiveness > 1.0) or
        (defending_pokemon.item == 'Coba Berry' and attack_type == 'flying' and effectiveness > 1.0) or
        (defending_pokemon.item == 'Colbur Berry' and attack_type == 'dark' and effectiveness > 1.0) or
        (defending_pokemon.item == 'Haban Berry' and attack_type == 'dragon' and effectiveness > 1.0) or
        (defending_pokemon.item == 'Kasib Berry' and attack_type == 'ghost' and effectiveness > 1.0) or
        (defending_pokemon.item == 'Kebia Berry' and attack_type == 'poison' and effectiveness > 1.0) or
        (defending_pokemon.item == 'Occa Berry' and attack_type == 'fire' and effectiveness > 1.0) or
        (defending_pokemon.item == 'Passho Berry' and attack_type == 'water' and effectiveness > 1.0) or
        (defending_pokemon.item == 'Payapa Berry' and attack_type == 'psychic' and effectiveness > 1.0) or
        (defending_pokemon.item == 'Rindo Berry' and attack_type == 'grass' and effectiveness > 1.0) or
        (defending_pokemon.item == 'Roseli Berry' and attack_type == 'fairy' and effectiveness > 1.0) or
        (defending_pokemon.item == 'Shuca Berry' and attack_type == 'ground' and effectiveness > 1.0) or
        (defending_pokemon.item == 'Tanga Berry' and attack_type == 'bug' and effectiveness > 1.0) or
        (defending_pokemon.item == 'Wacan Berry' and attack_type == 'electric' and effectiveness > 1.0) or
        (defending_pokemon.item == 'Yache Berry' and attack_type == 'ice' and effectiveness > 1.0)):
        other *= 0.5
    if aurora_veil:
        other *= 0.5
    if light_screen and category == 'special':
        other *= 0.5
    if reflect and category == 'physical':
        other *= 0.5
    return other

def damage_calc(attacking_pokemon, defending_pokemon, attack, critical=False, weather_condition='clear', burned=False, aurora_veil=False, light_screen=False, reflect=False):
    atk_level = attacking_pokemon.level
    atk_category = attack_dex[attack][1].casefold()
    if atk_category == 'physical':
        # some special cases missing
        atk_base_stat = attacking_pokemon.pokemon.base_attack
        atk_iv = _extract_iv_stat(attacking_pokemon, 'Atk')
        atk_ev = _extract_ev_stat(attacking_pokemon, 'Atk')
        atk_nature = _get_nature_multiplier(attacking_pokemon, 'attack')

        def_base_stat = defending_pokemon.pokemon.base_defense
        def_iv = _extract_iv_stat(defending_pokemon, 'Def')
        def_ev = _extract_ev_stat(defending_pokemon, 'Def')
        def_nature = _get_nature_multiplier(defending_pokemon, 'defense')

    elif atk_category == 'special':
        atk_base_stat = attacking_pokemon.pokemon.base_spattack
        atk_iv = 31 # assumes 31 IVs
        atk_ev = _extract_ev_stat(attacking_pokemon, 'SpA')
        atk_nature = _get_nature_multiplier(attacking_pokemon, 'spattack')

        def_base_stat = defending_pokemon.pokemon.base_spdefense
        def_iv = _extract_iv_stat(defending_pokemon, 'SpD')
        def_ev = _extract_ev_stat(defending_pokemon, 'SpD')
        def_nature = _get_nature_multiplier(defending_pokemon, 'spdefense')
    else:
        return [0 for i in range(15)]

    attack_stat = math.floor(math.floor(((2 * atk_base_stat + atk_iv + math.floor(atk_ev / 4)) * atk_level) / 100 + 5) * atk_nature)
    attack_power = attack_dex[attack][2]
    attacking_type = [attack_dex[attack][0]]

    defense_stat = math.floor(math.floor(((2 * def_base_stat + def_iv + math.floor(def_ev / 4)) * defending_pokemon.level) / 100 + 5) * def_nature)

    # check for STAB
    if attack_dex[attack][0].capitalize() in attacking_pokemon.type:
        STAB = 1.5
    else:
        STAB = 1.0

    # check for Effectiveness
    if len(defending_pokemon.type) > 1:
        effectiveness = TypeChart[(attack_dex[attack][0].capitalize(), defending_pokemon.type[0])] * TypeChart[(attack_dex[attack][0].capitalize(), defending_pokemon.type[1])]
    else:
        effectiveness = TypeChart[(attack_dex[attack][0].capitalize(), defending_pokemon.type[0])]

    other = _get_other_multipliers(attacking_pokemon, defending_pokemon, attack, critical, effectiveness, aurora_veil, light_screen, reflect)

    # weather toggle
    if weather_condition == 'sun':
        if attack_dex[attack][0] == 'fire':
            weather = 1.5
        elif attack_dex[attack][0] == 'water':
            weather = 0.5
        else:
            weather = 1.0
    elif weather_condition == 'rain':
        if attack_dex[attack][0] == 'water':
            weather = 1.5
        elif attack_dex[attack][0] == 'fire':
            weather = 0.5
        else:
            weather = 1.0
    else:
        weather = 1.0 # clear weather assumed

    # burn toggle
    if burned and attacking_pokemon.ability != 'Guts':
        burn = 0.5
    else:
        burn = 1.0

    # crit toggle
    if critical and defending_pokemon.ability != 'Battle Armor':
        crit = 1.5
    else:
        crit = 1.0

    damage_rolls = []
    for RandomNumber in RandomNumbers:
        modifiers = STAB * weather * burn * effectiveness * crit * RandomNumber * other
        damage_rolls.append(math.floor(((((2 * atk_level / 5 + 2) * attack_power * attack_stat / defense_stat) / 50) + 2) * modifiers))
    return damage_rolls

pokedex = pd.ExcelFile(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'Pokedex.xlsx'))
sheet_list = pokedex.sheet_names
POKEMON_LIST = {}
for i in sheet_list:
    xl_pkmn = pd.read_excel(pokedex, i)
    POKEMON_LIST[i] = Pokemon(name=xl_pkmn['name'].values[0],
                              nat_dex=xl_pkmn['nat_dex'].values[0],
                              type=xl_pkmn['type'].tolist(),
                              abilities=xl_pkmn['abilities'].tolist(),
                              weight=xl_pkmn['weight'].values[0],
                              base_stats=xl_pkmn['base_stats'].tolist(),
                              can_dynamax=xl_pkmn['dynamax'].values[0],
                              can_gigantimax=xl_pkmn['gigantamax'].values[0],
                              attacks=xl_pkmn['attacks'].tolist())

database = pd.read_excel(pd.ExcelFile(os.path.join(os.path.dirname(os.path.realpath(__file__)),
    'data', 'database.xlsx')), 'Sheet1')
sets = []
# for i in range(2):
#     sets.append(PokemonSet(get_pokemon(i), database['nat_dex'].values[i], [database['type1'].values[i], database['type2'].values[i]],
#                            database['usage_tier'].values[i], database['tags'].values[i], database['item'].values[i],
#                            database['ability'].values[i], database['ev_spread'].values[i], database['nature'].values[i],
#                            database['iv_spread'].values[i], [database['move1'].values[i], database['move2'].values[i], database['move3'].values[i], database['move4'].values[i]]))

# damage_rolls = damage_calc(sets[1], sets[0], 'Fishious Rend')
# print(damage_rolls)
