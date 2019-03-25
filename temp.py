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
        self.side_frame.grid(row=0, column=0, sticky='nsew')
        self.side_frame.grid_rowconfigure(0, weight=1)
        self.side_frame.grid_columnconfigure(0, weight=1)

        self.main_frame = tk.Frame(self)
        self.main_frame.grid(row=0, column=1, sticky='nsew')

        self.sidebar = Sidebar(parent=self.side_frame, controller=self)
        self.sidebar.grid(row=0, column=0, sticky='nsew')

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
                      RandomSettings, RandomGenerateSettings, Store, Players,
                      HelpPage, NewPull):
            page_name = Class.__name__
            frame = Class(parent=self.main_frame, controller=self)
            self.pages[page_name] = frame
            frame.grid(row=0, column=0, sticky='nsew')

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
                # fix here!
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
        self.button_text = [['Draft', 'Random'], ['Players', 'Store'],
                            ['settingsv1', 'settingsv2', 'Game', 'Sets']]
        self.img_button = [[[] for i in range(3)] for j in range(2)]
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
            self.section_frames[i].grid(row=i, column=0, sticky='nsew')
            self.labels.append(tk.Label(self.section_frames[i],
                                        image=self.img_labels[i]))
            self.labels[i].grid(row=0, column=0, sticky='nsew')
            for j in range(len(self.button_text[i])):
                self.buttons.append(tk.Button(self.section_frames[i],
                    image=self.img_button[1][i][j], bd=0.1,
                    command=lambda i=i, j=j: self.controller.show_frame(self.button_text[i][j])))
                self.buttons[self.tmp_counter].grid(row=j+1, column=0,
                                                    sticky='nsew')
                self.buttons[self.tmp_counter].bind('<Enter>',
                    lambda event, ctr=self.tmp_counter, i=i, j=j: self.on_enter(ctr, i, j))
                self.buttons[self.tmp_counter].bind('<Leave>',
                    lambda event, ctr=self.tmp_counter, i=i, j=j: self.on_leave(ctr, i, j))
                self.tmp_counter += 1

        self.empty_space = RGBAImage(os.path.join(COMMON, '3_empty_buttons.png'))
        self.empty_space_label = tk.Label(self, image=self.empty_space)
        self.empty_space_label.grid(row=3, column=0, rowspan=3, sticky='nsew')

        self.settingsV1 = tk.Button(self, image=self.img_button[1][2][0], bd=0.1,
            command=lambda: self.controller.show_frame('DraftSettings'))
        self.settingsV1.grid(row=6, column=0, sticky='nsew')
        self.settingsV1.bind('<Enter>', lambda event: self.on_enter_settings(0))
        self.settingsV1.bind('<Leave>', lambda event: self.on_leave_settings(0))
        self.settingsV2 = tk.Button(self, image=self.img_button[1][2][1], bd=0.1,
            command=lambda: self.controller.show_frame('DraftGenerateSettings'))
        self.settingsV2.grid(row=7, column=0, sticky='nsew')
        self.settingsV2.bind('<Enter>', lambda event: self.on_enter_settings(1))
        self.settingsV2.bind('<Leave>', lambda event: self.on_leave_settings(1))
        self.start_button = tk.Button(self, image=self.img_button[1][2][2], bd=0.1,
                                      command=None)
        self.start_button.grid(row=8, column=0, sticky='nsew')
        self.start_button.bind('<Enter>', lambda event: self.on_enter_settings(2))
        self.start_button.bind('<Leave>', lambda event: self.on_leave_settings(2))
        self.finish_button = tk.Button(self, image=self.img_button[1][2][3], bd=0.1,
                                       state='disabled', command=None)
        self.finish_button.grid(row=9, column=0, sticky='nsew')
        self.finish_button.bind('<Enter>', lambda event: self.on_enter_settings(3))
        self.finish_button.bind('<Leave>', lambda event: self.on_leave_settings(3))

    def on_enter(self, ctr, i, j):
        self.buttons[ctr].config(image=self.img_button[0][i][j])

    def on_leave(self, ctr, i, j):
        self.buttons[ctr].config(image=self.img_button[1][i][j])

    def on_enter_settings(self, button_num):
        if button_num == 0:
            if self.settingsV1.cget('state') != 'disabled':
                self.settingsV1.config(image=self.img_button[0][2][0])
        elif button_num == 1:
            if self.settingsV2.cget('state') != 'disabled':
                self.settingsV2.config(image=self.img_button[0][2][1])
        elif button_num == 2:
            if self.start_button.cget('state') != 'disabled':
                self.start_button.config(image=self.img_button[0][2][2])
        elif button_num == 3:
            if self.finish_button.cget('state') != 'disabled':
                self.finish_button.config(image=self.img_button[0][2][3])

    def on_leave_settings(self, button_num):
        if button_num == 0:
            self.settingsV1.config(image=self.img_button[1][2][0])
        elif button_num == 1:
            self.settingsV2.config(image=self.img_button[1][2][1])
        elif button_num == 2:
            self.start_button.config(image=self.img_button[1][2][2])
        elif button_num == 3:
            self.finish_button.config(image=self.img_button[1][2][3])


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
        self.show_megas = tk.StringVar()
        self.show_megas.set('No')
        self.img_pkmn = [[] for i in range(len(self.controller.img_type))]
        self.separators = [ttk.Separator(self, orient='horizontal') for i in range(2)]

        for i in range(11):
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
        self.pool_img = RGBAImage(os.path.join(COMMON, 'label_pool.png'))
        self.pool_text = tk.Label(self, image=self.pool_img)
        self.pool_text.grid(row=0, column=0, columnspan=6, sticky='nsw')
        self.pkmn_pool_list = []
        self.pool_buttons = []
        for i in range(3):
            for j in range(6):
                x = (i*6) + j
                self.pool_buttons.append(tk.Button(self,
                                                   image=self.controller.img_blank[0],
                                                   bd=0.1,
                                                   command=None))
                self.pool_buttons[x].grid(row=i+1, column=j, pady=5)
                self.pool_buttons[x].bind('<Enter>', lambda event, x=x: self.pool_on_enter(x))
                self.pool_buttons[x].bind('<Leave>', lambda event, x=x: self.pool_on_leave(x))

        self.separators[0].grid(row=4, column=0, columnspan=6, sticky='nsew')

        ##### Ban Boxes #####
        self.pkmn_ban_list = [[None, None], [None, None]]
        self.ban_img = RGBAImage(os.path.join(COMMON, 'label_bans.png'))
        self.ban_text = tk.Button(self, image=self.ban_img, bd=0.1, state='disabled')
        self.ban_text.grid(row=5, column=2, columnspan=2, sticky='nsew')
        self.ban_buttons = [[], []]
        for i in range(2):
            for j in range(2):
                self.ban_buttons[i].append(tk.Button(self,
                                                     image=self.controller.img_blank[0],
                                                     bd=0.1,
                                                     state='disabled',
                                                     command=None))
                if i == 0:
                    self.ban_buttons[i][j].grid(row=5, column=i*4+j,
                                                pady=5)
                else:
                    self.ban_buttons[i][j].grid(row=5, column=i*5-j,
                                                pady=5)

        self.separators[1].grid(row=6, column=0, columnspan=6, sticky='nsew')

        ##### Team Boxes #####
        self.team_text = []
        self.pkmn_team_list = [[None for i in range(6)] for j in range(2)]
        self.team_buttons = [[], []]
        for team in range(2):
            self.team_text.append(tk.Label(self, text='TEAM %s' % str(team+1)))
            self.team_text[team].grid(row=7, column=team*4, columnspan=2,
                                      sticky='nsew')
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
                    self.team_buttons[team][x].bind('<Enter>', lambda event, team=team, x=x: self.team_on_enter(team, x))
                    self.team_buttons[team][x].bind('<Leave>', lambda event, team=team, x=x: self.team_on_leave(team, x))

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
            if self.show_megas.get() == 'Yes':
                if is_mega(self.pkmn_pool_list[i]):
                    if self.pkmn_pool_list[i].item.endswith('ite X'):
                        pkmn_name = self.pkmn_pool_list[i].name + '-Mega-X'
                    elif self.pkmn_pool_list[i].item.endswith('ite Y'):
                        pkmn_name = self.pkmn_pool_list[i].name + '-Mega-X'
                    elif self.pkmn_pool_list[i].ability == 'Battle Bond':
                        pkmn_name = self.pkmn_pool_list[i].name + '-Ash'
                    else:
                        pkmn_name = self.pkmn_pool_list[i].name + '-Mega'
                else:
                    pkmn_name = self.pkmn_pool_list[i].name
            else:
                pkmn_name = self.pkmn_pool_list[i].name
            self.get_pkmn_imgs(pkmn_name)
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
        ext = ['_inactive.png', '_active.png', '_unknown.png', '_banned.png', '_picked.png']
        for i in range(len(ext)):
            self.img_pkmn_base = RGBAImage2(os.path.join(IMG_PKMN_DIR, pkmn_name + ext[i]))
            self.img_pkmn_base.paste(
                self.controller.img_border[self.draft_mode.get()],
                (0, 0),
                self.controller.img_border[self.draft_mode.get()])
            self.img_pkmn[i].append(ImageTk.PhotoImage(self.img_pkmn_base))

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

    def replace_images(self):
        if self.game_activated:
            ext = ['_inactive.png', '_active.png', '_unknown.png', '_banned.png', '_picked.png']
            for i in range(len(ext)):
                for j in range(len(self.img_pkmn[i])):
                    if self.show_megas.get() == 'Yes':
                        if is_mega(self.pkmn_pool_list[j]):
                            if self.pkmn_pool_list[j].item.endswith('ite X'):
                                pkmn_name = self.pkmn_pool_list[j].name + '-Mega-X'
                            elif self.pkmn_pool_list[j].item.endswith('ite Y'):
                                pkmn_name = self.pkmn_pool_list[j].name + '-Mega-X'
                            elif self.pkmn_pool_list[j].ability == 'Battle Bond':
                                pkmn_name = self.pkmn_pool_list[j].name + '-Ash'
                            else:
                                pkmn_name = self.pkmn_pool_list[j].name + '-Mega'
                            self.img_pkmn_base = RGBAImage2(os.path.join(IMG_PKMN_DIR, pkmn_name + ext[i]))
                            self.img_pkmn_base.paste(
                                self.controller.img_border[self.draft_mode.get()],
                                (0, 0),
                            self.controller.img_border[self.draft_mode.get()])
                            self.img_pkmn[i][j] = ImageTk.PhotoImage(self.img_pkmn_base)
                    else:
                        pkmn_name = self.pkmn_pool_list[j].name
                        pkmn_name = pkmn_name.replace('-Small', '').replace('-Large', '').replace('-Super', '').replace(':', '')
                        self.img_pkmn_base = RGBAImage2(os.path.join(IMG_PKMN_DIR, pkmn_name + ext[i]))
                        self.img_pkmn_base.paste(
                            self.controller.img_border[self.draft_mode.get()],
                            (0, 0),
                            self.controller.img_border[self.draft_mode.get()])
                        self.img_pkmn[i][j] = ImageTk.PhotoImage(self.img_pkmn_base)
            for i in range(len(self.img_pkmn[0])):
                if self.pkmn_not_picked[i]:
                    self.pool_buttons[i].config(image=self.img_pkmn[0][i])
                else:
                    self.pool_buttons[i].config(image=self.img_pkmn[4][i])
            for i in range(2):
                for j in range(6):
                    if self.pkmn_team_list[i][j] != None:
                        pool_num = self.get_pool_num(self.pkmn_team_list[i][j].name)
                        self.team_buttons[i][j].config(image=self.img_pkmn[0][pool_num])


    def get_pool_num(self, pkmn_name):
        for i in range(18):
            if self.pkmn_pool_list[i].name == pkmn_name:
                return i


