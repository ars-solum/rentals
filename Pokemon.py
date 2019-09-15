import csv
from datetime import date
import os
from PIL import Image, ImageTk
import random
from random import shuffle
import tkinter as tk
from tkinter.font import Font
from tkinter import ttk

ROOT = os.path.dirname(os.path.realpath(__file__))
COMMON = os.path.join(ROOT, 'media', 'Common')
IMG_PKMN_DIR = os.path.join(ROOT, 'media', 'pokemon')
PLAYER_DIR = os.path.join(ROOT, 'players')
DATA = os.path.join(ROOT, 'data')

TypeChart = {
    ('Bug', 'Bug')      : 0,
    ('Bug', 'Dark')     : 1,
    ('Bug', 'Dragon')   : 0,
    ('Bug', 'Electric') : 0,
    ('Bug', 'Fairy')    : -1,
    ('Bug', 'Fighting') : -1,
    ('Bug', 'Fire')     : -1,
    ('Bug', 'Flying')   : -1,
    ('Bug', 'Ghost')    : -1,
    ('Bug', 'Grass')    : 1,
    ('Bug', 'Ground')   : 0,
    ('Bug', 'Ice')      : 0,
    ('Bug', 'Normal')   : 0,
    ('Bug', 'Poison')   : -1,
    ('Bug', 'Psychic')  : 1,
    ('Bug', 'Rock')     : 0,
    ('Bug', 'Steel')    : -1,
    ('Bug', 'Water')    : 0,

    ('Dark', 'Bug')      : 0,
    ('Dark', 'Dark')     : -1,
    ('Dark', 'Dragon')   : 0,
    ('Dark', 'Electric') : 0,
    ('Dark', 'Fairy')    : -1,
    ('Dark', 'Fighting') : -1,
    ('Dark', 'Fire')     : 0,
    ('Dark', 'Flying')   : 0,
    ('Dark', 'Ghost')    : 1,
    ('Dark', 'Grass')    : 0,
    ('Dark', 'Ground')   : 0,
    ('Dark', 'Ice')      : 0,
    ('Dark', 'Normal')   : 0,
    ('Dark', 'Poison')   : 0,
    ('Dark', 'Psychic')  : 1,
    ('Dark', 'Rock')     : 0,
    ('Dark', 'Steel')    : 0,
    ('Dark', 'Water')    : 0,

    ('Dragon', 'Bug')      : 0,
    ('Dragon', 'Dark')     : 0,
    ('Dragon', 'Dragon')   : 1,
    ('Dragon', 'Electric') : 0,
    ('Dragon', 'Fairy')    : -1,
    ('Dragon', 'Fighting') : 0,
    ('Dragon', 'Fire')     : 0,
    ('Dragon', 'Flying')   : 0,
    ('Dragon', 'Ghost')    : 0,
    ('Dragon', 'Grass')    : 0,
    ('Dragon', 'Ground')   : 0,
    ('Dragon', 'Ice')      : 0,
    ('Dragon', 'Normal')   : 0,
    ('Dragon', 'Poison')   : 0,
    ('Dragon', 'Psychic')  : 0,
    ('Dragon', 'Rock')     : 0,
    ('Dragon', 'Steel')    : -1,
    ('Dragon', 'Water')    : 0,

    ('Electric', 'Bug')      : 0,
    ('Electric', 'Dark')     : 0,
    ('Electric', 'Dragon')   : -1,
    ('Electric', 'Electric') : -1,
    ('Electric', 'Fairy')    : 0,
    ('Electric', 'Fighting') : 0,
    ('Electric', 'Fire')     : 0,
    ('Electric', 'Flying')   : 1,
    ('Electric', 'Ghost')    : 0,
    ('Electric', 'Grass')    : -1,
    ('Electric', 'Ground')   : -1,
    ('Electric', 'Ice')      : 0,
    ('Electric', 'Normal')   : 0,
    ('Electric', 'Poison')   : 0,
    ('Electric', 'Psychic')  : 0,
    ('Electric', 'Rock')     : 0,
    ('Electric', 'Steel')    : 0,
    ('Electric', 'Water')    : 1,

    ('Fairy', 'Bug')      : 0,
    ('Fairy', 'Dark')     : 1,
    ('Fairy', 'Dragon')   : 1,
    ('Fairy', 'Electric') : 0,
    ('Fairy', 'Fairy')    : 0,
    ('Fairy', 'Fighting') : 1,
    ('Fairy', 'Fire')     : -1,
    ('Fairy', 'Flying')   : 0,
    ('Fairy', 'Ghost')    : 0,
    ('Fairy', 'Grass')    : 0,
    ('Fairy', 'Ground')   : 0,
    ('Fairy', 'Ice')      : 0,
    ('Fairy', 'Normal')   : 0,
    ('Fairy', 'Poison')   : -1,
    ('Fairy', 'Psychic')  : 0,
    ('Fairy', 'Rock')     : 0,
    ('Fairy', 'Steel')    : -1,
    ('Fairy', 'Water')    : 0,

    ('Fighting', 'Bug')      : -1,
    ('Fighting', 'Dark')     : 1,
    ('Fighting', 'Dragon')   : 0,
    ('Fighting', 'Electric') : 0,
    ('Fighting', 'Fairy')    : 1,
    ('Fighting', 'Fighting') : 0,
    ('Fighting', 'Fire')     : 0,
    ('Fighting', 'Flying')   : -1,
    ('Fighting', 'Ghost')    : -1,
    ('Fighting', 'Grass')    : 0,
    ('Fighting', 'Ground')   : 0,
    ('Fighting', 'Ice')      : 1,
    ('Fighting', 'Normal')   : 1,
    ('Fighting', 'Poison')   : -1,
    ('Fighting', 'Psychic')  : -1,
    ('Fighting', 'Rock')     : 1,
    ('Fighting', 'Steel')    : 1,
    ('Fighting', 'Water')    : 0,

    ('Fire', 'Bug')      : 1,
    ('Fire', 'Dark')     : 0,
    ('Fire', 'Dragon')   : -1,
    ('Fire', 'Electric') : 0,
    ('Fire', 'Fairy')    : 0,
    ('Fire', 'Fighting') : 0,
    ('Fire', 'Fire')     : -1,
    ('Fire', 'Flying')   : 0,
    ('Fire', 'Ghost')    : 0,
    ('Fire', 'Grass')    : 1,
    ('Fire', 'Ground')   : 0,
    ('Fire', 'Ice')      : 1,
    ('Fire', 'Normal')   : 0,
    ('Fire', 'Poison')   : 0,
    ('Fire', 'Psychic')  : 0,
    ('Fire', 'Rock')     : -1,
    ('Fire', 'Steel')    : 1,
    ('Fire', 'Water')    : -1,

    ('Flying', 'Bug')      : 1,
    ('Flying', 'Dark')     : 0,
    ('Flying', 'Dragon')   : 0,
    ('Flying', 'Electric') : -1,
    ('Flying', 'Fairy')    : 0,
    ('Flying', 'Fighting') : 1,
    ('Flying', 'Fire')     : 0,
    ('Flying', 'Flying')   : 0,
    ('Flying', 'Ghost')    : 0,
    ('Flying', 'Grass')    : 1,
    ('Flying', 'Ground')   : 0,
    ('Flying', 'Ice')      : 0,
    ('Flying', 'Normal')   : 0,
    ('Flying', 'Poison')   : 0,
    ('Flying', 'Psychic')  : 0,
    ('Flying', 'Rock')     : -1,
    ('Flying', 'Steel')    : -1,
    ('Flying', 'Water')    : 0,

    ('Ghost', 'Bug')      : 0,
    ('Ghost', 'Dark')     : -1,
    ('Ghost', 'Dragon')   : 0,
    ('Ghost', 'Electric') : 0,
    ('Ghost', 'Fairy')    : 0,
    ('Ghost', 'Fighting') : 0,
    ('Ghost', 'Fire')     : 0,
    ('Ghost', 'Flying')   : 0,
    ('Ghost', 'Ghost')    : 1,
    ('Ghost', 'Grass')    : 0,
    ('Ghost', 'Ground')   : 0,
    ('Ghost', 'Ice')      : 0,
    ('Ghost', 'Normal')   : -1,
    ('Ghost', 'Poison')   : 0,
    ('Ghost', 'Psychic')  : 1,
    ('Ghost', 'Rock')     : 0,
    ('Ghost', 'Steel')    : 0,
    ('Ghost', 'Water')    : 0,

    ('Grass', 'Bug')      : -1,
    ('Grass', 'Dark')     : 0,
    ('Grass', 'Dragon')   : -1,
    ('Grass', 'Electric') : 0,
    ('Grass', 'Fairy')    : 0,
    ('Grass', 'Fighting') : 0,
    ('Grass', 'Fire')     : -1,
    ('Grass', 'Flying')   : -1,
    ('Grass', 'Ghost')    : 0,
    ('Grass', 'Grass')    : -1,
    ('Grass', 'Ground')   : 1,
    ('Grass', 'Ice')      : 0,
    ('Grass', 'Normal')   : 0,
    ('Grass', 'Poison')   : -1,
    ('Grass', 'Psychic')  : 0,
    ('Grass', 'Rock')     : 1,
    ('Grass', 'Steel')    : -1,
    ('Grass', 'Water')    : 1,

    ('Ground', 'Bug')      : -1,
    ('Ground', 'Dark')     : 0,
    ('Ground', 'Dragon')   : 0,
    ('Ground', 'Electric') : 1,
    ('Ground', 'Fairy')    : 0,
    ('Ground', 'Fighting') : 0,
    ('Ground', 'Fire')     : 1,
    ('Ground', 'Flying')   : -1,
    ('Ground', 'Ghost')    : 0,
    ('Ground', 'Grass')    : -1,
    ('Ground', 'Ground')   : 0,
    ('Ground', 'Ice')      : 0,
    ('Ground', 'Normal')   : 0,
    ('Ground', 'Poison')   : 1,
    ('Ground', 'Psychic')  : 0,
    ('Ground', 'Rock')     : 1,
    ('Ground', 'Steel')    : 1,
    ('Ground', 'Water')    : 0,

    ('Ice', 'Bug')      : 0,
    ('Ice', 'Dark')     : 0,
    ('Ice', 'Dragon')   : 1,
    ('Ice', 'Electric') : 0,
    ('Ice', 'Fairy')    : 0,
    ('Ice', 'Fighting') : 0,
    ('Ice', 'Fire')     : -1,
    ('Ice', 'Flying')   : 1,
    ('Ice', 'Ghost')    : 0,
    ('Ice', 'Grass')    : 1,
    ('Ice', 'Ground')   : 1,
    ('Ice', 'Ice')      : -1,
    ('Ice', 'Normal')   : 0,
    ('Ice', 'Poison')   : 0,
    ('Ice', 'Psychic')  : 0,
    ('Ice', 'Rock')     : 0,
    ('Ice', 'Steel')    : -1,
    ('Ice', 'Water')    : -1,

    ('Normal', 'Bug')      : 0,
    ('Normal', 'Dark')     : 0,
    ('Normal', 'Dragon')   : 0,
    ('Normal', 'Electric') : 0,
    ('Normal', 'Fairy')    : 0,
    ('Normal', 'Fighting') : 0,
    ('Normal', 'Fire')     : 0,
    ('Normal', 'Flying')   : 0,
    ('Normal', 'Ghost')    : -1,
    ('Normal', 'Grass')    : 0,
    ('Normal', 'Ground')   : 0,
    ('Normal', 'Ice')      : 0,
    ('Normal', 'Normal')   : 0,
    ('Normal', 'Poison')   : 0,
    ('Normal', 'Psychic')  : 0,
    ('Normal', 'Rock')     : -1,
    ('Normal', 'Steel')    : -1,
    ('Normal', 'Water')    : 0,

    ('Poison', 'Bug')      : 0,
    ('Poison', 'Dark')     : 0,
    ('Poison', 'Dragon')   : 0,
    ('Poison', 'Electric') : 0,
    ('Poison', 'Fairy')    : 1,
    ('Poison', 'Fighting') : 0,
    ('Poison', 'Fire')     : 0,
    ('Poison', 'Flying')   : 0,
    ('Poison', 'Ghost')    : -1,
    ('Poison', 'Grass')    : 1,
    ('Poison', 'Ground')   : -1,
    ('Poison', 'Ice')      : 0,
    ('Poison', 'Normal')   : 0,
    ('Poison', 'Poison')   : -1,
    ('Poison', 'Psychic')  : 0,
    ('Poison', 'Rock')     : -1,
    ('Poison', 'Steel')    : -1,
    ('Poison', 'Water')    : 0,

    ('Psychic', 'Bug')      : 0,
    ('Psychic', 'Dark')     : -1,
    ('Psychic', 'Dragon')   : 0,
    ('Psychic', 'Electric') : 0,
    ('Psychic', 'Fairy')    : 0,
    ('Psychic', 'Fighting') : 1,
    ('Psychic', 'Fire')     : 0,
    ('Psychic', 'Flying')   : 0,
    ('Psychic', 'Ghost')    : 0,
    ('Psychic', 'Grass')    : 0,
    ('Psychic', 'Ground')   : 0,
    ('Psychic', 'Ice')      : 0,
    ('Psychic', 'Normal')   : 0,
    ('Psychic', 'Poison')   : 1,
    ('Psychic', 'Psychic')  : -1,
    ('Psychic', 'Rock')     : 0,
    ('Psychic', 'Steel')    : -1,
    ('Psychic', 'Water')    : 0,

    ('Rock', 'Bug')      : 1,
    ('Rock', 'Dark')     : 0,
    ('Rock', 'Dragon')   : 0,
    ('Rock', 'Electric') : 0,
    ('Rock', 'Fairy')    : 0,
    ('Rock', 'Fighting') : -1,
    ('Rock', 'Fire')     : 1,
    ('Rock', 'Flying')   : 1,
    ('Rock', 'Ghost')    : 0,
    ('Rock', 'Grass')    : 0,
    ('Rock', 'Ground')   : -1,
    ('Rock', 'Ice')      : 1,
    ('Rock', 'Normal')   : 0,
    ('Rock', 'Poison')   : 0,
    ('Rock', 'Psychic')  : 0,
    ('Rock', 'Rock')     : 0,
    ('Rock', 'Steel')    : -1,
    ('Rock', 'Water')    : 0,

    ('Steel', 'Bug')      : 0,
    ('Steel', 'Dark')     : 0,
    ('Steel', 'Dragon')   : 0,
    ('Steel', 'Electric') : -1,
    ('Steel', 'Fairy')    : 1,
    ('Steel', 'Fighting') : 0,
    ('Steel', 'Fire')     : -1,
    ('Steel', 'Flying')   : 0,
    ('Steel', 'Ghost')    : 0,
    ('Steel', 'Grass')    : 0,
    ('Steel', 'Ground')   : 0,
    ('Steel', 'Ice')      : 1,
    ('Steel', 'Normal')   : 0,
    ('Steel', 'Poison')   : 0,
    ('Steel', 'Psychic')  : 0,
    ('Steel', 'Rock')     : 1,
    ('Steel', 'Steel')    : -1,
    ('Steel', 'Water')    : -1,

    ('Water', 'Bug')      : 0,
    ('Water', 'Dark')     : 0,
    ('Water', 'Dragon')   : -1,
    ('Water', 'Electric') : 0,
    ('Water', 'Fairy')    : 0,
    ('Water', 'Fighting') : 0,
    ('Water', 'Fire')     : 1,
    ('Water', 'Flying')   : 0,
    ('Water', 'Ghost')    : 0,
    ('Water', 'Grass')    : -1,
    ('Water', 'Ground')   : 1,
    ('Water', 'Ice')      : 0,
    ('Water', 'Normal')   : 0,
    ('Water', 'Poison')   : 0,
    ('Water', 'Psychic')  : 0,
    ('Water', 'Rock')     : 1,
    ('Water', 'Steel')    : 0,
    ('Water', 'Water')    : -1
}

