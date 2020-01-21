import os
import math
import sys
import random

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

attack_dex = {'Flamethrower' : ('fire', 'special', 90),
              'Tackle' : ('normal', 'physical', 40),
              'Agility' : ('psychic', 'status', 0),
              'Crabhammer' : ('water', 'physical', 100),
              'Branch Poke' : ('grass', 'physical', 40)}

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


def get_stat(pokemon_set, stat):
    if stat in pokemon_set.ev_spread:
        stat_index = pokemon_set.ev_spread.find(stat) - 2
        if stat_index - 1 >= 0:
            if stat_index - 2 >= 0:
                if pokemon_set.ev_spread[stat_index - 2].isnumeric():
                    atk_ev = int(pokemon_set.ev_spread[stat_index-2:stat_index+1])
                elif pokemon_set.ev_spread[stat_index - 1].isnumeric():
                    atk_ev = int(pokemon_set.ev_spread[stat_index-1:stat_index+1])
                else:
                    atk_ev = int(pokemon_set.ev_spread[stat_index])
            else:
                if pokemon_set.ev_spread[stat_index - 1].isnumeric():
                    atk_ev = int(pokemon_set.ev_spread[stat_index-1:stat_index+1])
                else:
                    atk_ev = int(pokemon_set.ev_spread[stat_index])
        else:
            atk_ev = int(pokemon_set.ev_spread[stat_index])
    else:
        atk_ev = 0
    return atk_ev

def get_nature_multiplier(pokemon_set, category):
    #FIX HERE PLEASE
    if nature_dex[pokemon_set.nature]:
        print(nature_dex[pokemon_set.nature])
        if ((nature_dex[pokemon_set.nature][0] == 'attack' and category == 'physical') or
            (nature_dex[pokemon_set.nature][0] == 'spattack' and category == 'special')):
            multiplier = 1.1
        elif ((nature_dex[pokemon_set.nature][1] == 'attack' and category == 'physical') or
              (nature_dex[pokemon_set.nature][1] == 'spattack' and category == 'special')):
            multiplier = 0.9
        else:
            multiplier = 1.0
    else:
        multiplier = 1.0
    return multiplier

