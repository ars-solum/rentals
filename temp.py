try:
    import Tkinter as tk
    from Tkinter import ttk
except ImportError:
    import tkinter as tk
    from tkinter import ttk
from PIL import Image, ImageTk

import os
import csv
import time
import random
from random import shuffle


from Pokemon import *

ROOT = os.path.dirname(os.path.realpath(__file__))

TIERS_SINGLES = ['LC', 'LC Uber', 'Untiered', 'NFE', 'PU', 'NU', 'RU', 'UU', 'OU', 'Uber']
TIERS_DOUBLES = ['LC', 'Untiered', 'DUU', 'DOU', 'DUber']
GENERATIONS = ['Kanto', 'Johto', 'Hoenn', 'Sinnoh', 'Unova', 'Kalos', 'Alola']
TYPES = ['Bug', 'Dark', 'Dragon', 'Electric', 'Fairy', 'Fighting', 'Fire', 'Flying', 'Ghost', 'Grass', 'Ground', 'Ice', 'Normal', 'Poison', 'Psychic', 'Rock', 'Steel', 'Water']
ITEMS = ['Mega Stones', 'Z-Crystals', 'Berries', 'Choice Band', 'Choice Scarf', 'Choice Specs', 'Leftovers', 'Life Orb']
GIMMICKS = ['Sun', 'Rain', 'Sand', 'Hail', 'Trick Room', 'Baton Pass', 'E-Terrain', 'G-Terrain', 'M-Terrain', 'P-Terrain']

###############################################################################
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

        for Class in (Draft, Random, DraftSettings, GenerateSettings, RandomSettings, RandomGenerateSettings, Store):
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