class DraftSettings(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        setup_game_settings(self, 'Draft')

    def update_gen_settings(self):
        if self.parent_page().battle_mode.get() == 'Singles' or self.parent_page().battle_mode.get() == 'SRL':
            for i in range(len(self.controller.pages['DraftGenerateSettings'].tier_buttons)):
                self.controller.pages['DraftGenerateSettings'].tier_buttons[i].config(state='normal')
            for i in range(len(self.controller.pages['DraftGenerateSettings'].tier2_buttons)):
                self.controller.pages['DraftGenerateSettings'].tier2_buttons[i].config(state='disabled')
        if self.parent_page().battle_mode.get() == 'Doubles':
            for i in range(len(self.controller.pages['DraftGenerateSettings'].tier_buttons)):
                self.controller.pages['DraftGenerateSettings'].tier_buttons[i].config(state='disabled')
            for i in range(len(self.controller.pages['DraftGenerateSettings'].tier2_buttons)):
                self.controller.pages['DraftGenerateSettings'].tier2_buttons[i].config(state='normal')

    def activate_bans(self):
        for i in range(2):
            for j in range(0, self.parent_page().ban_number.get()):
                self.parent_page().ban_buttons[i][j].config(state='normal',
                                                            command=None)
            for j in range(self.parent_page().ban_number.get(), 2):
                self.parent_page().ban_buttons[i][j].config(state='disabled',
                                                            command=None)
        self.parent_page().ban_phase_finished = False
        if self.parent_page().ban_number.get() == 0:
            self.parent_page().ban_text.config(state='disabled')
        else:
            self.parent_page().ban_text.config(state='normal')

    def parent_page(self):
        return self.controller.pages['Draft']

    def exit(self):
        self.parent_page().replace_images()
        self.controller.show_frame('Draft')


class DraftGenerateSettings(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        setup_settings(self, 'Draft')

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
        self.show_megas = tk.StringVar()
        self.show_megas.set('No')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.img_pkmn = [[] for i in range(2)]
        self.frames = []
        for i in range(2):
            self.frames.append(tk.Frame(self))
            self.frames[i].grid(row=i, column=0, sticky='nsew')
        self.frames[1].config(bg='red')
        self.frames[0].grid_columnconfigure(0, weight=1)
        self.frames[0].grid_columnconfigure(3, weight=1)
        self.frames[0].grid_columnconfigure(6, weight=1)

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
            self.team_text.append(tk.Label(self.frames[0], text='TEAM %s' % str(team+1)))
            self.team_text[team].grid(row=1, column=(team*3)+1, columnspan=2,
                                      sticky='nsew')
            for row in range(3):
                for column in range(2):
                    x = (row * 2) + column
                    self.team_buttons[team].append(tk.Button(self.frames[0],
                                                             image=self.controller.img_blank[0],
                                                             bd=0.1,
                                                             command=None))
                    self.team_buttons[team][x].grid(row=row+2,
                                                    column=(team*3)+column+1,
                                                    padx=5, pady=5)
                    self.team_buttons[team][x].bind('<Enter>', lambda event, team=team, x=x: self.team_on_enter(team, x))
                    self.team_buttons[team][x].bind('<Leave>', lambda event, team=team, x=x: self.team_on_leave(team, x))

    def new_game(self):
        # reset private variables
        self.game_activated = True
        self.pkmn_team_list = [[None for i in range(6)] for j in range(2)]
        self.img_pkmn = [[] for i in range(2)]

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
                if self.show_megas.get() == 'Yes':
                    if is_mega(self.pkmn_team_list[i][j]):
                        if self.pkmn_team_list[i][j].item.endswith('ite X'):
                            pkmn_name = self.pkmn_team_list[i][j].name + '-Mega-X'
                        elif self.pkmn_team_list[i][j].item.endswith('ite Y'):
                            pkmn_name = self.pkmn_team_list[i][j].name + '-Mega-X'
                        elif self.pkmn_team_list[i][j].ability == 'Battle Bond':
                            pkmn_name = self.pkmn_team_list[i][j].name + '-Ash'
                        else:
                            pkmn_name = self.pkmn_team_list[i][j].name + '-Mega'
                    else:
                        pkmn_name = self.pkmn_team_list[i][j].name
                else:
                    pkmn_name = self.pkmn_team_list[i][j].name
                self.get_pkmn_imgs(pkmn_name)
                x = (i * 6) + j
                self.team_buttons[i][j].config(image=self.img_pkmn[0][x],
                                               command=lambda i=i, j=j: self.reroll(i, j))
        self.controller.sidebar.finish_button.config(state='normal',
                                                     command=lambda: get_sets(self))

    def get_pkmn_imgs(self, pkmn_name):
        pkmn_name = pkmn_name.replace('-Small', '').replace('-Large', '').replace('-Super', '').replace(':', '')
        self.img_pkmn_base = [RGBAImage2(os.path.join(IMG_PKMN_DIR, pkmn_name + '_inactive.png')),
                              RGBAImage2(os.path.join(IMG_PKMN_DIR, pkmn_name + '_active.png')),
                              RGBAImage2(os.path.join(IMG_PKMN_DIR, pkmn_name + '_unknown.png'))]
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

    def replace_images(self):
        if self.game_activated:
            for i in range(len(self.pkmn_team_list)):
                for j in range(len(self.pkmn_team_list[i])):
                    x = (i * 6) + j
                    if self.show_megas.get() == 'Yes':
                        if is_mega(self.pkmn_team_list[i][j]):
                            if self.pkmn_team_list[i][j].item.endswith('ite X'):
                                pkmn_name = self.pkmn_team_list[i][j].name + '-Mega-X'
                            elif self.pkmn_team_list[i][j].item.endswith('ite Y'):
                                pkmn_name = self.pkmn_team_list[i][j].name + '-Mega-X'
                            elif self.pkmn_team_list[i][j].ability == 'Battle Bond':
                                pkmn_name = self.pkmn_team_list[i][j].name + '-Ash'
                            else:
                                pkmn_name = self.pkmn_team_list[i][j].name + '-Mega'
                            self.img_pkmn_base = [
                                RGBAImage2(os.path.join(IMG_PKMN_DIR, pkmn_name + '_inactive.png')),
                                RGBAImage2(os.path.join(IMG_PKMN_DIR, pkmn_name + '_active.png')),
                                RGBAImage2(os.path.join(IMG_PKMN_DIR, pkmn_name + '_unknown.png'))]
                            for k in range(2):
                                self.img_pkmn_base[k].paste(
                                    self.controller.img_border['Random'],
                                    (0, 0),
                                    self.controller.img_border['Random'])
                                self.img_pkmn[k][x] = ImageTk.PhotoImage(self.img_pkmn_base[k])
                    else:
                        pkmn_name = self.pkmn_team_list[i][j].name
                        pkmn_name = pkmn_name.replace('-Small', '').replace('-Large', '').replace('-Super', '').replace(':', '')
                        self.img_pkmn_base = [
                            RGBAImage2(os.path.join(IMG_PKMN_DIR, pkmn_name + '_inactive.png')),
                            RGBAImage2(os.path.join(IMG_PKMN_DIR, pkmn_name + '_active.png')),
                            RGBAImage2(os.path.join(IMG_PKMN_DIR, pkmn_name + '_unknown.png'))]
                        for k in range(2):
                            self.img_pkmn_base[k].paste(
                                self.controller.img_border['Random'],
                                (0, 0),
                                self.controller.img_border['Random'])
                            self.img_pkmn[k][x] = ImageTk.PhotoImage(self.img_pkmn_base[k])
            for i in range(2):
                for j in range(6):
                    x = (i * 6) + j
                    self.team_buttons[i][j].config(image=self.img_pkmn[0][x])


class RandomSettings(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        setup_game_settings(self, 'Random')

    def update_gen_settings(self):
        if self.parent_page().battle_mode.get() == 'Singles' or self.parent_page().battle_mode.get() == 'SRL':
            for i in range(len(self.controller.pages['RandomGenerateSettings'].tier_buttons)):
                self.controller.pages['RandomGenerateSettings'].tier_buttons[i].config(state='normal')
            for i in range(len(self.controller.pages['RandomGenerateSettings'].tier2_buttons)):
                self.controller.pages['RandomGenerateSettings'].tier2_buttons[i].config(state='disabled')
        if self.parent_page().battle_mode.get() == 'Doubles':
            for i in range(len(self.controller.pages['RandomGenerateSettings'].tier_buttons)):
                self.controller.pages['RandomGenerateSettings'].tier_buttons[i].config(state='disabled')
            for i in range(len(self.controller.pages['RandomGenerateSettings'].tier2_buttons)):
                self.controller.pages['RandomGenerateSettings'].tier2_buttons[i].config(state='normal')

    def parent_page(self):
        return self.controller.pages['Random']

    def exit(self):
        self.parent_page().replace_images()
        self.controller.show_frame('Random')


class RandomGenerateSettings(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        setup_settings(self, 'Random')

    def parent_page(self):
        return self.controller.pages['Random']


class Store(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.banner_num = 0
        self.current_page = 0
        self.help_num = 0
        self.remaining = 43
        self.current_player = tk.StringVar()
        self.current_player.set(PLAYERS[0].name)

        self.img_banners = []
        self.img_banner_buttons = []
        self.img_banner_help = []
        for i in range(self.banner_num, self.banner_num+2):
            self.img_banners.append(
                RGBAImage(os.path.join(COMMON, 'banner%s_fit.png' % i)))
            self.img_banner_buttons.append(
                RGBAImage(os.path.join(COMMON, 'banner%s_button.png' % i)))
            self.img_banner_help.append(
                RGBAImage(os.path.join(COMMON, 'banner%s_help.png' % i)))
        self.banner_image = tk.Label(self, image=self.img_banners[self.banner_num])
        self.banner_image.grid(row=0, column=0, columnspan=4, sticky='nsew')
        self.page_frame = tk.Frame(self)
        self.page_frame.grid(row=2, column=0, columnspan=4, sticky='nsew')
        for i in range(4):
            self.page_frame.grid_columnconfigure(i, weight=1)
        self.page_buttons = []
        self.help_buttons = []
        for i in range(2):
            self.page_buttons.append(tk.Button(self.page_frame,
                image=self.img_banner_buttons[i],
                bd=0.1,
                command=lambda i=i: self.change_page(i)))
            self.page_buttons[i].grid(row=0, column=i*2, padx=5, sticky='nsw')
            self.help_buttons.append(tk.Button(self.page_frame,
                image=self.img_banner_help[i],
                bd=0.1,
                command=lambda i=i: self.view_help(i)))
            self.help_buttons[i].grid(row=0, column=(i*2)+1, sticky='nsw')

        self.scrollframe = tk.LabelFrame(self, text='Remaining Pokemon')
        self.scrollframe.grid(row=3, column=0, rowspan=5, columnspan=4, padx=5,
                              pady=5, sticky='nsew')
        self.container = tk.Canvas(self.scrollframe,
                                   scrollregion=(0, 0, 400, 640))
        self.scrollbar = ttk.Scrollbar(self.scrollframe, orient='vertical',
                                       command=self.container.yview)
        self.container.config(yscrollcommand=self.scrollbar.set)
        self.container.bind('<Enter>', self._on_mousewheel)
        self.container.bind('<Leave>', self._off_mousewheel)
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

        self.pull_result = tk.Label(self, image=self.controller.img_blank[0])
        self.pull_result.grid(row=8, column=0, padx=5, pady=5, sticky='nsew')
        self.player_option = tk.OptionMenu(self, self.current_player,
                                         *playerNames, command=self.switch_player)
        self.player_option.grid(row=8, column=1, padx=5, pady=5, sticky='ew')

        self.pull_img = []
        for i in ['inactive', 'active']:
            self.pull_img.append(RGBAImage(os.path.join(COMMON,
                                                        'button_%s_Pull.png' % i)))
        self.pull_button = tk.Button(self, image=self.pull_img[0], bd=0.1,
                                     command=self.pull)
        self.pull_button.grid(row=8, column=2)
        self.pull_button.bind('<Enter>', lambda event: self.on_enter())
        self.pull_button.bind('<Leave>', lambda event: self.on_leave())
        self.remaining_label = tk.Label(self, text='%d/43' % self.remaining)
        self.remaining_label.grid(row=8, column=3, pady=5, sticky='nsew')

        self.pkmn_lists = [[], []]
        for pkmn in ALL_POKEMON_S:
            if pkmn.srl_group == self.banner_num:
                self.pkmn_lists[0].append(pkmn)
            if pkmn.srl_group == self.banner_num+1:
                self.pkmn_lists[1].append(pkmn)

        self.switch_player(self.current_player.get())

        for i in range(9):
            self.grid_rowconfigure(i, weight=1)
        for i in range(4):
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
                        self.controller.img_border[get_rarity(pkmn_name)],
                        (0, 0),
                        self.controller.img_border[get_rarity(pkmn_name)])
                    self.img_pkmn[i][k].append(
                        ImageTk.PhotoImage(self.img_pkmn_base[k]))

    def _on_mousewheel(self, event):
        self.container.bind_all('<MouseWheel>', self._scroll)

    def _off_mousewheel(self, event):
        self.container.unbind_all('<MouseWheel>')

    def _scroll(self, event):
        self.container.yview_scroll(int(-1*(event.delta/120)), 'units')

    def switch_player(self, player):
        self.remaining = 43
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
                    self.remaining -= 1
                else:
                    self.pkmn_buttons[i][j].config(
                        image=self.img_pkmn[current_banner][0][x],
                        command=lambda x=x: self.add_to_team(x))
        self.remaining_label.config(text='%d/43' % self.remaining)

    def pull(self):
        current_banner = self.banner_num + self.current_page
        slot = playerNames.index(self.current_player.get())
        player_pkmn_list = PLAYERS[slot].pkmn_list
        player_pkmn_name_list = [get_mega_name(i) for i in player_pkmn_list]
        print(player_pkmn_name_list)
        while True:
            temp_new_pkmn = random.choice(self.pkmn_lists[current_banner])
            print(get_true_name(temp_new_pkmn.name))
            if get_true_name(temp_new_pkmn.name) not in player_pkmn_name_list:
                PLAYERS[slot].pkmn_list.append(temp_new_pkmn)
                pkmn_index = ALL_BANNERS[current_banner].index(
                    get_true_name(temp_new_pkmn.name))
                for i in range(9):
                    for j in range(len(self.pkmn_buttons[i])):
                        x = (i * 5) + j
                        if x == pkmn_index:
                            self.pkmn_buttons[i][j].config(
                                image=self.img_pkmn[current_banner][2][x],
                                command=lambda x=x: self.remove_from_team(x))
                            self.pull_result.config(
                                image=self.img_pkmn[current_banner][0][x])
                            self.remaining -= 1
                            self.remaining_label.config(text='%d/43' % self.remaining)
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
        self.remaining -= 1
        self.remaining_label.config(text='%d/43' % self.remaining)

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
        self.remaining += 1
        self.remaining_label.config(text='%d/43' % self.remaining)

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

    def on_enter(self):
        self.pull_button.config(image=self.pull_img[1])

    def on_leave(self):
        self.pull_button.config(image=self.pull_img[0])

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

    def view_help(self, banner_num):
        self.help_num = banner_num
        self.controller.show_frame('HelpPage')


class Players(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.current_player = tk.StringVar()
        self.current_player.set(PLAYERS[0].name)

        # add new player
        self.new_player_img = RGBAImage(os.path.join(COMMON, 'label_new_player.png'))
        self.new_player_label = tk.Label(self, image=self.new_player_img)
        self.new_player_label.grid(row=0, column=0, columnspan=2, pady=4, sticky='nsw')
        # new player text | entry widget | add button?
        self.name_img = RGBAImage(os.path.join(COMMON, 'label_name.png'))
        self.name_text = tk.Label(self, image=self.name_img, justify='right')
        self.name_text.grid(row=1, column=0, sticky='nse')
        self.enter_name = tk.Entry(self)
        self.enter_name.grid(row=1, column=1, sticky='ew')
        self.add_button = tk.Button(self, text='Add New Player', command=self.add_player)
        self.add_button.grid(row=1, column=2, padx=10, sticky='ew')
        # view player inventories
        self.collect_img = RGBAImage(os.path.join(COMMON, 'label_collections.png'))
        self.collect_text = tk.Label(self, image=self.collect_img)
        self.collect_text.grid(row=2, column=0, columnspan=2, pady=(20,10), sticky='nsw')
        # text instructions | drop down | get all set details
        self.player_instruct_img = RGBAImage(os.path.join(COMMON, 'label_instruct.png'))
        self.player_instruct_text = tk.Label(self, image=self.player_instruct_img)
        self.player_instruct_text.grid(row=3, column=0, sticky='nse')
        self.player_option = tk.OptionMenu(self, self.current_player,
                                         *playerNames, command=None)
        self.player_option.grid(row=3, column=1, sticky='ew')
        self.get_sets_button = tk.Button(self, text='Get Set Info', command=None)
        self.get_sets_button.grid(row=3, column=2, padx=10, sticky='ew')
        # [grid with pokemon icons]
        self.scrollframe = tk.LabelFrame(self, text='Remaining Pokemon')
        self.scrollframe.grid(row=4, column=0, rowspan=3, columnspan=3, padx=5,
                              pady=5, sticky='nsew')
        self.container = tk.Canvas(self.scrollframe,
                                   scrollregion=(0, 0, 400, 640))
        self.scrollbar = ttk.Scrollbar(self.scrollframe, orient='vertical',
                                       command=self.container.yview)
        self.container.config(yscrollcommand=self.scrollbar.set)
        self.container.bind('<Enter>', self._on_mousewheel)
        self.container.bind('<Leave>', self._off_mousewheel)
        self.scrollbar.pack(side='right', fill='y')
        self.container.pack(side='left', expand=True, fill='both')


        for i in range(1, 3):
            self.grid_columnconfigure(i, weight=1)

    def add_player(self):
        player_name = self.enter_name.get().strip()
        self.enter_name.delete(0, 'end')
        if player_name and player_name.lower() not in [i.lower() for i in playerNames]:
            empty_list = []
            PLAYERS.append(Player(player_name, empty_list))
            playerNames.append(player_name)
            # update option menus and open new pull page
            update_all_optionmenus(self.controller)
            self.controller.show_frame('NewPull')

        elif player_name.lower() in [i.lower() for i in playerNames]:
            top = tk.Toplevel(self.controller)
            top.grab_set()
            text = player_name + ' is already in use. Please choose another name.'
            message = tk.Label(top, text=text)
            message.grid(row=0, column=0, padx=20, pady=20, sticky='nsew')
            back_button = tk.Button(top, text='Ok', command=top.destroy)
            back_button.grid(row=1, column=0, padx=100, pady=5, sticky='nsew')
        else:
            pass


    def _on_mousewheel(self, event):
        self.container.bind_all('<MouseWheel>', self._scroll)

    def _off_mousewheel(self, event):
        self.container.unbind_all('<MouseWheel>')

    def _scroll(self, event):
        self.container.yview_scroll(int(-1*(event.delta/120)), 'units')


class HelpPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.page_num = 0


class NewPull(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller


def update_all_optionmenus(self):
    menu1 = self.pages['Store'].player_option['menu']
    menu2 = self.pages['Players'].player_option['menu']
    menu1.delete(0, 'end')
    menu2.delete(0, 'end')
    for player in playerNames:
        menu1.add_command(label=player, command=self.pages['Store'].switch_player(player))
        menu2.add_command(label=player)

def get_true_name(name):
    return name.replace('-Mega-X', '').replace('-Mega-Y', '').replace('-Ash', '').replace('-Mega', '')


def get_mega_name(pkmn):
    if ((pkmn.item != 'Eviolite' and (pkmn.item.endswith('ite') or
        pkmn.item.endswith('ite X') or pkmn.item.endswith('ite Y'))) or
        ('Dragon Ascent' in pkmn.moves):
        return pkmn.name + '-Mega'


def get_rarity(name):
    for pkmn in ALL_POKEMON_S:
        if name.endswith('-Mega'):
            temp_name = name.replace('-Mega', '')
            if (pkmn.name == temp_name and
                (pkmn.item.endswith('ite') or pkmn.item.endswith('ite X') or
                 pkmn.item.endswith('ite Y'))):
                rarity = pkmn.rarity
                break
        elif name.endswith('-Ash'):
            temp_name = name.replace('-Ash', '')
            if (pkmn.name == temp_name and pkmn.ability == 'Battle Bond'):
                rarity = pkmn.rarity
                break
        else:
            if pkmn.name == name:
                rarity = pkmn.rarity
                break
    return rarity


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
        self.controller.show_frame(page)
    else:
        top = tk.Toplevel(self.controller)
        top.grab_set()
        text = 'Not enough Pokemon fit the criteria you have selected.'
        text2 = '\nPlease remove some restrictions.'
        message = tk.Label(top, text=text+text2)
        message.grid(row=0, column=0, padx=20, pady=20, sticky='nsew')
        back_button = tk.Button(top, text='Ok', command=top.destroy)
        back_button.grid(row=1, column=0, padx=100, pady=5, sticky='nsew')


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
    if hasattr(self.parent_page(), 'pool_buttons'):
        for i in range(len(self.parent_page().pool_buttons)):
            self.parent_page().pool_buttons[i].config(
                image=self.parent_page().controller.img_blank[0],
                command=None)
    if hasattr(self.parent_page(), 'ban_buttons'):
        for i in range(len(self.parent_page().ban_buttons)):
            for j in range(len(self.parent_page().ban_buttons[i])):
                self.parent_page().ban_buttons[i][j].config(
                    image=self.parent_page().controller.img_blank[0],
                    command=None)
    if hasattr(self.parent_page(), 'team_buttons'):
        for i in range(len(self.parent_page().team_buttons)):
            for j in range(len(self.parent_page().team_buttons[i])):
                self.parent_page().team_buttons[i][j].config(
                    image=self.parent_page().controller.img_blank[0],
                    command=None)


def setup_settings(self, page):
    self.exclusions_img = RGBAImage(os.path.join(COMMON, 'label_exclusions.png'))
    self.exclusions_text = tk.Label(self, image=self.exclusions_img)
    self.exclusions_text.grid(row=0, column=0, columnspan=6, pady=2, sticky='nsw')
    self.tier_text = tk.Label(self, text='Tiers (Singles)')
    self.tier_text.grid(row=1, column=0, rowspan=2, sticky='w')
    self.tier_buttons = []
    for i in range(len(TIERS_SINGLES)):
        self.tier_buttons.append(tk.Checkbutton(self, text=TIERS_SINGLES[i],
            variable=self.parent_page().pkmn_excl_tiers_s[i],
            onvalue=TIERS_SINGLES[i],
            offvalue=''))
        self.tier_buttons[i].grid(row=1 + int(i / 5), column=(i % 5) + 1,
                                  sticky='w')

    self.separators = [ttk.Separator(self, orient='horizontal') for i in range(7)]
    self.separators[0].grid(row=3, column=0, columnspan=6, sticky='nsew')


    self.tier2_text = tk.Label(self, text='Tiers (Doubles)')
    self.tier2_text.grid(row=4, column=0, sticky='w')
    self.tier2_buttons = []
    for i in range(len(TIERS_DOUBLES)):
        self.tier2_buttons.append(tk.Checkbutton(self, text=TIERS_DOUBLES[i],
            variable=self.parent_page().pkmn_excl_tiers_d[i],
            onvalue=TIERS_DOUBLES[i],
            state='disabled',
            offvalue=''))
        self.tier2_buttons[i].grid(row=4 + int(i / 5), column=(i % 5) + 1,
                                   sticky='w')

    self.separators[1].grid(row=5, column=0, columnspan=6, sticky='nsew')

    self.gen_text = tk.Label(self, text='Generations')
    self.gen_text.grid(row=6, column=0, rowspan=2, sticky='w')
    self.gen_buttons = []
    for i in range(len(GENERATIONS)):
        self.gen_buttons.append(tk.Checkbutton(self, text=GENERATIONS[i],
            variable=self.parent_page().pkmn_excl_gens[i],
            onvalue=GENERATIONS[i],
            offvalue=''))
        self.gen_buttons[i].grid(row=6 + int(i / 5), column=(i % 5) + 1,
                                 sticky='w')

    self.separators[2].grid(row=8, column=0, columnspan=6, sticky='nsew')

    self.type_text = tk.Label(self, text='Types')
    self.type_text.grid(row=9, column=0, rowspan=4, sticky='w')
    self.type_buttons = []
    for i in range(len(TYPES)):
        self.type_buttons.append(tk.Checkbutton(self, text=TYPES[i],
            variable=self.parent_page().pkmn_excl_types[i],
            onvalue=TYPES[i],
            offvalue=''))
        self.type_buttons[i].grid(row=9 + int(i / 5), column=(i % 5) + 1,
                                  sticky='w')

    self.separators[3].grid(row=13, column=0, columnspan=6, sticky='nsew')

    self.item_text = tk.Label(self, text='Items')
    self.item_text.grid(row=14, column=0, rowspan=2, sticky='w')
    self.item_buttons = []
    for i in range(len(ITEMS)):
        self.item_buttons.append(tk.Checkbutton(self, text=ITEMS[i],
            variable=self.parent_page().pkmn_excl_items[i],
            onvalue=ITEMS[i],
            offvalue=''))
        self.item_buttons[i].grid(row=14 + int(i / 5), column=(i % 5) + 1,
                                  sticky='w')

    self.separators[4].grid(row=16, column=0, columnspan=6, sticky='nsew')

    self.gimmick_text = tk.Label(self, text='Gimmicks')
    self.gimmick_text.grid(row=17, column=0, rowspan=3, sticky='w')
    self.gimmick_buttons = []
    for i in range(len(GIMMICKS)):
        self.gimmick_buttons.append(tk.Checkbutton(self, text=GIMMICKS[i],
            variable=self.parent_page().pkmn_excl_gimmicks[i],
            onvalue=GIMMICKS[i],
            offvalue=''))
        self.gimmick_buttons[i].grid(row=17 + int(i / 5), column=(i % 5) + 1,
                                     sticky='w')

    self.separators[5].grid(row=20, column=0, columnspan=6, sticky='nsew')

    self.usage_text = tk.Label(self, text='Usage')
    self.usage_text.grid(row=21, column=0, sticky='w')

    self.separators[6].grid(row=22, column=0, columnspan=6, sticky='nsew')
    self.back_button = tk.Button(self, text='Back', command=lambda: validate(self, page))
    self.back_button.grid(row=23, column=1, columnspan=4, padx=5, pady=5,
                          sticky='nsew')


def setup_game_settings(self, page):
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
        self.battle_mode_buttons[i].grid(row=1+int(i/5), column=(i % 5)+1,
                                         padx=5, pady=5, sticky='nsew')
    if page == 'Draft':
        self.draft_mode_text = tk.Label(self, text='Draft Mode')
        self.draft_mode_text.grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.draft_mode_buttons = []
        draft_modes = ['Standard', 'Nemesis', 'First Pick']
        for i in range(len(draft_modes)):
            self.draft_mode_buttons.append(tk.Radiobutton(self,
                text=draft_modes[i],
                variable=self.parent_page().draft_mode,
                indicatoron=0,
                value=draft_modes[i]))
            self.draft_mode_buttons[i].grid(row=2 + int(i / 5),
                                            column=(i % 5) + 1,
                                            padx=5, pady=5, sticky='nsew')

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
                command=self.activate_bans))
            self.ban_number_buttons[i].grid(row=3 + int(i / 5),
                                            column=(i % 5) + 1,
                                            padx=5, pady=5, sticky='nsew')
    else:
        self.theme_text = tk.Label(self, text='Theme')
        self.theme_text.grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.theme_buttons = []
        themes = ['Random', 'Balanced', 'Monotype']
        for i in range(len(themes)):
            self.theme_buttons.append(tk.Radiobutton(self, text=themes[i],
                variable=self.parent_page().theme,
                indicatoron=0,
                width=10,
                value=themes[i]))
            self.theme_buttons[i].grid(row=2+int(i/5), column=(i % 5)+1, padx=5,
                                       pady=5, sticky='nsew')

    self.mega_text = tk.Label(self, text='Show Megas')
    self.mega_text.grid(row=4, column=0, padx=5, pady=5, sticky='w')
    self.mega_buttons = []
    megas = ['No', 'Yes']
    for i in range(len(megas)):
        self.mega_buttons.append(tk.Radiobutton(self,
            text=megas[i],
            variable=self.parent_page().show_megas,
            indicatoron=0,
            value=megas[i],
            command=self.parent_page().replace_images))
        self.mega_buttons[i].grid(row=4+ int(i/5), column=(i % 5) + 1,
                                  padx=5, pady=5, sticky='nsew')

    self.back_button = tk.Button(self, text='Back', command=self.exit)
    self.back_button.grid(row=15, column=1, columnspan=2,
                          padx=5, pady=5, sticky='nsew')

    for i in range(8):
        self.grid_rowconfigure(i, weight=1)
    for i in range(4):
        self.grid_columnconfigure(i, weight=1)


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
    if not os.listdir(PLAYER_DIR):
        with open(os.path.join(PLAYER_DIR, 'Virgo.csv'), 'w') as file:
            pass
    for filename in os.listdir(PLAYER_DIR):
        if filename.endswith('.csv'):
            with open(os.path.join(PLAYER_DIR, filename), 'r') as file:
                player_name = os.path.splitext(os.path.basename(file.name))[0]
                reader = csv.reader(file)
                temp_pkmn_list = []
                for row in reader:
                    if row:
                        temp_pkmn_list.append(Pokemon(row))
                PLAYERS.append(Player(player_name, temp_pkmn_list))
                playerNames.append(player_name)


def RGBAImage(path):
    return ImageTk.PhotoImage(Image.open(path).convert('RGBA'))


def RGBAImage2(path):
    return Image.open(path).convert('RGBA')


class Player:
    def __init__(self, name, pkmn_list):
        self.name = name
        self.pkmn_list = pkmn_list


if __name__ == '__main__':
    init_player_information()
    app = MainApp()
    app.mainloop()
