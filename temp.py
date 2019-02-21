try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk
from PIL import Image, ImageTk

import os
import csv
import time
import random
from random import shuffle


from Pokemon import *


DEBUG = True
def debug(message=None):
    if DEBUG:
        if message:
            print(message)
        else:
            print()

ROOT = os.path.dirname(os.path.realpath(__file__))

TIERS_SINGLES = ['LC', 'LC Uber', 'Untiered', 'NFE', 'PU', 'NU', 'RU', 'UU', 'OU', 'Uber']
TIERS_DOUBLES = ['LC', 'Untiered', 'DUU', 'DOU', 'DUber']
GENERATIONS = ['Kanto', 'Johto', 'Hoenn', 'Sinnoh', 'Unova', 'Kalos', 'Alola']
TYPES = ['Bug', 'Dark', 'Dragon', 'Electric', 'Fairy', 'Fighting', 'Fire', 'Flying', 'Ghost', 'Grass', 'Ground', 'Ice', 'Normal', 'Poison', 'Psychic', 'Rock', 'Steel', 'Water']
ITEMS = ['Mega Stones', 'Z-Crystals', 'Berries', 'Choice Band', 'Choice Scarf', 'Choice Specs', 'Leftovers', 'Life Orb']
GIMMICKS = ['Sun', 'Rain', 'Sand', 'Hail', 'Trick Room', 'Baton Pass', 'E-Terrain', 'G-Terrain', 'M-Terrain', 'P-Terrain']

