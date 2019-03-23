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
MEDIA = os.path.join(ROOT, 'media')
COMMON = os.path.join(MEDIA, 'Common')
IMG_PKMN_DIR = os.path.join(MEDIA, 'pokemon')
PLAYER_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'players')

class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.side_frame = tk.Frame(self)
        self.side_frame.grid(row=0, column=0, sticky="nsew")

        self.main_frame = tk.Frame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew")

        self.sidebar = Sidebar(parent=self.side_frame, controller=self)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        self.img_type = ['inactive', 'active', 'unknown', 'banned', 'picked']
        self.img_blank_base = {
            'active': RGBAImage2(os.path.join(COMMON, 'button_active_Blank.png')),
            'inactive': RGBAImage2(os.path.join(COMMON, 'button_inactive_Blank.png'))}
        self.img_border = {
            'Standard': RGBAImage2(os.path.join(COMMON, 'border_Standard.png')),
            'Nemesis': RGBAImage2(os.path.join(COMMON, 'border_Nemesis.png')),
            'Random': RGBAImage2(os.path.join(COMMON, 'border_Random.png')),
            'COMMON': RGBAImage2(os.path.join(COMMON, 'border_COMMON.png')),
            'RARE': RGBAImage2(os.path.join(COMMON, 'border_RARE.png')),
            'ULTRA-RARE': RGBAImage2(os.path.join(COMMON, 'border_ULTRA-RARE.png'))}
        self.img_blank_base['inactive'].paste(self.img_border['Standard'],
                                              (0, 0),
                                              self.img_border['Standard'])
        self.img_blank_base['active'].paste(self.img_border['Standard'],
                                            (0, 0),
                                            self.img_border['Standard'])
        self.img_blank = [ImageTk.PhotoImage(self.img_blank_base['inactive']),
                          ImageTk.PhotoImage(self.img_blank_base['active'])]

        self.pages = {}

        for Class in (Draft, Random, DraftSettings, DraftGenerateSettings,
                      RandomSettings, RandomGenerateSettings, Store,
                      PlayerManagement):
            page_name = Class.__name__
            frame = Class(parent=self.main_frame, controller=self)
            self.pages[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame('Draft')

        self.sidebar.start_button.config(command=self.pages['Draft'].new_game)

        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

    def show_frame(self, page_name):
        if page_name == 'Draft' or page_name == 'Random':
            self.sidebar.settingsV1.config(state='normal',
                command=lambda:self.show_frame('%sSettings' % page_name))
            self.sidebar.settingsV2.config(state='normal',
                command=lambda:self.show_frame('%sGenerateSettings' % page_name))
            self.sidebar.start_button.config(state='normal',
                command=self.pages[page_name].new_game)
            if self.pages[page_name].game_activated == False:
                self.sidebar.finish_button.config(state='disabled')
            else:
                self.sidebar.finish_button.config(state='normal')
        else:
            self.sidebar.settingsV1.config(state='disabled')
            self.sidebar.settingsV2.config(state='disabled')
            self.sidebar.start_button.config(state='disabled')
            self.sidebar.finish_button.config(state='disabled')
        frame = self.pages[page_name]
        frame.tkraise()


class Sidebar(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        for i in range(10):
            self.grid_rowconfigure(i, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.label_text = ['Battle', 'League']
        self.labels = []
        self.img_labels = []
        for i in range(len(self.label_text)):
            self.img_labels.append(RGBAImage(
                os.path.join(COMMON, 'label_%s.png' % self.label_text[i])))
        self.button_text = [['Draft', 'Random'], ['Store']]
        self.img_button = [[[] for i in range(2)] for j in range(2)]
        self.button_states = ['active', 'inactive']
        for i in range(len(self.button_states)):
            for j in range(len(self.button_text)):
                for k in range(len(self.button_text[j])):
                    self.img_button[i][j].append(RGBAImage(os.path.join(COMMON,
                        'button_%s_%s.png' % (self.button_states[i], self.button_text[j][k]))))
        self.buttons = []

        self.section_frames = []
        self.tmp_counter = 0
        for i in range(len(self.label_text)):
            self.section_frames.append(tk.Frame(self))
            self.section_frames[i].grid(row=i, column=0, sticky="nsew")
            self.labels.append(tk.Label(self.section_frames[i],
                                        image=self.img_labels[i]))
            self.labels[i].grid(row=0, column=0, sticky="nsew")
            for j in range(len(self.button_text[i])):
                self.buttons.append(tk.Button(self.section_frames[i],
                    image=self.img_button[1][i][j], bd=0.1,
                    command=lambda i=i, j=j: self.controller.show_frame(self.button_text[i][j])))
                self.buttons[self.tmp_counter].grid(row=j+1, column=0,
                                                    sticky="nsew")
                self.buttons[self.tmp_counter].bind("<Enter>",
                    lambda event, ctr=self.tmp_counter, i=i, j=j: self.on_enter(ctr, i, j))
                self.buttons[self.tmp_counter].bind("<Leave>",
                    lambda event, ctr=self.tmp_counter, i=i, j=j: self.on_leave(ctr, i, j))
                self.tmp_counter += 1

        self.settingsV1 = tk.Button(self, text="Game Settings",
            command=lambda: self.controller.show_frame('DraftSettings'))
        self.settingsV1.grid(row=6, column=0, sticky="nsew")
        self.settingsV2 = tk.Button(self, text="Pokemon Settings",
            command=lambda: self.controller.show_frame('DraftGenerateSettings'))
        self.settingsV2.grid(row=7, column=0, sticky="nsew")
        self.start_button = tk.Button(self, text="New Game", command=None)
        self.start_button.grid(row=8, column=0, sticky="nsew")
        self.finish_button = tk.Button(self, text="Get Sets",
                                       state='disabled', command=None)
        self.finish_button.grid(row=9, column=0, sticky="nsew")

    def on_enter(self, ctr, i, j):
        self.buttons[ctr].config(image=self.img_button[0][i][j])

    def on_leave(self, ctr, i, j):
        self.buttons[ctr].config(image=self.img_button[1][i][j])


class Draft(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        ##### Private Variables #####
        self.alpha = 0
        self.turn = 0
        self.game_activated = False
        self.pkmn_not_picked = [True for i in range(18)]
        self.battle_mode = tk.StringVar()
        self.battle_mode.set('Singles')
        self.draft_mode = tk.StringVar()
        self.draft_mode.set('Standard')
        self.ban_phase_finished = False
        self.ban_phase_1_finished = False
        self.ban_phase_2_finished = False
        self.ban_number = tk.IntVar()
        self.ban_number.set(0)
        self.img_pkmn = [[] for i in range(len(self.controller.img_type))]
        self.separators = [ttk.Separator(self, orient='horizontal') for i in range(2)]

        for i in range(8):
            self.grid_rowconfigure(i, weight=1)
        for i in range(6):
            self.grid_columnconfigure(i, weight=1)

        self.pkmn_excl_tiers_s = [tk.StringVar() for i in range(len(TIERS_SINGLES))]
        self.pkmn_excl_tiers_d = [tk.StringVar() for i in range(len(TIERS_DOUBLES))]
        self.pkmn_excl_gens = [tk.StringVar() for i in range(len(GENERATIONS))]
        self.pkmn_excl_types = [tk.StringVar() for i in range(len(TYPES))]
        self.pkmn_excl_items = [tk.StringVar() for i in range(len(ITEMS))]
        self.pkmn_excl_gimmicks = [tk.StringVar() for i in range(len(GIMMICKS))]
        self.pkmn_excl_usage = []

        self.checks = [[] for i in range(18)]

        ##### Pool Pokemon #####
        self.pkmn_pool_list = []
        self.pool_buttons = []
        for i in range(3):
            for j in range(6):
                x = (i*6) + j
                self.pool_buttons.append(tk.Button(self,
                                                   image=self.controller.img_blank[0],
                                                   bd=0.1,
                                                   command=None))
                self.pool_buttons[x].grid(row=i, column=j, pady=5)
                self.pool_buttons[x].bind("<Enter>", lambda event, x=x: self.pool_on_enter(x))
                self.pool_buttons[x].bind("<Leave>", lambda event, x=x: self.pool_on_leave(x))

        self.separators[0].grid(row=4, column=0, columnspan=6, sticky="nsew")

        ##### Ban Boxes #####
        self.pkmn_ban_list = [[None, None], [None, None]]
        self.ban_text = tk.Label(self, text="BANS")
        self.ban_text.grid(row=5, column=2, columnspan=2, sticky="nsew")
        self.ban_buttons = [[], []]
        for i in range(2):
            for j in range(2):
                self.ban_buttons[i].append(tk.Button(self,
                                                     image=self.controller.img_blank[0],
                                                     bd=0.1,
                                                     state="disabled",
                                                     command=None))
                if i == 0:
                    self.ban_buttons[i][j].grid(row=5, column=i*4+j,
                                                pady=5)
                else:
                    self.ban_buttons[i][j].grid(row=5, column=i*5-j,
                                                pady=5)

        self.separators[1].grid(row=6, column=0, columnspan=6, sticky="nsew")

        ##### Team Boxes #####
        self.team_text = []
        self.pkmn_team_list = [[None for i in range(6)] for j in range(2)]
        self.team_buttons = [[], []]
        for team in range(2):
            self.team_text.append(tk.Label(self, text="TEAM %s" % str(team+1)))
            self.team_text[team].grid(row=7, column=team*4, columnspan=2,
                                      sticky="nsew")
            for row in range(3):
                for column in range(2):
                    x = (row * 2) + column
                    self.team_buttons[team].append(tk.Button(self,
                                                             image=self.controller.img_blank[0],
                                                             bd=0.1,
                                                             command=None))
                    self.team_buttons[team][x].grid(row=row+8,
                                                    column=(team*4)+column,
                                                    pady=5)
                    self.team_buttons[team][x].bind("<Enter>", lambda event, team=team, x=x: self.team_on_enter(team, x))
                    self.team_buttons[team][x].bind("<Leave>", lambda event, team=team, x=x: self.team_on_leave(team, x))

    def new_game(self):
        # reset private variables
        self.game_activated = True
        self.turn = 0
        self.pkmn_pool_list = []
        self.pkmn_ban_list = [[None, None], [None, None]]
        self.ban_phase_finished = False
        self.ban_phase_1_finished = False
        self.ban_phase_2_finished = False
        self.pkmn_team_list = [[None for i in range(6)] for j in range(2)]
        self.pkmn_not_picked = [True for i in range(18)]
        self.img_pkmn = [[] for i in range(len(self.controller.img_type))]

        temp_excl_tiers = list(
            filter(None, [i.get() for i in self.pkmn_excl_tiers_s]))
        temp_excl_types = list(
            filter(None, [i.get() for i in self.pkmn_excl_types]))
        temp_excl_gimmicks = list(
            filter(None, [i.get() for i in self.pkmn_excl_gimmicks]))
        temp_list = []
        for pkmn in ALL_POKEMON_S:
            if ((pkmn.name in [i.name for i in temp_list]) or
                (pkmn.tier in temp_excl_tiers) or
                (pkmn.type[0] in temp_excl_types) or
                (pkmn.type[1] and pkmn.type[1] in temp_excl_types) or
                (check_valid_generation(self, pkmn)) or
                (check_valid_item(self, pkmn)) or
                (pkmn.tag in temp_excl_gimmicks)):
                continue
            else:
                temp_list.append(pkmn)
        temp_counter = 0
        while temp_counter < 18:
            temp_new_pkmn = random.choice(temp_list)
            if (check_validity(self, temp_new_pkmn)):
                self.pkmn_pool_list.append(temp_new_pkmn)
                temp_counter += 1


        self.get_checks()

        for i in range(18):
            self.get_pkmn_imgs(self.pkmn_pool_list[i].name)
            self.pool_buttons[i].config(image=self.img_pkmn[0][i],
                                        bd=0.1,
                                        command=lambda i=i: self.add_to_team(i))
        for i in range(2):
            for j in range(2):
                self.ban_buttons[i][j].config(image=self.controller.img_blank[0],
                                              command=None)
            for j in range(6):
                self.team_buttons[i][j].config(image=self.controller.img_blank[0],
                                               command=None)
        self.controller.sidebar.finish_button.config(state='disabled',
                                                     command=None)

    def get_pkmn_imgs(self, pkmn_name):
        pkmn_name = pkmn_name.replace('-Small', '').replace('-Large', '').replace('-Super', '').replace(':', '')
        self.img_pkmn_base = [
            RGBAImage2(os.path.join(IMG_PKMN_DIR, pkmn_name + '_inactive.png')),
            RGBAImage2(os.path.join(IMG_PKMN_DIR, pkmn_name + '_active.png')),
            RGBAImage2(os.path.join(IMG_PKMN_DIR, pkmn_name + '_unknown.png')),
            RGBAImage2(os.path.join(IMG_PKMN_DIR, pkmn_name + '_banned.png')),
            RGBAImage2(os.path.join(IMG_PKMN_DIR, pkmn_name + '_picked.png'))]
        for i in range(len(self.controller.img_type)):
            self.img_pkmn_base[i].paste(
                self.controller.img_border[self.draft_mode.get()],
                (0, 0),
                self.controller.img_border[self.draft_mode.get()])
        for i in range(len(self.controller.img_type)):
            self.img_pkmn[i].append(ImageTk.PhotoImage(self.img_pkmn_base[i]))

    def get_checks(self):
        self.checks = [[] for i in range(18)]
        for i in range(18):
            for j in range(18):
                if i != j:
                    attacking_type = self.pkmn_pool_list[j]
                    defending_type = self.pkmn_pool_list[i]
                    if type_logic(attacking_type, defending_type):
                        self.checks[i].append(self.pkmn_pool_list[j].name)
            shuffle(self.checks[i])

    def add_to_team(self, pool_number):
        if self.game_activated:
            if self.pkmn_not_picked[pool_number]:
                if self.turn < 12:
                    self.pkmn_not_picked[pool_number] = False
                    if self.ban_number.get() != 0 and not self.ban_phase_finished:
                        self.pool_buttons[pool_number].config(
                            image=self.img_pkmn[3][pool_number],
                            command=None)
                        self.ban_pkmn(pool_number)
                    else:
                        self.pool_buttons[pool_number].config(
                            image=self.img_pkmn[4][pool_number],
                            command=None)
                        if self.draft_mode.get() == 'Standard':
                            team_number = int(self.turn % 2)
                            slot_number = int(self.turn/2)
                        if self.draft_mode.get() == 'Nemesis':
                            team_number = int((self.turn+1) % 2)
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
                        self.pkmn_team_list[team_number][slot_number] = self.pkmn_pool_list[pool_number]
                        self.team_buttons[team_number][slot_number].config(
                            image=self.img_pkmn[0][pool_number],
                            command=lambda i=pool_number, j=team_number, k=slot_number: self.remove_from_team(i, j, k))
                        self.update_turns()

    def remove_from_team(self, pool_number, team_number, slot_number):
        if self.game_activated:
            self.pkmn_not_picked[pool_number] = True
            self.pkmn_team_list[team_number][slot_number] = None
            self.pool_buttons[pool_number].config(
                image=self.img_pkmn[0][pool_number],
                command=lambda i=pool_number: self.add_to_team(i))
            self.team_buttons[team_number][slot_number].config(
                image=self.controller.img_blank[0],
                command=None)
            self.update_turns()

    def ban_pkmn(self, pool_number):
        # add pkmn to proper banlist
        temp_done = False
        for i in range(self.ban_number.get()):
            for j in range(2):
                if not self.pkmn_ban_list[1-j][i]:
                    self.pkmn_ban_list[1-j][i] = self.pkmn_pool_list[pool_number]
                    self.ban_buttons[1-j][i].config(
                        image=self.img_pkmn[0][pool_number],
                        command=None)
                    temp_done = True
                    break
            if temp_done:
                break
        # end the ban phase
        if ((self.turn == 0 and self.pkmn_ban_list[0][0]) and
            (self.turn == 0 and self.pkmn_ban_list[1][0])):
            self.ban_phase_1_finished = True
        if (((self.turn == 8 and self.pkmn_ban_list[0][1] and self.draft_mode.get() == 'First Pick') and
             (self.turn == 8 and self.pkmn_ban_list[1][1] and self.draft_mode.get() == 'First Pick')) or
            ((self.turn == 6 and self.pkmn_ban_list[0][1] and self.draft_mode.get() != 'First Pick') and
             (self.turn == 6 and self.pkmn_ban_list[1][1] and self.draft_mode.get() != 'First Pick'))):
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
                if not self.pkmn_team_list[fp_team_order[i]][fp_slot_order[i]]:
                    break
                next_turn += 1
        else:
            for i in range(12):
                if self.draft_mode.get() == 'Standard':
                    if not self.pkmn_team_list[int(i % 2)][int(i/2)]:
                        break
                if self.draft_mode.get() == 'Nemesis':
                    if not self.pkmn_team_list[int((i+1) % 2)][int(i/2)]:
                        break
                next_turn += 1
        self.turn = next_turn
        if ((self.turn == 8 and self.ban_number.get() == 2 and self.draft_mode.get() == 'First Pick') or
            (self.turn == 6 and self.ban_number.get() == 2 and self.draft_mode.get() != 'First Pick')):
            self.ban_phase_finished = False
        if self.turn >= 12:
            self.controller.sidebar.finish_button.config(state='normal',
                command=lambda: get_sets(self))

    def pool_on_enter(self, x):
        if self.game_activated:
            if self.pkmn_not_picked[x]:
                self.pool_buttons[x].config(image=self.img_pkmn[1][x])
            else:
                pass
        else:
            if self.pkmn_not_picked[x]:
                self.pool_buttons[x].config(image=self.controller.img_blank[1])
            else:
                pass

    def pool_on_leave(self, x):
        if self.game_activated:
            if self.pkmn_not_picked[x]:
                self.pool_buttons[x].config(image=self.img_pkmn[0][x])
            else:
                pass
        else:
            self.pool_buttons[x].config(image=self.controller.img_blank[0])

    def team_on_enter(self, team, x):
        if self.pkmn_team_list[team][x]:
            pool_num = self.pkmn_pool_list.index(self.pkmn_team_list[team][x])
            self.team_buttons[team][x].config(image=self.img_pkmn[1][pool_num])
        else:
            self.team_buttons[team][x].config(image=self.controller.img_blank[1])

    def team_on_leave(self, team, x):
        if self.pkmn_team_list[team][x]:
            pool_num = self.pkmn_pool_list.index(self.pkmn_team_list[team][x])
            self.team_buttons[team][x].config(image=self.img_pkmn[0][pool_num])
        else:
            self.team_buttons[team][x].config(image=self.controller.img_blank[0])


class DraftSettings(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.battle_mode_text = tk.Label(self, text="Battle Mode")
        self.battle_mode_text.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.battle_mode_buttons = []
        battle_modes = ['Singles', 'Doubles', 'SRL']
        for i in range(len(battle_modes)):
            self.battle_mode_buttons.append(tk.Radiobutton(self,
                text=battle_modes[i],
                variable=self.parent_page().battle_mode,
                indicatoron=0,
                width=10,
                value=battle_modes[i]))
            self.battle_mode_buttons[i].grid(row=1+int(i/5), column=(i % 5)+1,
                                             padx=5, pady=5, sticky="nsew")

        self.draft_mode_text = tk.Label(self, text="Draft Mode")
        self.draft_mode_text.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.draft_mode_buttons = []
        draft_modes = ['Standard', 'Nemesis', 'First Pick']
        for i in range(len(draft_modes)):
            self.draft_mode_buttons.append(tk.Radiobutton(self,
                text=draft_modes[i],
                variable=self.parent_page().draft_mode,
                indicatoron=0,
                width=10,
                value=draft_modes[i]))
            self.draft_mode_buttons[i].grid(row=2+int(i/5), column=(i % 5)+1,
                                            padx=5, pady=5, sticky="nsew")

        self.ban_number_text = tk.Label(self, text="Bans")
        self.ban_number_text.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.ban_number_buttons = []
        ban_number = [0, 1, 2]
        for i in range(len(ban_number)):
            self.ban_number_buttons.append(tk.Radiobutton(self,
                text=ban_number[i],
                variable=self.parent_page().ban_number,
                indicatoron=0,
                width=10,
                value=ban_number[i],
                command=self.activate_bans))
            self.ban_number_buttons[i].grid(row=3+int(i/5),
                                            column=(i % 5)+1, padx=5, pady=5,
                                            sticky="nsew")

        self.back_button = tk.Button(self, text="Back", command=self.exit)
        self.back_button.grid(row=15, column=1, columnspan=2,
                              padx=5, pady=5, sticky="nsew")

        for i in range(8):
            self.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.grid_columnconfigure(i, weight=1)

    def activate_bans(self):
        for i in range(2):
            for j in range(0, self.parent_page().ban_number.get()):
                self.parent_page().ban_buttons[i][j].config(state="normal",
                                                            command=None)
            for j in range(self.parent_page().ban_number.get(), 2):
                self.parent_page().ban_buttons[i][j].config(state="disabled",
                                                            command=None)
        self.parent_page().ban_phase_finished = False

    def parent_page(self):
        return self.controller.pages['Draft']

    def exit(self):
        clean_up(self)
        self.controller.show_frame('Draft')


class DraftGenerateSettings(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        setup_settings(self)

        self.back_button = tk.Button(self, text="Back", command=self.validate)
        self.back_button.grid(row=21, column=1, columnspan=4, padx=5, pady=5,
                              sticky="nsew")

    def validate(self):
        temp_excl_tiers = list(filter(None, [i.get() for i in self.parent_page().pkmn_excl_tiers_s]))
        temp_excl_types = list(filter(None, [i.get()for i in self.parent_page().pkmn_excl_types]))
        temp_excl_gimmicks = list(filter(None, [i.get() for i in self.parent_page().pkmn_excl_gimmicks]))
        temp_counter = 0
        temp_list = []
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
            clean_up(self)
            self.controller.show_frame('Draft')
        else:
            top = tk.Toplevel(self.controller)
            top.grab_set()
            text = "Not enough Pokemon fit the criteria you have selected."
            text2 = "\nPlease remove some restrictions."
            message = tk.Label(top, text=text+text2)
            message.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
            back_button = tk.Button(top, text="Ok", command=top.destroy)
            back_button.grid(row=1, column=0, padx=100, pady=5, sticky="nsew")

    def parent_page(self):
        return self.controller.pages['Draft']


class Random(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        ##### Private Variables #####
        self.alpha = 0
        self.game_activated = False
        self.temp_list = []
        self.battle_mode = tk.StringVar()
        self.battle_mode.set('Singles')
        self.theme = tk.StringVar()
        self.theme.set('Random')
        for i in range(6):
            self.grid_columnconfigure(i, weight=1)
        for i in range(7):
            self.grid_rowconfigure(i, weight=1)
        self.img_pkmn = [[] for i in range(2)]

        self.pkmn_excl_tiers_s = [tk.StringVar() for i in range(len(TIERS_SINGLES))]
        self.pkmn_excl_tiers_d = [tk.StringVar() for i in range(len(TIERS_DOUBLES))]
        self.pkmn_excl_gens = [tk.StringVar() for i in range(len(GENERATIONS))]
        self.pkmn_excl_types = [tk.StringVar() for i in range(len(TYPES))]
        self.pkmn_excl_items = [tk.StringVar() for i in range(len(ITEMS))]
        self.pkmn_excl_gimmicks = [tk.StringVar() for i in range(len(GIMMICKS))]
        self.pkmn_excl_usage = []

        ##### Team Boxes #####
        self.team_text = []
        self.pkmn_team_list = [[None for i in range(6)] for j in range(2)]
        self.team_buttons = [[], []]
        for team in range(2):
            self.team_text.append(tk.Label(self, text="TEAM %s" % str(team+1)))
            self.team_text[team].grid(row=1, column=team*4, columnspan=2,
                                      sticky="nsew")
            for row in range(3):
                for column in range(2):
                    x = (row * 2) + column
                    self.team_buttons[team].append(tk.Button(self,
                                                             image=self.controller.img_blank[0],
                                                             bd=0.1,
                                                             command=None))
                    self.team_buttons[team][x].grid(row=row+2,
                                                    column=(team*4)+column,
                                                    pady=5)
                    self.team_buttons[team][x].bind("<Enter>", lambda event, team=team, x=x: self.team_on_enter(team, x))
                    self.team_buttons[team][x].bind("<Leave>", lambda event, team=team, x=x: self.team_on_leave(team, x))

    def new_game(self):
        # reset private variables
        self.game_activated = True
        self.pkmn_team_list = [[None for i in range(6)] for j in range(2)]

        temp_excl_tiers = list(filter(None, [i.get() for i in self.pkmn_excl_tiers_s]))
        temp_excl_types = list(filter(None, [i.get() for i in self.pkmn_excl_types]))
        temp_excl_gimmicks = list(filter(None, [i.get() for i in self.pkmn_excl_gimmicks]))
        self.temp_list = []
        for pkmn in ALL_POKEMON_S:
            if ((pkmn.name in [i.name for i in self.temp_list]) or
                (pkmn.tier in temp_excl_tiers) or
                (pkmn.type[0] in temp_excl_types) or
                (pkmn.type[1] and pkmn.type[1] in temp_excl_types) or
                (check_valid_generation(self, pkmn)) or
                (check_valid_item(self, pkmn)) or
                (pkmn.tag in temp_excl_gimmicks)):
                continue
            else:
                self.temp_list.append(pkmn)
        counter = 0
        for i in range(2):
            while counter < 6:
                if i == 1 and self.theme.get() == 'Balanced':
                    temp_new_pkmn = random.choice(self.temp_list)
                    if ((check_validity(self, temp_new_pkmn, i)) and
                        (temp_new_pkmn.tier == self.pkmn_team_list[0][counter].tier)):
                        self.pkmn_team_list[i][counter] = temp_new_pkmn
                        counter += 1
                else:
                    temp_new_pkmn = random.choice(self.temp_list)
                    if (check_validity(self, temp_new_pkmn, i)):
                        self.pkmn_team_list[i][counter] = temp_new_pkmn
                        counter += 1
            counter = 0

        for i in range(2):
            for j in range(6):
                self.get_pkmn_imgs(self.pkmn_team_list[i][j].name)
                x = (i * 6) + j
                self.team_buttons[i][j].config(image=self.img_pkmn[0][x],
                                               command=lambda i=i, j=j: self.reroll(i, j))
        self.controller.sidebar.finish_button.config(state='normal',
                                                     command=lambda: get_sets(self))

    def get_pkmn_imgs(self, pkmn_name):
        pkmn_name = pkmn_name.replace('-Small', '').replace('-Large', '').replace('-Super', '').replace(':', '')
        self.img_pkmn_base = [RGBAImage2(os.path.join(IMG_PKMN_DIR, pkmn_name + '_inactive.png')),
                              RGBAImage2(os.path.join(IMG_PKMN_DIR, pkmn_name + '_active.png'))]
        for i in range(2):
            self.img_pkmn_base[i].paste(self.controller.img_border['Random'],
                                        (0, 0),
                                        self.controller.img_border['Random'])
        for i in range(2):
            self.img_pkmn[i].append(ImageTk.PhotoImage(self.img_pkmn_base[i]))

    def reroll(self, team, slot):
        x = (team * 6) + slot
        while True:
            temp_new_pkmn = random.choice(self.temp_list)
            if (check_validity(self, temp_new_pkmn, team)):
                self.pkmn_team_list[team][slot] = temp_new_pkmn
                name = self.pkmn_team_list[team][slot].name.replace('-Small', '').replace('-Large', '').replace('-Super', '').replace(':', '')
                self.img_pkmn_base = [RGBAImage2(os.path.join(IMG_PKMN_DIR, name + '_inactive.png')),
                                      RGBAImage2(os.path.join(IMG_PKMN_DIR, name + '_active.png'))]
                for i in range(2):
                    self.img_pkmn_base[i].paste(self.controller.img_border['Random'],
                                                (0, 0),
                                                self.controller.img_border['Random'])
                for i in range(2):
                    self.img_pkmn[i][x] = ImageTk.PhotoImage(self.img_pkmn_base[i])
                self.team_buttons[team][slot].config(image=self.img_pkmn[0][x])
                break

    def team_on_enter(self, team, x):
        if self.pkmn_team_list[team][x]:
            pool_num = (team * 6) + x
            self.team_buttons[team][x].config(image=self.img_pkmn[1][pool_num])
        else:
            self.team_buttons[team][x].config(image=self.controller.img_blank[1])

    def team_on_leave(self, team, x):
        if self.pkmn_team_list[team][x]:
            pool_num = (team * 6) + x
            self.team_buttons[team][x].config(image=self.img_pkmn[0][pool_num])
        else:
            self.team_buttons[team][x].config(image=self.controller.img_blank[0])


class RandomSettings(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.battle_mode_text = tk.Label(self, text="Battle Mode")
        self.battle_mode_text.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.battle_mode_buttons = []
        battle_modes = ['Singles', 'Doubles', 'SRL']
        for i in range(len(battle_modes)):
            self.battle_mode_buttons.append(tk.Radiobutton(self,
                text=battle_modes[i],
                variable=self.parent_page().battle_mode,
                indicatoron=0,
                width=10,
                value=battle_modes[i]))
            self.battle_mode_buttons[i].grid(row=1+int(i/5), column=(i % 5)+1,
                                             padx=5, pady=5, sticky="nsew")

        self.back_button = tk.Button(self, text="Back", command=self.exit)
        self.back_button.grid(row=15, column=1, columnspan=2, padx=5, pady=5,
                              sticky="nsew")

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
            self.theme_buttons[i].grid(row=2+int(i/5), column=(i % 5)+1, padx=5,
                                       pady=5, sticky="nsew")

        for i in range(6):
            self.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.grid_columnconfigure(i, weight=1)

    def parent_page(self):
        return self.controller.pages['Random']

    def exit(self):
        clean_up(self)
        self.controller.show_frame('Random')


class RandomGenerateSettings(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        setup_settings(self)

        self.back_button = tk.Button(self, text="Back", command=self.validate)
        self.back_button.grid(row=24, column=1, columnspan=4, padx=5, pady=5,
                              sticky="nsew")

    def validate(self):
        temp_excl_tiers = list(filter(None, [i.get() for i in self.parent_page().pkmn_excl_tiers_s]))
        temp_excl_types = list(filter(None, [i.get() for i in self.parent_page().pkmn_excl_types]))
        temp_excl_gimmicks = list(filter(None, [i.get() for i in self.parent_page().pkmn_excl_gimmicks]))
        temp_counter = 0
        temp_list = []
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
            clean_up(self)
            self.controller.show_frame('Random')
        else:
            top = tk.Toplevel(self.controller)
            top.grab_set()
            text = "Not enough Pokemon fit the criteria you have selected."
            text2 = "\nPlease remove some restrictions."
            message = tk.Label(top, text=text+text2)
            message.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
            back_button = tk.Button(top, text="Ok", command=top.destroy)
            back_button.grid(row=1, column=0, padx=100, pady=5, sticky="nsew")

    def parent_page(self):
        return self.controller.pages['Random']


class Store(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.banner_num = 0
        self.current_page = 0
        self.current_player = tk.StringVar()
        self.current_player.set(PLAYERS[0].name)

        self.img_banners = []
        self.img_banner_buttons = []
        for i in range(self.banner_num, self.banner_num+2):
            self.img_banners.append(
                RGBAImage(os.path.join(COMMON, 'banner%s_fit.png' % i)))
            self.img_banner_buttons.append(
                RGBAImage(os.path.join(COMMON, 'banner%s_button.png' % i)))
        self.banner_image = tk.Label(self, image=self.img_banners[self.banner_num])
        self.banner_image.grid(row=0, column=0, columnspan=3, sticky="nsew")
        self.page_buttons = []
        for i in range(2):
            self.page_buttons.append(tk.Button(self,
                image=self.img_banner_buttons[i],
                bd=0.1,
                command=lambda i=i: self.change_page(i)))
            self.page_buttons[i].grid(row=2, column=i, padx=(30, 0), sticky="nsew")

        #self.scrollframe = tk.LabelFrame(self, text="Pokemon List", border=2)
        self.scrollframe = tk.Frame(self)
        self.scrollframe.grid(row=3, column=0, rowspan=5, columnspan=3, padx=5,
                              pady=5, sticky="nsew")
        self.container = tk.Canvas(self.scrollframe,
                                   scrollregion=(0, 0, 400, 640))
        self.scrollbar = ttk.Scrollbar(self.scrollframe, orient='vertical',
                                       command=self.container.yview)
        self.container.config(yscrollcommand=self.scrollbar.set)
        self.container.bind("<Enter>", self._on_mousewheel)
        self.container.bind("<Leave>", self._off_mousewheel)
        self.scrollbar.pack(side='right', fill='y')
        self.container.pack(side='left', expand=True, fill='both')

        self.img_pkmn = [[[] for i in range(3)] for j in range(2)]
        self.get_pkmn_imgs()

        self.pkmn_buttons = [[None for i in range(5)] for j in range(8)]
        self.pkmn_buttons.append([None for i in range(4)])
        for i in range(9):
            for j in range(len(self.pkmn_buttons[i])):
                x = (i * 5) + j
                self.pkmn_buttons[i][j] = tk.Button(self.container,
                    image=self.img_pkmn[self.current_page][0][x],
                    bd=0.1,
                    command=None)
                self.container.create_window((j*100)+50, (i*70)+30,
                                             window=self.pkmn_buttons[i][j])

        self.bottom_frame = tk.Frame(self)
        self.bottom_frame.grid(row=8, column=0, columnspan=2, sticky="nsew")
        self.pull_result = tk.Label(self.bottom_frame, text="? ? ?", command=None)
        self.pull_result.pack(side='left', fill='both', expand=True,
                              padx=5, pady=5)
        self.player_name = tk.OptionMenu(self.bottom_frame, self.current_player,
                                         *playerNames, command=self.switch_player)
        self.player_name.pack(side='left', fill='both', expand=True,
                              padx=5, pady=5)
        self.pull_button = tk.Button(self.bottom_frame, text="Pull New Pokemon",
                                     command=self.pull)
        self.pull_button.pack(side='left', fill='both', expand=True,
                              padx=5, pady=5)

        self.pkmn_lists = [[], []]
        for pkmn in ALL_POKEMON_S:
            if pkmn.srl_group == self.banner_num:
                self.pkmn_lists[0].append(pkmn)
            if pkmn.srl_group == self.banner_num+1:
                self.pkmn_lists[1].append(pkmn)

        self.switch_player(self.current_player.get())

        for i in range(9):
            self.grid_rowconfigure(i, weight=1)
        for i in range(3):
            self.grid_columnconfigure(i, weight=1)

    def get_pkmn_imgs(self):
        for i in range(self.banner_num, self.banner_num+2):
            for j in range(44):
                pkmn_name = ALL_BANNERS[i][j].replace('-Small', '').replace('-Large', '').replace('-Super', '').replace(':', '')
                self.img_pkmn_base = [
                    RGBAImage2(os.path.join(IMG_PKMN_DIR,
                                            pkmn_name + '_inactive.png')),
                    RGBAImage2(os.path.join(IMG_PKMN_DIR,
                                            pkmn_name + '_active.png')),
                    RGBAImage2(os.path.join(IMG_PKMN_DIR,
                                            pkmn_name + '_picked.png'))]
                for k in range(3):
                    self.img_pkmn_base[k].paste(
                        self.controller.img_border['Random'],
                        (0, 0),
                        self.controller.img_border['Random'])
                for k in range(3):
                    self.img_pkmn[i][k].append(
                        ImageTk.PhotoImage(self.img_pkmn_base[k]))

    def _on_mousewheel(self, event):
        self.container.bind_all('<MouseWheel>', self._scroll)

    def _off_mousewheel(self, event):
        self.container.unbind_all('<MouseWheel>')

    def _scroll(self, event):
        self.container.yview_scroll(int(-1*(event.delta/120)), "units")

    def switch_player(self, player):
        current_banner = self.banner_num + self.current_page
        slot = playerNames.index(player)
        player_pkmn_list = PLAYERS[slot].pkmn_list
        player_pkmn_name_list = [i.name for i in player_pkmn_list]
        for i in range(9):
            for j in range(len(self.pkmn_buttons[i])):
                x = (i * 5) + j
                name = ALL_BANNERS[current_banner][x]
                if get_true_name(name) in player_pkmn_name_list:
                    self.pkmn_buttons[i][j].config(
                        image=self.img_pkmn[current_banner][2][x],
                        command=lambda x=x: self.remove_from_team(x))
                else:
                    self.pkmn_buttons[i][j].config(
                        image=self.img_pkmn[current_banner][0][x],
                        command=lambda x=x: self.add_to_team(x))

    def pull(self):
        current_banner = self.banner_num + self.current_page
        slot = playerNames.index(self.current_player.get())
        player_pkmn_list = PLAYERS[slot].pkmn_list
        player_pkmn_name_list = [i.name for i in player_pkmn_list]
        while True:
            temp_new_pkmn = random.choice(self.pkmn_lists[current_banner])
            if temp_new_pkmn.name not in player_pkmn_name_list:
                PLAYERS[slot].pkmn_list.append(temp_new_pkmn)
                self.pull_result.config(text=temp_new_pkmn.name)
                pkmn_index = ALL_BANNERS[current_banner].index(
                    get_true_name(temp_new_pkmn.name))
                for i in range(9):
                    for j in range(len(self.pkmn_buttons[i])):
                        x = (i * 5) + j
                        if x == pkmn_index:
                            self.pkmn_buttons[i][j].config(
                                image=self.img_pkmn[current_banner][2][x],
                                command=lambda x=x: self.remove_from_team(x))
                self.update_player_csv(slot)
                break

    def add_to_team(self, x):
        current_banner = self.banner_num + self.current_page
        slot = playerNames.index(self.current_player.get())
        player_pkmn_list = PLAYERS[slot].pkmn_list
        player_pkmn_name_list = [i.name for i in player_pkmn_list]

        temp_pkmn_list = []
        for pkmn in self.pkmn_lists[current_banner]:
            if pkmn.name == get_true_name(ALL_BANNERS[current_banner][x]):
                temp_pkmn_list.append(pkmn)
        temp_new_pkmn = random.choice(temp_pkmn_list)
        PLAYERS[slot].pkmn_list.append(temp_new_pkmn)
        self.pull_result.config(text=ALL_BANNERS[current_banner][x])

        for i in range(9):
            for j in range(len(self.pkmn_buttons[i])):
                y = (i * 5) + j
                if y == x:
                    self.pkmn_buttons[i][j].config(
                        image=self.img_pkmn[current_banner][2][y],
                        command=lambda y=y: self.remove_from_team(y))
        self.update_player_csv(slot)

    def remove_from_team(self, x):
        current_banner = self.banner_num + self.current_page
        slot = playerNames.index(self.current_player.get())
        player_pkmn_list = PLAYERS[slot].pkmn_list
        player_pkmn_name_list = [i.name for i in player_pkmn_list]
        target_name = get_true_name(ALL_BANNERS[current_banner][x])
        for pkmn in PLAYERS[slot].pkmn_list:
            if pkmn.name == target_name:
                target_index = PLAYERS[slot].pkmn_list.index(pkmn)
                break
        del PLAYERS[slot].pkmn_list[target_index]
        self.pull_result.config(text="Removed " + ALL_BANNERS[current_banner][x])

        for i in range(9):
            for j in range(len(self.pkmn_buttons[i])):
                y = (i * 5) + j
                if y == x:
                    self.pkmn_buttons[i][j].config(
                        image=self.img_pkmn[current_banner][0][y],
                        command=lambda y=y: self.add_to_team(y))
        self.update_player_csv(slot)

    def change_page(self, page_num):
        if self.current_page != page_num:
            self.current_page = page_num
            self.banner_image.config(image=self.img_banners[self.current_page])
            self.switch_player(self.current_player.get())

    def update_player_csv(self, slot):
        file = os.path.join(PLAYER_DIR, self.current_player.get() + '.csv')
        with open(file, 'w', newline='') as fileName:
            writer = csv.writer(fileName, delimiter=',')
            for pkmn in PLAYERS[slot].pkmn_list:
                writer.writerow(
                    [pkmn.name, pkmn.dex, pkmn.type[0], pkmn.type[1],
                     pkmn.tier, pkmn.rarity, str(pkmn.srl_group),
                     pkmn.tag, pkmn.item, pkmn.ability,
                     pkmn.evSpread, pkmn.nature, pkmn.ivSpread,
                     pkmn.moves[0], pkmn.moves[1], pkmn.moves[2],
                     pkmn.moves[3],
                     str(pkmn.generated_draft),
                     str(pkmn.generated_nemesis),
                     str(pkmn.generated_random),
                     str(pkmn.picked_draft),
                     str(pkmn.picked_nemesis),
                     str(pkmn.banned)])


class PlayerManagement(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller


def get_true_name(name):
    return name.replace('-Mega-X', '').replace('-Mega-Y', '').replace('-Ash', '').replace('-Mega', '')


def check_validity(self, pkmn, i=0):
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
        names = [slot.name for slot in self.pkmn_team_list[i] if slot != None]
        if ((pkmn in self.pkmn_team_list[i]) or
            (pkmn.name in names) or
            (pkmn.tier in tier_list) or
            (pkmn.type[0] in type_list) or
            (pkmn.type[1] and pkmn.type[1] in type_list) or
            (check_valid_generation(self, pkmn)) or
            (check_valid_item(self, pkmn)) or
            (pkmn.tag in gimmick_list)):
            return False
    return True


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


def update_statistics(self):
    if hasattr(self, 'pkmn_ban_list'):
        for team in self.pkmn_ban_list:
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
    file = 'main_database_copy.csv'
    with open(file, 'w', newline='') as fileName:
        writer = csv.writer(fileName, delimiter=',')
        writer.writerow(['POKEMON', 'DEX', 'TYPE 1', 'TYPE 2', 'TIER',
                         'RARITY', 'SRL', 'TAG', 'ITEM', 'ABILITY', 'EV SPREAD',
                         'NATURE', 'IV SPREAD', 'MOVE 1', 'MOVE 2', 'MOVE 3',
                         'MOVE 4', 'GENERATED (D)', 'GENERATED (N)',
                         'GENERATED (R)', 'PICKED (D)', 'PICKED (N)', 'BANNED'])
        for pkmn in ALL_POKEMON_S:
            writer.writerow(
                [pkmn.name, pkmn.dex, pkmn.type[0], pkmn.type[1],
                 pkmn.tier, pkmn.rarity, str(pkmn.srl_group),
                 pkmn.tag, pkmn.item, pkmn.ability,
                 pkmn.evSpread, pkmn.nature, pkmn.ivSpread,
                 pkmn.moves[0], pkmn.moves[1], pkmn.moves[2],
                 pkmn.moves[3],
                 str(pkmn.generated_draft),
                 str(pkmn.generated_nemesis),
                 str(pkmn.generated_random),
                 str(pkmn.picked_draft),
                 str(pkmn.picked_nemesis),
                 str(pkmn.banned)])


def clean_up(self):
    if hasattr(self.parent_page(), 'game_activated'):
        self.parent_page().game_activated = False
    if hasattr(self.parent_page(), 'turn'):
        self.parent_page().turn = 0
    if hasattr(self.parent_page(), 'pkmn_pool_list'):
        self.parent_page().pkmn_pool_list = []
        for i in range(18):
            self.parent_page().pool_buttons[i].config(command=None)
    if hasattr(self.parent_page(), 'pkmn_ban_list'):
        self.parent_page().pkmn_ban_list = [[None, None], [None, None]]
    if hasattr(self.parent_page(), 'ban_phase_finished'):
        self.parent_page().ban_phase_finished = False
        self.parent_page().ban_phase_1_finished = False
        self.parent_page().ban_phase_2_finished = False
    self.parent_page().pkmn_team_list = [[None for i in range(6)] for j in range(2)]
    if hasattr(self.parent_page(), 'pkmn_not_picked'):
        self.parent_page().pkmn_not_picked = [True for i in range(18)]
    for i in range(2):
        if hasattr(self.parent_page(), 'ban_buttons'):
            for j in range(2):
                self.parent_page().ban_buttons[i][j].config(command=None)
        for j in range(6):
            self.parent_page().team_buttons[i][j].config(command=None)
    if hasattr(self.parent_page(), 'mode_text'):
        if hasattr(self, 'draft_mode_buttons'):
            self.parent_page().mode_text.config(
                text="%s Draft" % self.parent_page().draft_mode.get())
        if hasattr(self, 'theme_buttons'):
            self.parent_page().mode_text.config(
                text="%s Battle" % self.parent_page().theme.get())


def setup_settings(self):
    self.tier_text = tk.Label(self, text="Tiers (Singles)")
    self.tier_text.grid(row=1, column=0, rowspan=2, sticky="w")
    self.tier_buttons = []
    for i in range(len(TIERS_SINGLES)):
        self.tier_buttons.append(tk.Checkbutton(self, text=TIERS_SINGLES[i],
            variable=self.parent_page().pkmn_excl_tiers_s[i],
            onvalue=TIERS_SINGLES[i],
            offvalue=''))
        self.tier_buttons[i].grid(row=1+int(i/5), column=(i % 5)+1, sticky="w")

    self.separators = [ttk.Separator(self, orient='horizontal') for i in range(7)]
    self.separators[0].grid(row=3, column=0, columnspan=6, sticky="nsew")


    self.tier2_text = tk.Label(self, text="Tiers (Doubles)")
    self.tier2_text.grid(row=4, column=0, sticky="w")
    self.tier2_buttons = []
    for i in range(len(TIERS_DOUBLES)):
        self.tier2_buttons.append(tk.Checkbutton(self, text=TIERS_DOUBLES[i],
            variable=self.parent_page().pkmn_excl_tiers_d[i],
            onvalue=TIERS_DOUBLES[i],
            offvalue=''))
        self.tier2_buttons[i].grid(row=4+int(i/5), column=(i % 5)+1, sticky="w")

    self.separators[1].grid(row=5, column=0, columnspan=6, sticky="nsew")

    self.gen_text = tk.Label(self, text="Generations")
    self.gen_text.grid(row=6, column=0, rowspan=2, sticky="w")
    self.gen_buttons = []
    for i in range(len(GENERATIONS)):
        self.gen_buttons.append(tk.Checkbutton(self, text=GENERATIONS[i],
            variable=self.parent_page().pkmn_excl_gens[i],
            onvalue=GENERATIONS[i],
            offvalue=''))
        self.gen_buttons[i].grid(row=6+int(i/5), column=(i % 5)+1, sticky="w")

    self.separators[2].grid(row=8, column=0, columnspan=6, sticky="nsew")

    self.type_text = tk.Label(self, text="Types")
    self.type_text.grid(row=9, column=0, rowspan=4, sticky="w")
    self.type_buttons = []
    for i in range(len(TYPES)):
        self.type_buttons.append(tk.Checkbutton(self, text=TYPES[i],
            variable=self.parent_page().pkmn_excl_types[i],
            onvalue=TYPES[i],
            offvalue=''))
        self.type_buttons[i].grid(row=9+int(i/5), column=(i % 5)+1, sticky="w")

    self.separators[3].grid(row=13, column=0, columnspan=6, sticky="nsew")

    self.item_text = tk.Label(self, text="Items")
    self.item_text.grid(row=14, column=0, rowspan=2, sticky="w")
    self.item_buttons = []
    for i in range(len(ITEMS)):
        self.item_buttons.append(tk.Checkbutton(self, text=ITEMS[i],
            variable=self.parent_page().pkmn_excl_items[i],
            onvalue=ITEMS[i],
            offvalue=''))
        self.item_buttons[i].grid(row=14+int(i/5), column=(i % 5)+1, sticky="w")

    self.separators[4].grid(row=16, column=0, columnspan=6, sticky="nsew")

    self.gimmick_text = tk.Label(self, text="Gimmicks")
    self.gimmick_text.grid(row=17, column=0, rowspan=2, sticky="w")
    self.gimmick_buttons = []
    for i in range(len(GIMMICKS)):
        self.gimmick_buttons.append(tk.Checkbutton(self, text=GIMMICKS[i],
            variable=self.parent_page().pkmn_excl_gimmicks[i],
            onvalue=GIMMICKS[i],
            offvalue=''))
        self.gimmick_buttons[i].grid(row=17+int(i/5),
                                     column=(i % 5)+1, sticky="w")

    self.separators[5].grid(row=19, column=0, columnspan=6, sticky="nsew")

    self.usage_text = tk.Label(self, text="Usage")
    self.usage_text.grid(row=20, column=0, sticky="w")

    self.separators[6].grid(row=21, column=0, columnspan=6, sticky="nsew")


def init_player_information():
    directory = os.path.dirname(os.path.realpath(__file__))
    PLAYER_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                    'players')
    with open(os.path.join(directory, 'Banners.csv'), 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            ALL_BANNERS.append(row)
    if not os.path.isdir(PLAYER_DIR):
        os.mkdir(PLAYER_DIR)
        print("Made Player directory")
    for filename in os.listdir(PLAYER_DIR):
        if filename.endswith(".csv"):
            with open(os.path.join(PLAYER_DIR, filename)) as file:
                player_name = os.path.splitext(os.path.basename(file.name))[0]
                reader = csv.reader(file)
                temp_pkmn_list = []
                for row in reader:
                    if not row:
                        print("File for " + player_name + " is empty")
                    else:
                        temp_pkmn_list.append(Pokemon(row))
                PLAYERS.append(Player(player_name, temp_pkmn_list))
                playerNames.append(player_name)


def RGBAImage(path):
    return ImageTk.PhotoImage(Image.open(path).convert("RGBA"))


def RGBAImage2(path):
    return Image.open(path).convert("RGBA")


class Player:
    def __init__(self, name, pkmn_list=[]):
        self.name = name
        self.pkmn_list = pkmn_list


if __name__ == "__main__":
    init_player_information()
    app = MainApp()
    app.mainloop()