def type_logic(attackingPokemon, defendingPokemon):
    matchup = 0
    if ('Delta Stream' in attackingPokemon.ability):
        return True
    if ('Multitype' in attackingPokemon.ability or
        'Multitype' in defendingPokemon.ability or
        'RKS System' in attackingPokemon.ability or
        'RKS System' in defendingPokemon.ability):
        return False
    for x in attackingPokemon.type:
        if x:
            for y in defendingPokemon.type:
                if y:
                    if (('Levitate' in defendingPokemon.ability and 'Ground' in x) or
                        ('Flash Fire' in defendingPokemon.ability and 'Fire' in x) or
                        ('Water Bubble' in defendingPokemon.ability and 'Fire' in x) or
                        ('Water Absorb' in defendingPokemon.ability and 'Water' in x) or
                        ('Storm Drain' in defendingPokemon.ability and 'Water' in x) or
                        ('Dry Skin' in defendingPokemon.ability and 'Water' in x) or
                        ('Lightningrod' in defendingPokemon.ability and 'Electric' in x) or
                        ('Volt Absorb' in defendingPokemon.ability and 'Electric' in x) or
                        ('Motor Drive' in defendingPokemon.ability and 'Electric' in x) or
                        ('Sap Sipper' in defendingPokemon.ability and 'Grass' in x) or
                        ('Desolate Land' in defendingPokemon.ability and 'Water' in x) or
                        ('Primordial Sea' in defendingPokemon.ability and 'Fire' in x) or
                        ('Prankster' in attackingPokemon.ability and 'Dark' in y)):
                        matchup -= 1
                    elif (('Fluffy' in defendingPokemon.ability and 'Fire' in x) or
                          ('Dry Skin' in defendingPokemon.ability and 'Fire' in x) or
                          ('Steelworker' in attackingPokemon.ability and 'Rock' in y) or
                          ('Steelworker' in attackingPokemon.ability and 'Fairy' in y) or
                          ('Steelworker' in attackingPokemon.ability and 'Ice' in y)):
                        matchup += 1
                    elif ('Scrappy' in attackingPokemon.ability and 'Ghost' in y):
                        matchup += 0
                    elif (('Tinted Lens' in attackingPokemon.ability and 'Bug' in x) and
                          ('Fairy' in y or 'Fighting' in y or 'Fire' in y or
                           'Flying' in y or 'Ghost' in y or 'Poison' in y or
                           'Steel' in y)):
                        matchup += 0
                    elif (('Tinted Lens' in attackingPokemon.ability and 'Flying' in x) and
                          ('Electric' in y or 'Rock' in y or 'Steel' in y)):
                        matchup += 0
                    elif (('Tinted Lens' in attackingPokemon.ability and 'Normal' in x) and
                          ('Rock' in y or 'Steel' in y)):
                        matchup += 0
                    elif (('Tinted Lens' in attackingPokemon.ability and 'Poison' in x) and
                          ('Ghost' in y or 'Ground' in y or 'Poison' in y or
                           'Rock' in y)):
                        matchup += 0
                    elif (('Tinted Lens' in attackingPokemon.ability and 'Psychic' in x) and
                          ('Psychic' in y or 'Steel' in y)):
                        matchup += 0
                    else:
                        matchup += TypeChart[(x, y)]
    if matchup > 0:
        return True
    else:
        return False