###############################################################################
class Sidebar(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.label_text = ['Battle', 'League']
        self.labels = []
        self.button_text = [['Draft', 'Random'], ['Store']] # remove after getting images
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
        self.battle_mode = tk.StringVar()
        self.battle_mode.set('Singles')
        self.draft_mode = tk.StringVar()
        self.draft_mode.set('Standard')
        self.ban_phase_finished = False
        self.ban_phase_1_finished = False
        self.ban_phase_2_finished = False
        self.ban_number = tk.IntVar()
        self.ban_number.set(0)
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
        self.pokemon_ban_list = [[None, None], [None, None]]
        self.ban_text = tk.Label(self, text="BANS")
        self.ban_text.grid(row=4, column=2, columnspan=2, sticky="nsew")
        self.ban_buttons = [[], []]
        for i in range(2):
            for j in range(2):
                self.ban_buttons[i].append(tk.Button(self, text="? ? ? ? ?", state="disabled", command=None))
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
        self.mode_text = tk.Label(self, text="%s Draft" % self.draft_mode.get())
        self.mode_text.grid(row=5, column=2, columnspan=2, padx=5, pady=5, sticky="nsew")
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
        self.pokemon_ban_list = [[None, None], [None, None]]
        self.ban_phase_finished = False
        self.ban_phase_1_finished = False
        self.ban_phase_2_finished = False
        self.pokemon_team_list = [[None for i in range(6)] for j in range(2)]
        self.pokemon_not_picked = [True for i in range(18)]

        temp_exclude_tiers = list(filter(None, [i.get() for i in self.pokemon_exclusion_tiers_singles]))
        temp_exclude_types = list(filter(None, [i.get() for i in self.pokemon_exclusion_types]))
        temp_exclude_gimmicks = list(filter(None, [i.get() for i in self.pokemon_exclusion_gimmicks]))
        temp_list = []
        for pokemon in ALL_POKEMON:
            if ((pokemon.name in temp_list) or
                (pokemon.tier in temp_exclude_tiers) or
                (pokemon.type[0] in temp_exclude_types) or
                (pokemon.type[1] and pokemon.type[1] in temp_exclude_types) or
                (check_valid_generation(self, pokemon)) or
                (check_valid_item(self, pokemon)) or
                (pokemon.tag in temp_exclude_gimmicks)):
                continue
            else:
                temp_list.append(pokemon)
        temp_counter = 0
        while temp_counter < 18:
            temp_new_pokemon = random.choice(temp_list)
            if (check_validity(self, temp_new_pokemon)):
                self.pokemon_pool_list.append(temp_new_pokemon)
                temp_counter += 1

        print([i.name for i in self.pokemon_pool_list])
        print()

        self.get_checks_and_counters()

        for i in range(18):
            self.pool_buttons[i].config(text=self.pokemon_pool_list[i].name, command=lambda i=i: self.add_to_team(i))
        for i in range(2):
            for j in range(2):
                self.ban_buttons[i][j].config(text="? ? ? ? ?", command=None)
            for j in range(6):
                self.team_buttons[i][j].config(text="? ? ? ? ?", command=None)
        self.finish_button.config(command=None)

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
        if self.game_activated:
            if self.pokemon_not_picked[pool_number]:
                if self.turn < 12:
                    self.pokemon_not_picked[pool_number] = False
                    self.pool_buttons[pool_number].config(text="- - - - -", command=None)
                    if self.ban_number.get() != 0 and not self.ban_phase_finished:
                        self.ban_pokemon(pool_number)
                    else:
                        if self.draft_mode.get() == 'Standard':
                            team_number = int(self.turn%2)
                            slot_number = int(self.turn/2)
                        if self.draft_mode.get() == 'Nemesis':
                            team_number = int((self.turn+1)%2)
                            slot_number = int(self.turn/2)
                        if self.draft_mode.get() == 'First Pick':
                            if self.turn <= 1:
                                team_number = 0
                                slot_number = self.turn
                            elif 6 <= self.turn <= 9:
                                team_number = 0
                                slot_number = self.turn - 4
                            elif 2 <= self.turn <= 5:
                                team_number = 1
                                slot_number = self.turn - 2
                            elif 10 <= self.turn <= 11:
                                team_number = 1
                                slot_number = self.turn - 6
                        self.pokemon_team_list[team_number][slot_number] = self.pokemon_pool_list[pool_number]
                        self.team_buttons[team_number][slot_number].config(text=self.pokemon_pool_list[pool_number].name,
                                                                           command=lambda i=pool_number, j=team_number, k=slot_number: self.remove_from_team(i, j, k))
                        self.update_turns()

    def remove_from_team(self, pool_number, team_number, slot_number):
        if self.game_activated:
            pokemon_name = self.pokemon_team_list[team_number][slot_number].name
            self.pokemon_not_picked[pool_number] = True
            self.pokemon_team_list[team_number][slot_number] = None
            self.pool_buttons[pool_number].config(text=pokemon_name, command=lambda i=pool_number: self.add_to_team(i))
            self.team_buttons[team_number][slot_number].config(text="? ? ? ? ?", command=None)
            self.update_turns()

    def ban_pokemon(self, pool_number):
        # add pokemon to proper banlist
        temp_done = False
        for i in range(self.ban_number.get()):
            for j in range(2):
                if not self.pokemon_ban_list[1-j][i]:
                    self.pokemon_ban_list[1-j][i] = self.pokemon_pool_list[pool_number]
                    self.ban_buttons[1-j][i].config(text=self.pokemon_pool_list[pool_number].name,
                                                    command=None)
                    temp_done = True
                    break
            if temp_done:
                break
        # end the ban phase
        if ((self.turn == 0 and self.pokemon_ban_list[0][0]) and
            (self.turn == 0 and self.pokemon_ban_list[1][0])):
            self.ban_phase_1_finished = True
        if (((self.turn == 8 and self.pokemon_ban_list[0][1] and self.draft_mode.get() == 'First Pick') and
             (self.turn == 8 and self.pokemon_ban_list[1][1] and self.draft_mode.get() == 'First Pick')) or
             ((self.turn == 6 and self.pokemon_ban_list[0][1] and self.draft_mode.get() != 'First Pick') and
             (self.turn == 6 and self.pokemon_ban_list[1][1] and self.draft_mode.get() != 'First Pick'))):
            self.ban_phase_2_finished = True
        if ((self.turn == 0 and self.ban_phase_1_finished) or
            ((self.turn == 8 and self.ban_phase_2_finished and self.draft_mode.get() == 'First Pick') or
              (self.turn == 6 and self.ban_phase_2_finished and self.draft_mode.get() != 'First Pick'))):
            self.ban_phase_finished = True

    def update_turns(self):
        next_turn = 0
        if self.draft_mode.get() == 'First Pick':
            fp_team_order = [0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1]
            fp_slot_order = [0, 1, 0, 1, 2, 3, 2, 3, 4, 5, 4, 5]
            for i in range(12):
                if not self.pokemon_team_list[fp_team_order[i]][fp_slot_order[i]]:
                    break
                next_turn += 1
        else:
            for i in range(12):
                if self.draft_mode.get() == 'Standard':
                    if not self.pokemon_team_list[int(i%2)][int(i/2)]:
                        break
                if self.draft_mode.get() == 'Nemesis':
                    if not self.pokemon_team_list[int((i+1)%2)][int(i/2)]:
                        break
                next_turn += 1
        self.turn = next_turn
        if ((self.turn == 8 and self.ban_number.get() == 2 and self.draft_mode.get() == 'First Pick') or
            (self.turn == 6 and self.ban_number.get() == 2 and self.draft_mode.get() != 'First Pick')):
            self.ban_phase_finished = False
        if self.turn >= 12:
            self.finish_button.config(command=lambda: get_sets(self))
###############################################################################

###############################################################################
class DraftSettings(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.battle_mode_text = tk.Label(self, text="Battle Mode")
        self.battle_mode_text.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.battle_mode_buttons = []
        battle_modes = ['Singles', 'Doubles', 'SRL']
        for i in range(len(battle_modes)):
            self.battle_mode_buttons.append(tk.Radiobutton(self, text=battle_modes[i],
                                                           variable=self.parent_page().battle_mode,
                                                           indicatoron=0,
                                                           width=10,
                                                           value=battle_modes[i]))
            self.battle_mode_buttons[i].grid(row=1+int(i/5), column=(i%5)+1, padx=5, pady=5, sticky="nsew")

        self.draft_mode_text = tk.Label(self, text="Draft Mode")
        self.draft_mode_text.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.draft_mode_buttons = []
        draft_modes = ['Standard', 'Nemesis', 'First Pick']
        for i in range(len(draft_modes)):
            self.draft_mode_buttons.append(tk.Radiobutton(self, text=draft_modes[i],
                                                           variable=self.parent_page().draft_mode,
                                                           indicatoron=0,
                                                           width=10,
                                                           value=draft_modes[i]))
            self.draft_mode_buttons[i].grid(row=2+int(i/5), column=(i%5)+1, padx=5, pady=5, sticky="nsew")

        self.ban_number_text = tk.Label(self, text="Bans")
        self.ban_number_text.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.ban_number_buttons = []
        ban_number = [0, 1, 2]
        for i in range(len(ban_number)):
            self.ban_number_buttons.append(tk.Radiobutton(self, text=ban_number[i],
                                                           variable=self.parent_page().ban_number,
                                                           indicatoron=0,
                                                           width=10,
                                                           value=ban_number[i],
                                                           command=self.activate_bans))
            self.ban_number_buttons[i].grid(row=3+int(i/5), column=(i%5)+1, padx=5, pady=5, sticky="nsew")

        self.back_button = tk.Button(self, text="Back", command=self.exit)
        self.back_button.grid(row=15, column=1, columnspan=2, padx=5, pady=5, sticky="nsew")

        for i in range(8):
            self.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.grid_columnconfigure(i, weight=1)

    def activate_bans(self):
        for i in range(2):
            for j in range(0, self.parent_page().ban_number.get()):
                self.parent_page().ban_buttons[i][j].config(state="normal", command=None)
            for j in range(self.parent_page().ban_number.get(), 2):
                self.parent_page().ban_buttons[i][j].config(state="disabled", command=None)
        self.parent_page().ban_phase_finished = False

    def parent_page(self):
        return self.controller.pages['Draft']

    def exit(self):
        clean_up(self)
        self.controller.show_frame('Draft')
###############################################################################

###############################################################################
class GenerateSettings(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        setup_settings(self)

        self.back_button = tk.Button(self, text="Back", command=self.validate)
        self.back_button.grid(row=15, column=2, columnspan=2, padx=5, pady=5, sticky="nsew")

    def validate(self):
        temp_exclude_tiers = list(filter(None, [i.get() for i in self.parent_page().pokemon_exclusion_tiers_singles]))
        temp_exclude_types = list(filter(None, [i.get() for i in self.parent_page().pokemon_exclusion_types]))
        temp_exclude_gimmicks = list(filter(None, [i.get() for i in self.parent_page().pokemon_exclusion_gimmicks]))
        temp_counter = 0
        temp_list = []
        for pokemon in ALL_POKEMON:
            if ((pokemon.name in [i.name for i in temp_list]) or
                (pokemon.dex in [j.dex for j in temp_list]) or
                (pokemon.tier in temp_exclude_tiers) or
                (pokemon.type[0] in temp_exclude_types) or
                (pokemon.type[1] and pokemon.type[1] in temp_exclude_types) or
                (check_valid_generation(self.parent_page(), pokemon)) or
                (check_valid_item(self.parent_page(), pokemon)) or
                (pokemon.tag in temp_exclude_gimmicks)):
                continue
            else:
                temp_list.append(pokemon)
                temp_counter += 1
        if temp_counter >= 18:
            clean_up(self)
            self.controller.show_frame('Draft')
        else:
            top = tk.Toplevel(self.controller)
            top.grab_set()
            message = tk.Label(top, text="Not enough Pokemon fit the criteria you have selected.\nPlease remove some restrictions.")
            message.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
            back_button = tk.Button(top, text="Ok", command=top.destroy)
            back_button.grid(row=1, column=0, padx=100, pady=5, sticky="nsew")

    def parent_page(self):
        return self.controller.pages['Draft']
###############################################################################

###############################################################################
class Random(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        ##### Private Variables #####
        # misc. variables
        self.alpha = 0
        self.temp_list = []
        self.battle_mode = tk.StringVar()
        self.battle_mode.set('Singles')
        self.theme = tk.StringVar()
        self.theme.set('Random')
        for i in range(6):
            self.grid_columnconfigure(i, weight=1)
        for i in range(8):
            self.grid_rowconfigure(i, weight=1)
        # filter/exclusion variables
        self.pokemon_exclusion_tiers_singles = [tk.StringVar() for i in range(len(TIERS_SINGLES))]
        self.pokemon_exclusion_tiers_doubles = [tk.StringVar() for i in range(len(TIERS_DOUBLES))]
        self.pokemon_exclusion_generations = [tk.StringVar() for i in range(len(GENERATIONS))]
        self.pokemon_exclusion_types = [tk.StringVar() for i in range(len(TYPES))]
        self.pokemon_exclusion_items = [tk.StringVar() for i in range(len(ITEMS))]
        self.pokemon_exclusion_gimmicks = [tk.StringVar() for i in range(len(GIMMICKS))]
        self.pokemon_exclusion_usages = []

        ##### Team Boxes #####
        self.team_text = []
        self.pokemon_team_list = [[None for i in range(6)] for j in range(2)]
        self.team_buttons = [[], []]
        for team in range(2):
            self.team_text.append(tk.Label(self, text="TEAM %s" % str(team+1)))
            self.team_text[team].grid(row=1, column=team*4, columnspan=2, sticky="nsew")
            for row in range(3):
                for column in range(2):
                    x = (row * 2) + column
                    self.team_buttons[team].append(tk.Button(self, text="? ? ? ? ?", command=None))
                    self.team_buttons[team][x].grid(row=row+2, column=(team*4)+column, padx=5, pady=5, sticky="nsew")
        ######################

        ##### Settings #####
        self.mode_text = tk.Label(self, text="Random Battle")
        self.mode_text.grid(row=2, column=2, columnspan=2, padx=5, pady=5, sticky="nsew")
        self.settingsV1 = tk.Button(self, text="Random Settings", command=lambda: self.controller.show_frame('RandomSettings'))
        self.settingsV1.grid(row=3, column=2, columnspan=2, padx=5, pady=5, sticky="nsew")
        self.settingsV2 = tk.Button(self, text="Generate Settings", command=lambda: self.controller.show_frame('RandomGenerateSettings'))
        self.settingsV2.grid(row=4, column=2, columnspan=2, padx=5, pady=5, sticky="nsew")
        ######################

        ##### Start/Finish Buttons #####
        self.start_button = tk.Button(self, text="New Game", command=self.new_game)
        self.start_button.grid(row=5, column=2, padx=5, pady=5, sticky="nsew")
        self.finish_button = tk.Button(self, text="Get Sets", command=None)
        self.finish_button.grid(row=5, column=3, padx=5, pady=5, sticky="nsew")
        ################################

    def new_game(self):
        # reset private variables
        self.game_activated = True
        self.pokemon_team_list = [[None for i in range(6)] for j in range(2)]

        temp_exclude_tiers = list(filter(None, [i.get() for i in self.pokemon_exclusion_tiers_singles]))
        temp_exclude_types = list(filter(None, [i.get() for i in self.pokemon_exclusion_types]))
        temp_exclude_gimmicks = list(filter(None, [i.get() for i in self.pokemon_exclusion_gimmicks]))
        self.temp_list = []
        for pokemon in ALL_POKEMON:
            if ((pokemon.name in self.temp_list) or
                (pokemon.tier in temp_exclude_tiers) or
                (pokemon.type[0] in temp_exclude_types) or
                (pokemon.type[1] and pokemon.type[1] in temp_exclude_types) or
                (check_valid_generation(self, pokemon)) or
                (check_valid_item(self, pokemon)) or
                (pokemon.tag in temp_exclude_gimmicks)):
                continue
            else:
                self.temp_list.append(pokemon)
        temp_counter = 0
        for i in range(2):
            while temp_counter < 6:
                if i == 1 and self.theme.get() == 'Balanced':
                    temp_new_pokemon = random.choice(self.temp_list)
                    if ((check_validity(self, temp_new_pokemon, i)) and
                        (temp_new_pokemon.tier == self.pokemon_team_list[0][temp_counter].tier)):
                            self.pokemon_team_list[i][temp_counter] = temp_new_pokemon
                            temp_counter += 1
                else:
                    temp_new_pokemon = random.choice(self.temp_list)
                    if (check_validity(self, temp_new_pokemon, i)):
                        self.pokemon_team_list[i][temp_counter] = temp_new_pokemon
                        temp_counter += 1
            temp_counter = 0

        print([i.name for i in self.pokemon_team_list[0]])
        print([i.tier for i in self.pokemon_team_list[0]])
        print()
        print([i.name for i in self.pokemon_team_list[1]])
        print([i.tier for i in self.pokemon_team_list[1]])
        print()

        for i in range(2):
            for j in range(6):
                self.team_buttons[i][j].config(text=self.pokemon_team_list[i][j].name, command=lambda i=i, j=j: self.reroll(i, j))
        self.finish_button.config(command=lambda: get_sets(self))

    def reroll(self, team, slot):
        while True:
            temp_new_pokemon = random.choice(self.temp_list)
            if (check_validity(self, temp_new_pokemon, team)):
                self.pokemon_team_list[team][slot] = temp_new_pokemon
                self.team_buttons[team][slot].config(text=temp_new_pokemon.name)
                break
###############################################################################

###############################################################################
class RandomSettings(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.battle_mode_text = tk.Label(self, text="Battle Mode")
        self.battle_mode_text.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.battle_mode_buttons = []
        battle_modes = ['Singles', 'Doubles', 'SRL']
        for i in range(len(battle_modes)):
            self.battle_mode_buttons.append(tk.Radiobutton(self, text=battle_modes[i],
                                                           variable=self.parent_page().battle_mode,
                                                           indicatoron=0,
                                                           width=10,
                                                           value=battle_modes[i]))
            self.battle_mode_buttons[i].grid(row=1+int(i/5), column=(i%5)+1, padx=5, pady=5, sticky="nsew")

        self.back_button = tk.Button(self, text="Back", command=self.exit)
        self.back_button.grid(row=15, column=1, columnspan=2, padx=5, pady=5, sticky="nsew")

        self.theme_text = tk.Label(self, text="Theme")
        self.theme_text.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.theme_buttons = []
        themes = ['Random', 'Balanced', 'Monotype']
        for i in range(len(themes)):
            self.theme_buttons.append(tk.Radiobutton(self, text=themes[i],
                                                           variable=self.parent_page().theme,
                                                           indicatoron=0,
                                                           width=10,
                                                           value=themes[i]))
            self.theme_buttons[i].grid(row=2+int(i/5), column=(i%5)+1, padx=5, pady=5, sticky="nsew")


        for i in range(6):
            self.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.grid_columnconfigure(i, weight=1)

    def parent_page(self):
        return self.controller.pages['Random']

    def exit(self):
        clean_up(self)
        self.controller.show_frame('Random')
###############################################################################

###############################################################################
class RandomGenerateSettings(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        setup_settings(self)

        self.back_button = tk.Button(self, text="Back", command=self.validate)
        self.back_button.grid(row=15, column=2, columnspan=2, padx=5, pady=5, sticky="nsew")

    def validate(self):
        temp_exclude_tiers = list(filter(None, [i.get() for i in self.parent_page().pokemon_exclusion_tiers_singles]))
        temp_exclude_types = list(filter(None, [i.get() for i in self.parent_page().pokemon_exclusion_types]))
        temp_exclude_gimmicks = list(filter(None, [i.get() for i in self.parent_page().pokemon_exclusion_gimmicks]))
        temp_counter = 0
        temp_list = []
        for pokemon in ALL_POKEMON:
            if ((pokemon.name in [i.name for i in temp_list]) or
                (pokemon.dex in [j.dex for j in temp_list]) or
                (pokemon.tier in temp_exclude_tiers) or
                (pokemon.type[0] in temp_exclude_types) or
                (pokemon.type[1] and pokemon.type[1] in temp_exclude_types) or
                (check_valid_generation(self.parent_page(), pokemon)) or
                (check_valid_item(self.parent_page(), pokemon)) or
                (pokemon.tag in temp_exclude_gimmicks)):
                continue
            else:
                temp_list.append(pokemon)
                temp_counter += 1
        if temp_counter >= 18:
            clean_up(self)
            self.controller.show_frame('Random')
        else:
            top = tk.Toplevel(self.controller)
            top.grab_set()
            message = tk.Label(top, text="Not enough Pokemon fit the criteria you have selected.\nPlease remove some restrictions.")
            message.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
            back_button = tk.Button(top, text="Ok", command=top.destroy)
            back_button.grid(row=1, column=0, padx=100, pady=5, sticky="nsew")

    def parent_page(self):
        return self.controller.pages['Random']
###############################################################################

###############################################################################
class Store(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.banner_num = 1
        self.currentPlayer = tk.StringVar()
        self.currentPlayer.set(playerNames[0])

        self.banner_image = tk.Label(self, text="Banner %d Image" % self.banner_num)
        self.banner_image.grid(row=0, column=0, rowspan=2, columnspan=3, sticky="nsew")
        self.banner_info_text = tk.Label(self, text="Banner Info")
        self.banner_info_text.grid(row=2, column=1, sticky="nsew")

        self.scrollframe = tk.LabelFrame(self, text="Banner Info", border=2)
        self.scrollframe.grid(row=3, column=0, rowspan=5, columnspan=3, padx=5, pady=5, sticky="nsew")
        self.container = tk.Canvas(self.scrollframe, scrollregion=(0,0,400,400))
        self.scrollbar = ttk.Scrollbar(self.scrollframe, orient='vertical', command=self.container.yview)
        self.container.config(yscrollcommand=self.scrollbar.set)
        self.container.bind('<Enter>', self._on_mousewheel)
        self.container.bind('<Leave>', self._off_mousewheel)
        self.scrollbar.pack(side='right', fill='y')
        self.container.pack(side='left', expand=True, fill='both')

        self.pokemon_icons = [[None for i in range(5)] for j in range(8)]
        for i in range(8):
            for j in range(5):
                x = (i*5)+j
                self.pokemon_icons[i][j] = tk.Button(self.container, text="Pokemon %d" % x, command=None)
                self.container.create_window((j*100)+40, (i*50)+20, window=self.pokemon_icons[i][j])
                #####################################
        self.pull_result = tk.Label(self, text="? ? ?", command=None)
        self.pull_result.grid(row=8, column=0, padx=5, pady=5, sticky="nsew")
        self.player_name = tk.OptionMenu(self, self.currentPlayer, *playerNames, command=self.update_player_info)
        self.player_name.grid(row=8, column=1, padx=5, pady=5, sticky="nsew")
        self.pull_button = tk.Button(self, text="? ? ?", command=None)
        self.pull_button.grid(row=8, column=2, padx=5, pady=5, sticky="nsew")

        for i in range(9):
            self.grid_rowconfigure(i, weight=1)
        for i in range(3):
            self.grid_columnconfigure(i, weight=1)

    def _on_mousewheel(self, event):
        self.container.bind_all('<MouseWheel>', self._scroll)
    def _off_mousewheel(self, event):
        self.container.unbind_all('<MouseWheel>')
    def _scroll(self, event):
        self.container.yview_scroll(int(-1*(event.delta/120)), "units")

    def


###############################################################################

def check_validity(self, pokemon, i=0):
    if hasattr(self, 'pokemon_pool_list'):
        if ((pokemon in self.pokemon_pool_list) or
            (pokemon.name in [pool.name for pool in self.pokemon_pool_list]) or
            (pokemon.tier in list(filter(None, [i.get() for i in self.pokemon_exclusion_tiers_singles]))) or
            (pokemon.type[0] in list(filter(None, [i.get() for i in self.pokemon_exclusion_types]))) or
            (pokemon.type[1] and pokemon.type[1] in list(filter(None, [i.get() for i in self.pokemon_exclusion_types]))) or
            (check_valid_generation(self, pokemon)) or
            (check_valid_item(self, pokemon)) or
            (pokemon.tag in list(filter(None, [i.get() for i in self.pokemon_exclusion_gimmicks])))):
            return False
        return True
    else:
        if ((pokemon in self.pokemon_team_list[i]) or
            (pokemon.name in [slot.name for slot in self.pokemon_team_list[i] if slot != None]) or
            (pokemon.tier in list(filter(None, [i.get() for i in self.pokemon_exclusion_tiers_singles]))) or
            (pokemon.type[0] in list(filter(None, [i.get() for i in self.pokemon_exclusion_types]))) or
            (pokemon.type[1] and pokemon.type[1] in list(filter(None, [i.get() for i in self.pokemon_exclusion_types]))) or
            (check_valid_generation(self, pokemon)) or
            (check_valid_item(self, pokemon)) or
            (pokemon.tag in list(filter(None, [i.get() for i in self.pokemon_exclusion_gimmicks])))):
            return False
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
    for item in list(filter(None, [i.get() for i in self.pokemon_exclusion_items])):
        if item == 'Mega Stones':
            item_list.extend(MEGA_STONES)
        elif item == 'Z-Crystals':
            item_list.extend(Z_CRYSTALS)
        elif item == 'Berries':
            item_list.extend(BERRIES)
        else:
            item_list.append(item)
    if pokemon.item in item_list:
        return True
    return False

def get_sets(self):
    self.controller.clipboard_clear()
    sets = ''
    for team in self.pokemon_team_list:
        sets += '====================\n'
        for pokemon in team:
            if pokemon.item:
                sets += pokemon.name + ' @ ' + pokemon.item + '\n'
            else:
                sets += 'pokemon.name\n'
            if 'LC' in pokemon.tier:
                sets += 'Level: 5\n'
            sets += 'Ability: ' + pokemon.ability + '\n'
            sets += 'EVs: ' + pokemon.evSpread + '\n'
            sets += pokemon.nature + ' Nature\n'
            if pokemon.ivSpread:
                sets += 'IVs: ' + pokemon.ivSpread + '\n'
            for move in pokemon.moves:
                if move:
                    sets += '- ' + move + '\n'
            sets += '\n'
        sets += '\n'
    self.controller.clipboard_append(sets)
    self.update_statistics(self)

def update_statistics(self):
    if hasattr(self, 'pokemon_ban_list'):
        for team in self.pokemon_ban_list:
            for pokemon in team:
                if pokemon:
                    pokemon.banned += 1
    if hasattr(self, 'pokemon_pool_list'):
        for pokemon in self.pokemon_pool_list:
            if self.draft_mode.get() == 'Nemesis':
                pokemon.generated_nemesis += 1
            else:
                pokemon.generated_draft += 1
    for team in self.pokemon_team_list:
        for pokemon in team:
            if hasattr(self, 'draft_mode'):
                if self.draft_mode.get() == 'Nemesis':
                    pokemon.picked_nemesis += 1
                else:
                    pokemon.picked_draft += 1
            else:
                pokemon.generated_random += 1
    with open('main_database_copy.csv', 'w') as fileName:
        writer = csv.writer(fileName, delimiter=',')
        writer.writerow(['POKEMON', 'DEX', 'TYPE 1', 'TYPE 2', 'TIER',
                         'RARITY', 'TAG', 'ITEM', 'ABILITY', 'EV SPREAD',
                         'NATURE', 'IV SPREAD', 'MOVE 1', 'MOVE 2', 'MOVE 3',
                         'MOVE 4', 'STATUS', 'GENERATED (D)', 'GENERATED (N)',
                         'GENERATED (R)', 'PICKED (D)', 'PICKED (N)', 'BANNED'])
        for pokemon in ALL_POKEMON:
            writer.writerow([pokemon.name, pokemon.dex, pokemon.type[0], pokemon.type[1],
                             pokemon.tier, pokemon.rarity, pokemon.tag, pokemon.item,
                             pokemon.ability, pokemon.evSpread, pokemon.nature,
                             pokemon.ivSpread, pokemon.moves[0], pokemon.moves[1],
                             pokemon.moves[2], pokemon.moves[3], pokemon.status,
                             str(pokemon.generated_draft), str(pokemon.generated_nemesis),
                             str(pokemon.generated_random), str(pokemon.picked_draft),
                             str(pokemon.picked_nemesis), str(pokemon.banned)])

def clean_up(self):
    if hasattr(self.parent_page(), 'game_activated'):
        self.parent_page().game_activated = False
    if hasattr(self.parent_page(), 'turn'):
        self.parent_page().turn = 0
    if hasattr(self.parent_page(), 'pokemon_pool_list'):
        self.parent_page().pokemon_pool_list = []
        for i in range(18):
            self.parent_page().pool_buttons[i].config(text="? ? ? ? ?", command=None)
    if hasattr(self.parent_page(), 'pokemon_ban_list'):
        self.parent_page().pokemon_ban_list = [[None, None], [None, None]]
    if hasattr(self.parent_page(), 'ban_phase_finished'):
        self.parent_page().ban_phase_finished = False
        self.parent_page().ban_phase_1_finished = False
        self.parent_page().ban_phase_2_finished = False
    self.parent_page().pokemon_team_list = [[None for i in range(6)] for j in range(2)]
    if hasattr(self.parent_page(), 'pokemon_not_picked'):
        self.parent_page().pokemon_not_picked = [True for i in range(18)]
    for i in range(2):
        if hasattr(self.parent_page(), 'ban_buttons'):
            for j in range(2):
                self.parent_page().ban_buttons[i][j].config(text="? ? ? ? ?", command=None)
        for j in range(6):
            self.parent_page().team_buttons[i][j].config(text="? ? ? ? ?", command=None)
    if hasattr(self.parent_page(), 'mode_text'):
        if hasattr(self, 'draft_mode_buttons'):
            self.parent_page().mode_text.config(text="%s Draft" % self.parent_page().draft_mode.get())
        if hasattr(self, 'theme_buttons'):
            self.parent_page().mode_text.config(text="%s Battle" % self.parent_page().theme.get())

def setup_settings(self):
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

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