class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.side_frame = tk.Frame(self)
        self.side_frame.grid(row=0, column=0, sticky="nsew")

        self.main_frame = tk.Frame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew")

        self.sidebar = Sidebar(parent=self.side_frame, controller=self)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        self.pages = {}

        for Class in (Draft, Random, GenerateSettings, Banners):
            page_name = Class.__name__
            frame = Class(parent=self.main_frame, controller=self)
            self.pages[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame('Draft')

        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

    def show_frame(self, page_name):
        frame = self.pages[page_name]
        frame.tkraise()

###############################################################################
class Sidebar(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.label_text = ['Battle', 'League']
        self.labels = []
        self.button_text = [['Draft', 'Random'], ['Banners']] # remove after getting images
        self.button_states = ['active', 'inactive']
        self.buttons = []

        self.section_frames = []
        self.tmp_counter = 0
        for i in range(len(self.label_text)):
            self.section_frames.append(tk.Frame(self))
            self.section_frames[i].grid(row=i, column=0, sticky="nsew")
            self.labels.append(tk.Label(self.section_frames[i], text=self.label_text[i], justify="center"))
            self.labels[i].grid(row=0, column=0, sticky="nsew")
            for j in range(len(self.button_text[i])):
                self.buttons.append(tk.Button(self.section_frames[i], text=self.button_text[i][j], command=lambda i=i, j=j: self.controller.show_frame(self.button_text[i][j])))
                self.buttons[self.tmp_counter].grid(row=j+1, column=0, sticky="nsew")
                self.tmp_counter += 1
###############################################################################

###############################################################################
class Draft(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        ##### Private Variables #####
        # misc. variables
        self.alpha = 0
        self.turn = 0
        self.game_activated = False
        self.pokemon_not_picked = [True for i in range(18)]
        for i in range(8):
            self.grid_rowconfigure(i, weight=1)
        for i in range(6):
            self.grid_columnconfigure(i, weight=1)
        # filter/exclusion variables
        self.pokemon_exclusion_tiers_singles = [tk.StringVar() for i in range(len(TIERS_SINGLES))]
        self.pokemon_exclusion_tiers_doubles = [tk.StringVar() for i in range(len(TIERS_DOUBLES))]
        self.pokemon_exclusion_generations = [tk.StringVar() for i in range(len(GENERATIONS))]
        self.pokemon_exclusion_types = [tk.StringVar() for i in range(len(TYPES))]
        self.pokemon_exclusion_items = [tk.StringVar() for i in range(len(ITEMS))]
        self.pokemon_exclusion_gimmicks = [tk.StringVar() for i in range(len(GIMMICKS))]
        self.pokemon_exclusion_usages = []
        # other pokemon variables
        self.checks_and_counters = [[] for i in range(18)]
        #############################

        ##### Pool Pokemon #####
        self.pokemon_pool_list = []
        self.pool_buttons = []
        for i in range(3):
            for j in range(6):
                x = (i*6) + j
                self.pool_buttons.append(tk.Button(self, text="? ? ? ? ?", command=None))
                self.pool_buttons[x].grid(row=i, column=j, padx=5, pady=5, sticky="nsew")
        ########################

        ##### Ban Boxes #####
        self.pokemon_ban_list = [[], []]
        self.ban_text = tk.Label(self, text="BANS")
        self.ban_text.grid(row=4, column=2, columnspan=2, sticky="nsew")
        self.ban_buttons = [[], []]
        for i in range(2):
            for j in range(2):
                self.ban_buttons[i].append(tk.Button(self, text="? ? ? ? ?", command=None))
                if i == 0:
                    self.ban_buttons[i][j].grid(row=4, column=i*4+j, padx=5, pady=5, sticky="nsew")
                else:
                    self.ban_buttons[i][j].grid(row=4, column=i*5-j, padx=5, pady=5, sticky="nsew")
        #####################

        ##### Team Boxes #####
        self.team_text = []
        self.pokemon_team_list = [[None for i in range(6)] for j in range(2)]
        self.team_buttons = [[], []]
        for team in range(2):
            self.team_text.append(tk.Label(self, text="TEAM %s" % str(team+1)))
            self.team_text[team].grid(row=5, column=team*4, columnspan=2, sticky="nsew")
            for row in range(3):
                for column in range(2):
                    x = (row * 2) + column
                    self.team_buttons[team].append(tk.Button(self, text="? ? ? ? ?", command=None))
                    self.team_buttons[team][x].grid(row=row+6, column=(team*4)+column, padx=5, pady=5, sticky="nsew")
        ######################

        ##### Settings #####
        self.settingsV1 = tk.Button(self, text="Draft Settings", command=lambda: self.controller.show_frame('DraftSettings'))
        self.settingsV1.grid(row=6, column=2, columnspan=2, padx=5, pady=5, sticky="nsew")
        self.settingsV2 = tk.Button(self, text="Generate Settings", command=lambda: self.controller.show_frame('GenerateSettings'))
        self.settingsV2.grid(row=7, column=2, columnspan=2, padx=5, pady=5, sticky="nsew")
        ######################

        ##### Start/Finish Buttons #####
        self.start_button = tk.Button(self, text="New Game", command=self.new_game)
        self.start_button.grid(row=8, column=2, padx=5, pady=5, sticky="nsew")
        self.finish_button = tk.Button(self, text="Get Sets", command=None)
        self.finish_button.grid(row=8, column=3, padx=5, pady=5, sticky="nsew")
        ################################

    def new_game(self):
        # reset private variables
        self.game_activated = True
        self.turn = 0
        self.pokemon_pool_list = []
        self.pokemon_ban_list = [[], []]
        self.pokemon_team_list = [[None for i in range(6)] for j in range(2)]
        self.pokemon_not_picked = [True for i in range(18)]

        temp_counter = 0
        while temp_counter < 18:
            temp_new_pokemon = random.choice(ALL_POKEMON)
            if (self.check_validity(temp_new_pokemon)):
                self.pokemon_pool_list.append(temp_new_pokemon)
                temp_counter += 1
        for pokemon in self.pokemon_pool_list:
            debug(pokemon.name)
        self.get_checks_and_counters()
        for i in range(18):
            self.pool_buttons[i].config(text=self.pokemon_pool_list[i].name,
                                        command=lambda i=i: self.add_to_team(i))

    def check_validity(self, pokemon):
        if ((pokemon in self.pokemon_pool_list) or
            (pokemon.name in [pool.name for pool in self.pokemon_pool_list]) or
            (pokemon.tier in [i.get() for i in self.pokemon_exclusion_tiers_singles]) or
            (pokemon.type[0] in [i.get() for i in self.pokemon_exclusion_types]) or
            (pokemon.type[1] and pokemon.type[1] in [i.get() for i in self.pokemon_exclusion_types]) or
            (self.check_valid_generation(pokemon)) or
            (self.check_valid_item(pokemon)) or
            (pokemon.tag in [i.get() for i in self.pokemon_exclusion_gimmicks])):
            return False
        else:
            return True

    def check_valid_generation(self, pokemon):
        dex_list = []
        for generation in [j.get() for j in self.pokemon_exclusion_generations]:
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
        if str(pokemon.dex) in dex_list:
            return True
        return False

    def check_valid_item(self, pokemon):
        item_list = []
        for item in [j.get() for j in self.pokemon_exclusion_items]:
            if item == 'Mega Stones':
                item_list.extend(MEGA_STONES)
            elif item == 'Z-Crystals':
                item_list.extend(Z_CRYSTALS)
            elif item == 'Berries':
                item_list.extend(BERRIES)
            elif item:
                item_list.append(item)
            else:
                continue
        if pokemon.item in item_list:
            return True
        return False

    def get_checks_and_counters(self):
        self.checks_and_counters = [[] for i in range(18)]
        for i in range(18):
            for j in range(18):
                if i != j:
                    attacking_type = self.pokemon_pool_list[j]
                    defending_type = self.pokemon_pool_list[i]
                    if type_logic(attacking_type, defending_type):
                        self.checks_and_counters[i].append(self.pokemon_pool_list[j].name)
            shuffle(self.checks_and_counters[i])

    def add_to_team(self, pool_number):
        if self.pokemon_not_picked[pool_number]:
            if self.turn < 12: # 12 == all pokemon picked for both teams
                self.pokemon_not_picked[pool_number] = False
                self.pool_buttons[pool_number].config(text="- - - - -", command=None)
                team_number = int(self.turn%2)
                slot_number = int(self.turn/2)
                self.pokemon_team_list[team_number][slot_number] = self.pokemon_pool_list[pool_number]
                self.team_buttons[team_number][slot_number].config(text=self.pokemon_pool_list[pool_number].name,
                                                                   command=lambda i=pool_number, j=team_number, k=slot_number: self.remove_from_team(i, j, k))
                self.update_turns()

    def remove_from_team(self, pool_number, team_number, slot_number):
        pokemon_name = self.pokemon_team_list[team_number][slot_number].name
        self.pokemon_not_picked[pool_number] = True
        self.pokemon_team_list[team_number][slot_number] = None
        self.pool_buttons[pool_number].config(text=pokemon_name, command=lambda i=pool_number: self.add_to_team(i))
        self.team_buttons[team_number][slot_number].config(text="? ? ? ? ?", command=None)
        self.update_turns()

    def update_turns(self):
        next_turn = 0
        for i in range(12):
            if not self.pokemon_team_list[int(i%2)][int(i/2)]:
                break
            next_turn += 1
        self.turn = next_turn
###############################################################################

###############################################################################
class DraftSettings(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

    def parent_page(self):
        return self.controller.pages['Draft']
###############################################################################

###############################################################################
class GenerateSettings(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.tier_text = tk.Label(self, text="Tiers (Singles)")
        self.tier_text.grid(row=1, column=0, rowspan=2, sticky="w")
        self.tier_buttons = []
        for i in range(len(TIERS_SINGLES)):
            self.tier_buttons.append(tk.Checkbutton(self, text=TIERS_SINGLES[i],
                                                    variable=self.parent_page().pokemon_exclusion_tiers_singles[i],
                                                    onvalue=TIERS_SINGLES[i],
                                                    offvalue=''))
            self.tier_buttons[i].grid(row=1+int(i/5), column=(i%5)+1, sticky="w")

        self.tier2_text = tk.Label(self, text="Tiers (Doubles)")
        self.tier2_text.grid(row=3, column=0, sticky="w")
        self.tier2_buttons = []
        for i in range(len(TIERS_DOUBLES)):
            self.tier2_buttons.append(tk.Checkbutton(self, text=TIERS_DOUBLES[i],
                                                    variable=self.parent_page().pokemon_exclusion_tiers_doubles[i],
                                                    onvalue=TIERS_DOUBLES[i],
                                                    offvalue=''))
            self.tier2_buttons[i].grid(row=3+int(i/5), column=(i%5)+1, sticky="w")

        self.gen_text = tk.Label(self, text="Generations")
        self.gen_text.grid(row=4, column=0, rowspan=2, sticky="w")
        self.gen_buttons = []
        for i in range(len(GENERATIONS)):
            self.gen_buttons.append(tk.Checkbutton(self, text=GENERATIONS[i],
                                                    variable=self.parent_page().pokemon_exclusion_generations[i],
                                                    onvalue=GENERATIONS[i],
                                                    offvalue=''))
            self.gen_buttons[i].grid(row=4+int(i/5), column=(i%5)+1, sticky="w")

        self.type_text = tk.Label(self, text="Types")
        self.type_text.grid(row=6, column=0, rowspan=4, sticky="w")
        self.type_buttons = []
        for i in range(len(TYPES)):
            self.type_buttons.append(tk.Checkbutton(self, text=TYPES[i],
                                                    variable=self.parent_page().pokemon_exclusion_types[i],
                                                    onvalue=TYPES[i],
                                                    offvalue=''))
            self.type_buttons[i].grid(row=6+int(i/5), column=(i%5)+1, sticky="w")

        self.item_text = tk.Label(self, text="Items")
        self.item_text.grid(row=10, column=0, rowspan=2, sticky="w")
        self.item_buttons = []
        for i in range(len(ITEMS)):
            self.item_buttons.append(tk.Checkbutton(self, text=ITEMS[i],
                                                    variable=self.parent_page().pokemon_exclusion_items[i],
                                                    onvalue=ITEMS[i],
                                                    offvalue=''))
            self.item_buttons[i].grid(row=10+int(i/5), column=(i%5)+1, sticky="w")

        self.gimmick_text = tk.Label(self, text="Gimmicks")
        self.gimmick_text.grid(row=12, column=0, rowspan=2, sticky="w")
        self.gimmick_buttons = []
        for i in range(len(GIMMICKS)):
            self.gimmick_buttons.append(tk.Checkbutton(self, text=GIMMICKS[i],
                                                    variable=self.parent_page().pokemon_exclusion_gimmicks[i],
                                                    onvalue=GIMMICKS[i],
                                                    offvalue=''))
            self.gimmick_buttons[i].grid(row=12+int(i/5), column=(i%5)+1, sticky="w")

        self.usage_text = tk.Label(self, text="Usage")
        self.usage_text.grid(row=14, column=0, sticky="w")

        self.back_button = tk.Button(self, text="Back", command=self.validate)
        self.back_button.grid(row=15, column=2, columnspan=2, padx=5, pady=5, sticky="nsew")

    def validate(self):
        temp_exclude_tiers = list(filter(None, [i.get() for i in self.parent_page().pokemon_exclusion_tiers_singles]))
        temp_exclude_types = list(filter(None, [i.get() for i in self.parent_page().pokemon_exclusion_types]))
        temp_exclude_gimmicks = list(filter(None, [i.get() for i in self.parent_page().pokemon_exclusion_gimmicks]))
        temp_counter = 0
        temp_list = []
        for pokemon in ALL_POKEMON:
            if ((pokemon.name in temp_list) or
                (pokemon.tier in temp_exclude_tiers) or
                (pokemon.type[0] in temp_exclude_types) or
                (pokemon.type[1] and pokemon.type[1] in temp_exclude_types) or
                (self.parent_page().check_valid_generation(pokemon)) or
                (self.parent_page().check_valid_item(pokemon)) or
                (pokemon.tag in temp_exclude_gimmicks)):
                continue
            else:
                temp_list.append(pokemon.name)
                temp_counter += 1
            if temp_counter >= 18:
                break
        if temp_counter >= 18:
            self.controller.show_frame('Draft')
        else:
            top = tk.Toplevel(self.controller)
            
            # warning menu

    def parent_page(self):
        return self.controller.pages['Draft']
###############################################################################

###############################################################################
class Random(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
###############################################################################

###############################################################################
class Banners(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
###############################################################################

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