ALL_POKEMON_S = []
ALL_POKEMON_D = []
ABILITIES = {}
MEGA_STONES = []
Z_CRYSTALS = []
BERRIES = []
PLAYERS = []
playerNames = []
TIERS_SINGLES = ['LC', 'LC Uber', 'Untiered', 'NFE', 'PU', 'NU', 'RU', 'UU', 'OU', 'Uber']
TIERS_DOUBLES = ['LC', 'Untiered', 'DUU', 'DOU', 'DUber']
GENERATIONS = ['Kanto', 'Johto', 'Hoenn', 'Sinnoh', 'Unova', 'Kalos', 'Alola']
TYPES = ['Bug', 'Dark', 'Dragon', 'Electric', 'Fairy', 'Fighting', 'Fire', 'Flying', 'Ghost', 'Grass', 'Ground', 'Ice', 'Normal', 'Poison', 'Psychic', 'Rock', 'Steel', 'Water']
ITEMS = ['Mega Stones', 'Z-Crystals', 'Berries', 'Choice Band', 'Choice Scarf', 'Choice Specs', 'Leftovers', 'Life Orb']
GIMMICKS = ['Sun', 'Rain', 'Sand', 'Hail', 'Trick Room', 'Baton Pass', 'E-Terrain', 'G-Terrain', 'M-Terrain', 'P-Terrain']
ALL_BANNERS = []
month = int(date.today().strftime('%m'))
day = int(date.today().strftime('%d'))

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
        self.generated_draft = int(row[16])
        self.generated_nemesis = int(row[17])
        self.generated_random = int(row[18])
        self.picked_draft = int(row[19])
        self.picked_nemesis = int(row[20])
        self.banned = int(row[21])