def damage_calc(attacking_pokemon, defending_pokemon, attack):
    atk_level = attacking_pokemon.level
    def_level = defending_pokemon.level
    if attack_dex[attack][1] == 'physical':
        if 'Atk' in attacking_pokemon.iv_spread:
            stat_index = attacking_pokemon.iv_spread.find('Atk') - 2
            if stat_index - 1 >= 0:
                if attacking_pokemon.iv_spread[stat_index - 1].isnumeric():
                    atk_iv = int(attacking_pokemon.iv_spread[stat_index-1:stat_index+1])
                else:
                    atk_iv = int(attacking_pokemon.iv_spread[stat_index])
            else:
                atk_iv = int(attacking_pokemon.iv_spread[0])
        else:
            atk_iv = 31
        # some special cases
        atk_base_stat = attacking_pokemon.pokemon.base_attack
        atk_ev = get_stat(attacking_pokemon, 'Atk')
        atk_nature = get_nature_multiplier(attacking_pokemon, 'physical')

        if 'Def' in defending_pokemon.iv_spread:
            stat_index = defending_pokemon.iv_spread.find('Def') - 2
            if stat_index - 1 >= 0:
                if defending_pokemon.iv_spread[stat_index - 1].isnumeric():
                    def_iv = int(defending_pokemon.iv_spread[stat_index-1:stat_index+1])
                else:
                    def_iv = int(defending_pokemon.iv_spread[stat_index])
            else:
                def_iv = int(defending_pokemon.iv_spread[0])
        else:
            def_iv = 31
        def_base_stat = defending_pokemon.pokemon.base_defense
        def_ev = get_stat(defending_pokemon, 'Def')
        def_nature = get_nature_multiplier(defending_pokemon, 'physical')

    elif attack_dex[attack][1] == 'special':
        atk_iv = 31
        atk_base_stat = attacking_pokemon.pokemon.base_spattack
        atk_ev = get_stat(attacking_pokemon, 'SpA')
        atk_nature = get_nature_multiplier(attacking_pokemon, 'special')

        if 'SpD' in defending_pokemon.iv_spread:
            stat_index = defending_pokemon.iv_spread.find('SpD') - 2
            if stat_index - 1 >= 0:
                if defending_pokemon.iv_spread[stat_index - 1].isnumeric():
                    def_iv = int(defending_pokemon.iv_spread[stat_index-1:stat_index+1])
                else:
                    def_iv = int(defending_pokemon.iv_spread[stat_index])
            else:
                def_iv = int(defending_pokemon.iv_spread[0])
        else:
            def_iv = 31
        def_base_stat = defending_pokemon.pokemon.base_spdefense
        def_ev = get_stat(defending_pokemon, 'SpD')
        def_nature = get_nature_multiplier(defending_pokemon, 'special')
    else:
        return 0

    attack_stat = math.floor(math.floor(((2 * atk_base_stat + atk_iv + math.floor(atk_ev / 4)) * atk_level) / 100 + 5) * atk_nature)
    attack_power = attack_dex[attack][2]
    attacking_type = [attack_dex[attack][0]]


    defense_stat = math.floor(math.floor(((2 * def_base_stat + def_iv + math.floor(def_ev / 4)) * def_level) / 100 + 5) * def_nature)
    if attack_dex[attack][0].capitalize() in attacking_pokemon.type:
        STAB = 1.5
    else:
        STAB = 1.0
    if len(defending_pokemon.type) > 1:
        effectiveness = TypeChart[(attack_dex[attack][0].capitalize(), defending_pokemon.type[0])] * TypeChart[(attack_dex[attack][0].capitalize(), defending_pokemon.type[1])]
    else:
        effectiveness = TypeChart[(attack_dex[attack][0].capitalize(), defending_pokemon.type[0])]
    damage_rolls = []
    print(def_nature)
    for RandomNumber in RandomNumbers:
        damage_rolls.append(round(((((2 * atk_level / 5 + 2) * attack_stat * attack_power / defense_stat) / 50) + 2) * STAB * effectiveness * RandomNumber))
    return damage_rolls

#testing
#open a pokemon file
import pandas as pd
from pandas import ExcelFile

pokedex = pd.ExcelFile(os.path.join(os.path.dirname(os.path.realpath(__file__)),
    'data', 'Pokedex.xlsx'))
pokemon_list = {}
for i in ['4', '99', '810']:
    xl_pkmn = pd.read_excel(pokedex, i)
    pokemon_list[xl_pkmn['name'].values[0]] = Pokemon(name=xl_pkmn['name'].values[0],
                                                      nat_dex=xl_pkmn['nat_dex'].values[0],
                                                      type=xl_pkmn['type'].tolist(),
                                                      abilities=xl_pkmn['abilities'].tolist(),
                                                      weight=xl_pkmn['weight'].values[0],
                                                      base_stats=xl_pkmn['base_stats'].tolist(),
                                                      can_dynamax=xl_pkmn['dynamax'].values[0],
                                                      can_gigantimax=xl_pkmn['gigantimax'].values[0],
                                                      attacks=xl_pkmn['attacks'].tolist())
def get_pokemon(i):
    if i == 0:
        return pokemon_list['Charmander']
    if i == 1:
        return pokemon_list['Kingler']

database = pd.read_excel(pd.ExcelFile(os.path.join(os.path.dirname(os.path.realpath(__file__)),
    'data', 'database.xlsx')), 'Sheet1')
sets = []
for i in range(2):
    sets.append(PokemonSet(get_pokemon(i), database['nat_dex'].values[i], [database['type1'].values[i], database['type2'].values[i]],
                           database['usage_tier'].values[i], database['tags'].values[i], database['item'].values[i],
                           database['ability'].values[i], database['ev_spread'].values[i], database['nature'].values[i],
                           database['iv_spread'].values[i], [database['move1'].values[i], database['move2'].values[i], database['move3'].values[i], database['move4'].values[i]]))

damage_rolls = damage_calc(sets[0], sets[1], 'Flamethrower')
sets[0].print_set()
sets[1].print_set()
print("Charmander uses Flamethrower vs. Kingler:")
print(damage_rolls)