with open(os.path.join(DATA, 'Singles.csv'), 'r', encoding='utf-8') as fileName:
    reader = csv.reader(fileName)
    next(reader, None)
    for row in reader:
        ALL_POKEMON_S.append(Pokemon(row))

with open(os.path.join(DATA, 'Abilities.csv'), 'r', encoding='utf-8') as fileName:
    reader = csv.reader(fileName)
    for row in reader:
        ABILITIES[row[0]] = [row[x] for x in range(1,4) if row[x] != '']

with open(os.path.join(DATA, 'Items.csv'), 'r', encoding='utf-8') as fileName:
    reader = csv.reader(fileName)
    for row in reader:
        if row[0].endswith('ite') and row[0] != 'Eviolite':
            MEGA_STONES.append(row[0])
        if row[0].endswith('ium Z'):
            Z_CRYSTALS.append(row[0])
        if row[0].endswith('Berry'):
            BERRIES.append(row[0])

with open(os.path.join(DATA, 'Banners.csv'), 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        ALL_BANNERS.append(row)


################################################################################
# global helper functions
################################################################################
def RGBAImage(path):
    return ImageTk.PhotoImage(Image.open(path).convert('RGBA'))


def RGBAImage2(path):
    return Image.open(path).convert('RGBA')


def create_image(base_image, image):
    base_image.paste(image, (0, 0), image)


def popup_message(self, type, text, text2=''):
    # initialize window and settings
    top = tk.Toplevel(self)
    top.grab_set()
    x = app.winfo_x()
    y = app.winfo_y()
    top.geometry('+%d+%d' % (x + 100, y + 200))

    # determine type of popup image
    if type == 'ERROR':
        icon = tk.Label(top, image=self.img_error)
    elif type == 'INFO':
        icon = tk.Label(top, image=self.img_info)
    icon.grid(row=0, column=0, padx=20, pady=20, sticky='nsew')

    # display message
    message = tk.Label(top, text=text+text2)
    message.grid(row=0, column=1, padx=20, pady=20, sticky='nsew')

    # close button
    back_button = tk.Button(top, text='Ok', width=10, command=top.destroy)
    back_button.grid(row=1, column=0, columnspan=2, padx=100, pady=5, sticky='nsew')

    # do not let user interact with underlying window
    self.wait_window(top)


def get_banner_num():
    if month < 6 or (month == 6 and 1 <= day <= 8):
        return 0
    if month == 6 and 9 <= day <= 15:
        return 2
    if month == 6 and 16 <= day <= 22:
        return 4
    if month == 6 and 23 <= day <= 29:
        return 6
    if (month == 6 and 30 == day) or (month == 7 and 1 <= day <= 6):
        return 8
    if month == 7 and 7 <= day <= 13:
        return 10
    if month == 7 and 14 <= day <= 20:
        return 12
    if month == 7 and 21 <= day <= 27:
        return 14
    return 0


def update_all_optionmenus(self):
    # get each optionmenu to update
    menu1 = self.pages['Store'].player_option['menu']
    menu2 = self.pages['Players'].player_option['menu']
    menu3 = self.pages['DraftSettings'].player_option[0]['menu']
    menu4 = self.pages['DraftSettings'].player_option[1]['menu']
    menu5 = self.pages['RandomSettings'].player_option[0]['menu']
    menu6 = self.pages['RandomSettings'].player_option[1]['menu']

    # delete the optionmenu's items
    menu1.delete(0, 'end')
    menu2.delete(0, 'end')
    menu3.delete(0, 'end')
    menu4.delete(0, 'end')
    menu5.delete(0, 'end')
    menu6.delete(0, 'end')

    # re-populate the menu lists
    for player in playerNames:
        menu1.add_command(label=player, command=lambda player=player: self.pages['Store'].switch_player(player))
        menu2.add_command(label=player, command=lambda player=player: self.pages['Players'].display_pkmn(player))
        menu3.add_command(label=player, command=lambda player=player: self.pages['Draft'].current_player[0].set(player))
        menu4.add_command(label=player, command=lambda player=player: self.pages['Draft'].current_player[1].set(player))
        menu5.add_command(label=player, command=lambda player=player: self.pages['Random'].current_player[0].set(player))
        menu6.add_command(label=player, command=lambda player=player: self.pages['Random'].current_player[1].set(player))


def strip_mega_name(name):
    return name.replace('-Mega-X', '').replace('-Mega-Y', '').replace('-Ash', '').replace('-Mega', '')


def get_mega_name(pkmn):
    if ((pkmn.item != 'Eviolite' and (pkmn.item.endswith('ite')) or 'Dragon Ascent' in pkmn.moves)):
        return pkmn.name + '-Mega'
    elif pkmn.item.endswith('ite X'):
        return pkmn.name + '-Mega-X'
    elif pkmn.item.endswith('ite Y'):
        return pkmn.name + '-Mega-Y'
    elif pkmn.ability == 'Battle Bond':
        return pkmn.name + '-Ash'
    else:
        return pkmn.name


def get_rarity(name):
    for pkmn in ALL_POKEMON_S:
        if name.endswith('-Mega') or name.endswith('Mega-Y') or name.endswith('Mega-X') or name.endswith('-Ash'):
            temp_name = strip_mega_name(name)
            if pkmn.item == 'Eviolite':
                continue
            if pkmn.name == temp_name:
                if (pkmn.item.endswith('ite') or pkmn.item.endswith('ite X') or pkmn.item.endswith('ite Y') or pkmn.ability == 'Battle Bond'):
                    rarity = pkmn.rarity
                    break
        else:
            temp_name = name
            if pkmn.name == temp_name:
                rarity = pkmn.rarity
                break
    return rarity


def check_validity(self, pkmn, team=0):
    # get all exclusions
    type_list = list(filter(None, [i.get() for i in self.pkmn_excl_types]))
    tier_list = list(filter(None, [i.get() for i in self.pkmn_excl_tiers_s]))
    gimmick_list = list(filter(None, [i.get() for i in self.pkmn_excl_gimmicks]))
    if hasattr(self, 'pkmn_pool_list'):
        if ((pkmn in self.pkmn_pool_list) or
            (pkmn.name in [pool.name for pool in self.pkmn_pool_list]) or
            (pkmn.tier in tier_list) or
            (pkmn.type[0] in type_list) or
            (pkmn.type[1] and pkmn.type[1] in type_list) or
            (check_valid_generation(self, pkmn)) or
            (check_valid_item(self, pkmn)) or
            (pkmn.tag in gimmick_list)):
            return False
    else:
        names = [slot.name for slot in self.pkmn_team_list[team] if slot != None]
        if ((pkmn in self.pkmn_team_list[team]) or
            (pkmn.name in names) or
            (pkmn.tier in tier_list) or
            (pkmn.type[0] in type_list) or
            (pkmn.type[1] and pkmn.type[1] in type_list) or
            (check_valid_generation(self, pkmn)) or
            (check_valid_item(self, pkmn)) or
            (pkmn.tag in gimmick_list)):
            return False
    return True


def is_mega(pkmn):
    if pkmn.item != 'Eviolite':
        if (pkmn.item.endswith('ite') or pkmn.item.endswith('ite X') or
            pkmn.item.endswith('ite Y') or ('Dragon Ascent' in pkmn.moves) or
            pkmn.ability == 'Battle Bond'):
            return True
    return False


def check_valid_generation(self, pkmn):
    dex_list = []
    for generation in [j.get() for j in self.pkmn_excl_gens]:
        if generation == 'Kanto':
            for i in range(1, 152):
                dex_list.append(str(i))
        if generation == 'Johto':
            for i in range(152, 252):
                dex_list.append(str(i))
        if generation == 'Hoenn':
            for i in range(252, 387):
                dex_list.append(str(i))
        if generation == 'Sinnoh':
            for i in range(387, 494):
                dex_list.append(str(i))
        if generation == 'Unova':
            for i in range(494, 650):
                dex_list.append(str(i))
        if generation == 'Kalos':
            for i in range(650, 722):
                dex_list.append(str(i))
        if generation == 'Alola':
            for i in range(722, 807):
                dex_list.append(str(i))
    if str(pkmn.dex) in dex_list:
        return True
    return False


def check_valid_item(self, pkmn):
    item_list = []
    for item in list(filter(None, [i.get() for i in self.pkmn_excl_items])):
        if item == 'Mega Stones':
            item_list.extend(MEGA_STONES)
        elif item == 'Z-Crystals':
            item_list.extend(Z_CRYSTALS)
        elif item == 'Berries':
            item_list.extend(BERRIES)
        else:
            item_list.append(item)
    if pkmn.item in item_list:
        return True
    return False


def validate(self, page):
    # get exclusion lists
    temp_excl_tiers = list(filter(None, [i.get() for i in self.parent_page().pkmn_excl_tiers_s]))
    temp_excl_types = list(filter(None, [i.get() for i in self.parent_page().pkmn_excl_types]))
    temp_excl_gimmicks = list(filter(None, [i.get() for i in self.parent_page().pkmn_excl_gimmicks]))
    temp_counter = 0
    temp_list = []

    # check if Pokemon fit criteria and count number of occurrences
    for pkmn in ALL_POKEMON_S:
        if ((pkmn.name in [i.name for i in temp_list]) or
            (pkmn.dex in [j.dex for j in temp_list]) or
            (pkmn.tier in temp_excl_tiers) or
            (pkmn.type[0] in temp_excl_types) or
            (pkmn.type[1] and pkmn.type[1] in temp_excl_types) or
            (check_valid_generation(self.parent_page(), pkmn)) or
            (check_valid_item(self.parent_page(), pkmn)) or
                (pkmn.tag in temp_excl_gimmicks)):
            continue
        else:
            temp_list.append(pkmn)
            temp_counter += 1

    if temp_counter >= 18:
        # valid number of Pokemon
        self.controller.change_page(page)
    else:
        popup_message(self.controller,
                      'ERROR',
                      'Not enough Pokemon fit the criteria you have selected.',
                      text2='\nPlease remove some restrictions.')


def get_sets(self):
    self.controller.clipboard_clear()
    sets = ''
    for team in self.pkmn_team_list:
        sets += '====================\n'
        for pkmn in team:
            if pkmn.item:
                sets += pkmn.name + ' @ ' + pkmn.item + '\n'
            else:
                sets += 'pkmn.name\n'
            if 'LC' in pkmn.tier:
                sets += 'Level: 5\n'
            sets += 'Ability: ' + pkmn.ability + '\n'
            sets += 'EVs: ' + pkmn.evSpread + '\n'
            sets += pkmn.nature + ' Nature\n'
            if pkmn.ivSpread:
                sets += 'IVs: ' + pkmn.ivSpread + '\n'
            for move in pkmn.moves:
                if move:
                    sets += '- ' + move + '\n'
            sets += '\n'
        sets += '\n'
    self.controller.clipboard_append(sets)
    update_statistics(self)
    popup_message(self.controller, 'INFO', 'Copied all sets to clipboard.')


def update_statistics(self):
    if hasattr(self, 'ban_list'):
        for team in self.ban_list:
            for pkmn in team:
                if pkmn:
                    pkmn.banned += 1
    if hasattr(self, 'pkmn_pool_list'):
        for pkmn in self.pkmn_pool_list:
            if self.draft_mode.get() == 'Nemesis':
                pkmn.generated_nemesis += 1
            else:
                pkmn.generated_draft += 1
    for team in self.pkmn_team_list:
        for pkmn in team:
            if hasattr(self, 'draft_mode'):
                if self.draft_mode.get() == 'Nemesis':
                    pkmn.picked_nemesis += 1
                else:
                    pkmn.picked_draft += 1
            else:
                pkmn.generated_random += 1
    file = os.path.join(DATA, 'Singles.csv')
    with open(file, 'w', encoding='utf-8', newline='') as fileName:
        writer = csv.writer(fileName, delimiter=',')
        writer.writerow(['POKEMON', 'DEX', 'TYPE 1', 'TYPE 2', 'TIER',
                         'RARITY', 'SRL', 'TAG', 'ITEM', 'ABILITY', 'EV SPREAD',
                         'NATURE', 'IV SPREAD', 'MOVE 1', 'MOVE 2', 'MOVE 3',
                         'MOVE 4', 'GENERATED (D)', 'GENERATED (N)',
                         'GENERATED (R)', 'PICKED (D)', 'PICKED (N)', 'BANNED'])
        for pkmn in ALL_POKEMON_S:
            writer.writerow(
                [pkmn.name, pkmn.dex, pkmn.type[0], pkmn.type[1],
                 pkmn.tier, pkmn.rarity, pkmn.tag, pkmn.item, pkmn.ability,
                 pkmn.evSpread, pkmn.nature, pkmn.ivSpread,
                 pkmn.moves[0], pkmn.moves[1], pkmn.moves[2], pkmn.moves[3],
                 str(pkmn.generated_draft), str(pkmn.generated_nemesis),
                 str(pkmn.generated_random), str(pkmn.picked_draft),
                 str(pkmn.picked_nemesis), str(pkmn.banned)])


def clean_up(self):
    if hasattr(self.parent_page(), 'game_activated'):
        self.parent_page().game_activated = False
    if hasattr(self.parent_page(), 'turn'):
        self.parent_page().turn = 0
    if hasattr(self.parent_page(), 'pkmn_pool_list'):
        self.parent_page().pkmn_pool_list = []
        for i in range(18):
            self.parent_page().pool_buttons[i].config(command=lambda: None)
    if hasattr(self.parent_page(), 'ban_list'):
        self.parent_page().ban_list = [[None, None], [None, None]]
    if hasattr(self.parent_page(), 'ban_phase_finished'):
        self.parent_page().ban_phase_finished = False
    self.parent_page().pkmn_team_list = [[None for i in range(6)] for j in range(2)]
    if hasattr(self.parent_page(), 'pkmn_not_picked'):
        self.parent_page().pkmn_not_picked = [True for i in range(18)]
    for i in range(2):
        if hasattr(self.parent_page(), 'ban_buttons'):
            for j in range(2):
                self.parent_page().ban_buttons[i][j].config(command=lambda: None)
        for j in range(6):
            self.parent_page().team_buttons[i][j].config(command=lambda: None)
    if hasattr(self.parent_page(), 'pool_buttons'):
        for i in range(len(self.parent_page().pool_buttons)):
            self.parent_page().pool_buttons[i].config(
                image=self.parent_page().controller.img_blank[0],
                command=lambda: None)
    if hasattr(self.parent_page(), 'ban_buttons'):
        for i in range(len(self.parent_page().ban_buttons)):
            for j in range(len(self.parent_page().ban_buttons[i])):
                self.parent_page().ban_buttons[i][j].config(
                    image=self.parent_page().controller.img_blank[0],
                    command=lambda: None)
    if hasattr(self.parent_page(), 'team_buttons'):
        for i in range(len(self.parent_page().team_buttons)):
            for j in range(len(self.parent_page().team_buttons[i])):
                self.parent_page().team_buttons[i][j].config(
                    image=self.parent_page().controller.img_blank[0],
                    command=lambda: None)


def setup_pkmn_settings(self, page):
    for i in range(1, 22):
        self.grid_rowconfigure(i, weight=1)

    # exclusions header
    self.exclusions_img = RGBAImage(os.path.join(COMMON, 'label_exclusions.png'))
    self.exclusions_text = tk.Label(self, image=self.exclusions_img)
    self.exclusions_text.grid(row=0, column=0, columnspan=6, sticky='nsw')

    # singles tiers section
    self.tier_text = tk.Label(self, text='Tiers (Singles)')
    self.tier_text.grid(row=1, column=0, rowspan=2, sticky='w')
    self.tier_buttons = []
    for i in range(len(TIERS_SINGLES)):
        self.tier_buttons.append(tk.Checkbutton(self,
            text=TIERS_SINGLES[i],
            variable=self.parent_page().pkmn_excl_tiers_s[i],
            onvalue=TIERS_SINGLES[i],
            offvalue=''))
        self.tier_buttons[i].grid(row=1 + int(i/5), column=(i%5) + 1, sticky='w')

    # create horizontal separators for clarity
    self.separators = [ttk.Separator(self, orient='horizontal') for i in range(7)]
    self.separators[0].grid(row=3, column=0, columnspan=6, sticky='nsew')

    # doubles tiers section
    self.tier2_text = tk.Label(self, text='Tiers (Doubles)')
    self.tier2_text.grid(row=4, column=0, sticky='w')
    self.tier2_buttons = []
    for i in range(len(TIERS_DOUBLES)):
        self.tier2_buttons.append(tk.Checkbutton(self,
            text=TIERS_DOUBLES[i],
            variable=self.parent_page().pkmn_excl_tiers_d[i],
            onvalue=TIERS_DOUBLES[i],
            state='disabled',
            offvalue=''))
        self.tier2_buttons[i].grid(row=4 + int(i/5), column=(i%5) + 1, sticky='w')
    self.separators[1].grid(row=5, column=0, columnspan=6, sticky='nsew')

    # generations section
    self.gen_text = tk.Label(self, text='Generations')
    self.gen_text.grid(row=6, column=0, rowspan=2, sticky='w')
    self.gen_buttons = []
    for i in range(len(GENERATIONS)):
        self.gen_buttons.append(tk.Checkbutton(self,
            text=GENERATIONS[i],
            variable=self.parent_page().pkmn_excl_gens[i],
            onvalue=GENERATIONS[i],
            offvalue=''))
        self.gen_buttons[i].grid(row=6 + int(i/5), column=(i%5) + 1, sticky='w')
    self.separators[2].grid(row=8, column=0, columnspan=6, sticky='nsew')

    # types section
    self.type_text = tk.Label(self, text='Types')
    self.type_text.grid(row=9, column=0, rowspan=4, sticky='w')
    self.type_buttons = []
    for i in range(len(TYPES)):
        self.type_buttons.append(tk.Checkbutton(self,
            text=TYPES[i],
            variable=self.parent_page().pkmn_excl_types[i],
            onvalue=TYPES[i],
            offvalue=''))
        self.type_buttons[i].grid(row=9 + int(i/5), column=(i%5) + 1, sticky='w')
    self.separators[3].grid(row=13, column=0, columnspan=6, sticky='nsew')

    # held items section
    self.item_text = tk.Label(self, text='Items')
    self.item_text.grid(row=14, column=0, rowspan=2, sticky='w')
    self.item_buttons = []
    for i in range(len(ITEMS)):
        self.item_buttons.append(tk.Checkbutton(self,
            text=ITEMS[i],
            variable=self.parent_page().pkmn_excl_items[i],
            onvalue=ITEMS[i],
            offvalue=''))
        self.item_buttons[i].grid(row=14 + int(i/5), column=(i%5) + 1, sticky='w')
    self.separators[4].grid(row=16, column=0, columnspan=6, sticky='nsew')

    # gimmick section
    self.gimmick_text = tk.Label(self, text='Gimmicks')
    self.gimmick_text.grid(row=17, column=0, rowspan=3, sticky='w')
    self.gimmick_buttons = []
    for i in range(len(GIMMICKS)):
        self.gimmick_buttons.append(tk.Checkbutton(self,
            text=GIMMICKS[i],
            variable=self.parent_page().pkmn_excl_gimmicks[i],
            onvalue=GIMMICKS[i],
            offvalue=''))
        self.gimmick_buttons[i].grid(row=17 + int(i/5), column=(i%5) + 1, sticky='w')
    self.separators[5].grid(row=19, column=0, columnspan=6, sticky='nsew')

    # rentals usage section (empty)
    self.usage_text = tk.Label(self, text='Usage')
    self.usage_text.grid(row=20, column=0, sticky='w')
    self.separators[6].grid(row=21, column=0, columnspan=6, sticky='nsew')

    # back button
    self.back_frame = tk.Frame(self)
    self.back_frame.grid(row=22, column=0, columnspan=6, padx=5, pady=5, sticky='nsew')
    self.back_frame.grid_columnconfigure(0, weight=1)
    self.back_button = tk.Button(self.back_frame, image=self.controller.img_back['inactive'], bd=0.1, command=lambda page=page: validate(self, page))
    self.back_button.grid(row=0, column=0, sticky='nsew')
    self.back_button.bind('<Enter>', lambda event: self.controller.on_enter(self.back_button, self.controller.img_back['active']))
    self.back_button.bind('<Leave>', lambda event: self.controller.on_leave(self.back_button, self.controller.img_back['inactive']))


def setup_game_settings(self, page):
    for i in range(1, 6):
        self.grid_rowconfigure(i, weight=1)
    for i in range(4):
        self.grid_columnconfigure(i, weight=1)

    # rules header
    self.rules_img = RGBAImage(os.path.join(COMMON, 'label_rules.png'))
    self.rules_label = tk.Label(self, image=self.rules_img)
    self.rules_label.grid(row=0, column=0, columnspan=4, sticky='nsw')

    # battle mode | singles | doubles | srl
    self.battle_mode_text = tk.Label(self, text='Battle Mode')
    self.battle_mode_text.grid(row=1, column=0, padx=5, pady=5, sticky='w')
    self.battle_mode_buttons = []
    battle_modes = ['Singles', 'Doubles', 'SRL']
    for i in range(len(battle_modes)):
        self.battle_mode_buttons.append(tk.Radiobutton(self,
            text=battle_modes[i],
            variable=self.parent_page().battle_mode,
            indicatoron=0,
            width=10,
            value=battle_modes[i],
            command=self.update_gen_settings))
        self.battle_mode_buttons[i].grid(row=1+int(i/5), column=(i % 5)+1, padx=5, pady=5, sticky='nsew')

    if page == 'Draft':
        # draft mode | standard | nemesis | first pick
        self.draft_mode_text = tk.Label(self, text='Draft Mode')
        self.draft_mode_text.grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.draft_mode_buttons = []
        draft_modes = ['Standard', 'Nemesis', 'First Pick']
        for i in range(len(draft_modes)):
            self.draft_mode_buttons.append(tk.Radiobutton(self,
                text=draft_modes[i],
                variable=self.parent_page().draft_mode,
                indicatoron=0,
                value=draft_modes[i],
                command=self.reset_game))
            self.draft_mode_buttons[i].grid(row=2 + int(i/5), column=(i % 5) + 1, padx=5, pady=5, sticky='nsew')

        # bans | 0 | 1 | 2
        self.ban_number_text = tk.Label(self, text='Bans')
        self.ban_number_text.grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.ban_number_buttons = []
        ban_number = [0, 1, 2]
        for i in range(len(ban_number)):
            self.ban_number_buttons.append(tk.Radiobutton(self,
                text=ban_number[i],
                variable=self.parent_page().ban_number,
                indicatoron=0,
                value=ban_number[i],
                command=self.reset_game))
            self.ban_number_buttons[i].grid(row=3 + int(i/5), column=(i % 5) + 1, padx=5, pady=5, sticky='nsew')
    else:
        # theme | random | balanced | monotype
        self.theme_text = tk.Label(self, text='Theme')
        self.theme_text.grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.theme_buttons = []
        themes = ['Random', 'Balanced', 'Monotype']
        for i in range(len(themes)):
            self.theme_buttons.append(tk.Radiobutton(self, text=themes[i],
                variable=self.parent_page().theme,
                indicatoron=0,
                width=10,
                value=themes[i],
                command=self.update_gen_settings))
            self.theme_buttons[i].grid(row=2+int(i/5), column=(i%5)+1, padx=5, pady=5, sticky='nsew')

        # create dropdown menus for two types
        self.type_option = []
        for i in range(2):
            self.type_option.append(tk.OptionMenu(self, self.parent_page().type[i], *TYPES))
            self.type_option[i].config(width=10)
            self.type_option[i].grid(row=7, column=i*2, columnspan=2, padx=5, pady=5, sticky='ew')
            # remove since the mode is not monotype
            self.type_option[i].grid_remove()

    # megas | no | yes
    self.mega_text = tk.Label(self, text='Show Megas')
    self.mega_text.grid(row=4 if (page == 'Draft') else 3, column=0, padx=5, pady=5, sticky='w')
    self.mega_buttons = []
    megas = ['No', 'Yes']
    for i in range(len(megas)):
        self.mega_buttons.append(tk.Radiobutton(self,
            text=megas[i],
            variable=self.parent_page().show_megas,
            indicatoron=0,
            value=megas[i],
            command=self.parent_page().replace_images))
        self.mega_buttons[i].grid(row=4 + int(i/5) if (page == 'Draft') else 3 + int(i/5), column=(i%5) + 1, padx=5, pady=5, sticky='nsew')

    # hidden | no | yes
    self.hidden_text = tk.Label(self, text='Hide Pokemon')
    self.hidden_text.grid(row=5 if (page == 'Draft') else 4, column=0, padx=5, pady=5, sticky='w')
    self.hidden_buttons = []
    hidden = ['No', 'Yes']
    for i in range(len(hidden)):
        self.hidden_buttons.append(tk.Radiobutton(self,
            text=hidden[i],
            variable=self.parent_page().hidden,
            indicatoron=0,
            value=hidden[i]))
        self.hidden_buttons[i].grid(row=5 + int(i/5) if (page == 'Draft') else 4 + int(i/5), column=(i % 5) + 1, padx=5, pady=5, sticky='nsew')

    # create dropdown menus for two players
    self.player_option = []
    for i in range(2):
        self.player_option.append(tk.OptionMenu(self, self.parent_page().current_player[i], *playerNames))
        self.player_option[i].config(width=10)
        self.player_option[i].grid(row=6, column=i*2, columnspan=2, padx=5, pady=5, sticky='ew')
        self.player_option[i].grid_remove()

    # back button
    self.back_frame = tk.Frame(self)
    self.back_frame.grid(row=9, column=0, columnspan=4, pady=5, sticky='nsew')
    self.back_frame.grid_columnconfigure(0, weight=1)
    self.back_button = tk.Button(self.back_frame, image=self.controller.img_back['inactive'], bd=0.1, command=lambda page=page: exit(self, page))
    self.back_button.grid(row=0, column=0, sticky='nsew')
    self.back_button.bind('<Enter>', lambda event: self.controller.on_enter(self.back_button, self.controller.img_back['active']))
    self.back_button.bind('<Leave>', lambda event: self.controller.on_leave(self.back_button, self.controller.img_back['inactive']))


def exit(self, page):
    # get number of Pokemon on each roster
    list1 = len(PLAYERS[playerNames.index(self.parent_page().current_player[0].get())].pkmn_list) if (self.parent_page().current_player[0].get()) else 0
    list2 = len(PLAYERS[playerNames.index(self.parent_page().current_player[1].get())].pkmn_list) if (self.parent_page().current_player[1].get()) else 0
    # check if amount of Pokemon is invalid
    if (self.parent_page().battle_mode.get() == 'SRL' and (list1 + list2 < 18) and page == 'Draft'):
        popup_message(self.controller, 'ERROR', 'Not enough Pokemon required to Draft (18 needed).')
    elif (self.parent_page().battle_mode.get() == 'SRL' and (list1 < 12 or list2 < 12) and page == 'Random'):
        popup_message(self.controller, 'ERROR', 'Not enough Pokemon required for Random (12 needed per player).')
    else:
        # valid amount, update page info and change page
        self.parent_page().replace_images()
        self.controller.change_page(page)
