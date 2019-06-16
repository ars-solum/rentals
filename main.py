"""
main.py
Purpose : Creates an interactive GUI for the Pokemon Rentals Database and
          related streaming activities.

Author  : Ars Solum
Version : 2.2.0
"""

import csv
from datetime import date
import os
from PIL import Image, ImageTk
import random
from random import shuffle
import tkinter as tk
from tkinter.font import Font
from tkinter import ttk

from Pokemon import *

class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.init_vars()
        self.init_side_menu()
        self.init_main_menu()

        self.change_page('Draft')

    def init_vars(self):
        self.img_type = ['inactive', 'active', 'unknown', 'banned', 'picked']
        self.img_blank_base = {
            'active': RGBAImage2(os.path.join(COMMON, 'button_active_Blank.png')),
            'inactive': RGBAImage2(os.path.join(COMMON, 'button_inactive_Blank.png'))
        }
        self.img_border = {
            'Standard': RGBAImage2(os.path.join(COMMON, 'border_Standard.png')),
            'Nemesis': RGBAImage2(os.path.join(COMMON, 'border_Nemesis.png')),
            'Random': RGBAImage2(os.path.join(COMMON, 'border_Random.png')),
            'First Pick': RGBAImage2(os.path.join(COMMON, 'border_First Pick.png')),
            'COMMON': RGBAImage2(os.path.join(COMMON, 'border_COMMON.png')),
            'RARE': RGBAImage2(os.path.join(COMMON, 'border_RARE.png')),
            'ULTRA-RARE': RGBAImage2(os.path.join(COMMON, 'border_ULTRA-RARE.png'))
        }

        for key in self.img_blank_base:
            create_image(self.img_blank_base[key], self.img_border['Standard'])

        self.img_blank = {
            'inactive': ImageTk.PhotoImage(self.img_blank_base['inactive']),
            'active': ImageTk.PhotoImage(self.img_blank_base['active'])
        }
        self.img_team_text = {
            'team 1': RGBAImage(os.path.join(COMMON, 'team1.png')),
            'team 2': RGBAImage(os.path.join(COMMON, 'team2.png'))
        }
        self.img_help = {
            'active': RGBAImage(os.path.join(COMMON, 'button_active_help.png')),
            'inactive': RGBAImage(os.path.join(COMMON, 'button_inactive_help.png'))
        }
        self.img_back = {
            'active': RGBAImage(os.path.join(COMMON, 'button_active_back.png')),
            'inactive': RGBAImage(os.path.join(COMMON, 'button_inactive_back.png'))
        }
        self.img_error = RGBAImage(os.path.join(COMMON, 'error.png'))
        self.img_info = RGBAImage(os.path.join(COMMON, 'info.png'))

    def init_side_menu(self):
        self.frame_side_menu = tk.Frame(self)
        self.frame_side_menu.grid(row=0, column=0, sticky='nsew')

        self.frame_side_menu.grid_rowconfigure(0, weight=1)
        self.frame_side_menu.grid_columnconfigure(0, weight=1)

        self.sidebar = Sidebar(parent=self.frame_side_menu, controller=self)
        self.sidebar.grid(row=0, column=0, sticky='nsew')
        self.current_page = 'Draft'
        self.load_page = False

    def init_main_menu(self):
        self.main_frame = tk.Frame(self)
        self.main_frame.grid(row=0, column=1, sticky='nsew')

        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.pages = {}

        # create each page
        for page in (Draft, Random, DraftSettings, DraftGenerateSettings,
                     RandomSettings, RandomGenerateSettings, Store, StoreSettings, Players,
                     StoreHelpPage, NewPullHelpPage, NewPull, Portrait, Details):
            page_name = page.__name__
            frame = page(parent=self.main_frame, controller=self)
            self.pages[page_name] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        # modify the start button
        self.sidebar.buttons['Game'].config(command=self.pages['Draft'].new_game)

    def change_page(self, page_name):
        if (page_name == 'Store' and len(PLAYERS) == 1 and len(PLAYERS[0].pkmn_list) == 0):
            popup_message(self, 'ERROR', 'You cannot visit the store right now.', text2='\nPlease roll for your first team.')
        elif (page_name == 'Players' and len(PLAYERS) == 1 and len(PLAYERS[0].pkmn_list) == 0):
            # change button bindings
            self.sidebar.buttons[self.current_page].config(image=self.sidebar.img_buttons[self.current_page]['inactive'])
            self.current_page = page_name
            self.sidebar.buttons[self.current_page].config(image=self.sidebar.img_buttons[self.current_page]['active'])
            self.sidebar.buttons[self.current_page].unbind('<Leave>')

            popup_message(self, 'INFO', "Welcome Virgo! Let's get your starter Pokemon!")

            # disable all sidebar buttons
            for key, button in self.sidebar.buttons.items():
                button.config(state='disabled')

            # redirect to Pull page
            frame = self.pages['NewPull']
            frame.tkraise()
        else:
            if (page_name == 'Draft' or page_name == 'Random'):
                for key, button in self.sidebar.buttons.items():
                    button.config(state='normal')
                    button.grid()
                # disable Sets button if game not finished
                if (self.pages[page_name].game_activated == False or
                    (hasattr(self.pages[page_name], 'turn') and self.pages[page_name].turn < 12)):
                    self.sidebar.buttons['Sets'].config(state='disabled')

                # reconfigure settings buttons
                self.sidebar.buttons['game_settings'].config(command=lambda:self.change_page('%sSettings' % page_name))
                self.sidebar.buttons['pkmn_settings'].config(command=lambda:self.change_page('%sGenerateSettings' % page_name))
                self.sidebar.buttons['Game'].config(command=self.pages[page_name].new_game)
            else:
                # modify page-related buttons
                for key, button in self.sidebar.buttons.items():
                    if ('Settings' in page_name or 'Help' in page_name or 'NewPull' in page_name or 'Portrait' in page_name or 'Details' in page_name):
                        button.config(state='disabled')
                    else:
                        button.config(state='normal')
                if ('Store' == page_name or 'Players' == page_name):
                    for key in ['game_settings', 'pkmn_settings', 'Game', 'Sets']:
                        self.sidebar.buttons[key].config(state='disabled')

            if page_name == 'Players':
                # display current player's pokemon information
                self.pages[page_name].display_pkmn(self.pages[page_name].current_player.get())

            if page_name == 'Portrait':
                # update portrait info
                self.pages[page_name].cur_portrait.set(PLAYERS[playerNames.index(self.pages['Players'].current_player.get())].portrait)

            # change button bindings
            if not ('Settings' in page_name or 'Help' in page_name or 'NewPull' in page_name or 'Portrait' in page_name or 'Details' in page_name):
                if self.load_page:
                    self.sidebar.buttons[self.current_page].config(image=self.sidebar.img_buttons[self.current_page]['inactive'])
                self.load_page = True
                self.sidebar.buttons[self.current_page].bind('<Leave>', lambda event, page=self.current_page: self.on_leave(self.sidebar.buttons[page], self.sidebar.img_buttons[page]['inactive']))
                self.current_page = page_name
                self.sidebar.buttons[self.current_page].unbind('<Leave>')
            else:
                self.load_page = False
            # change the page
            frame = self.pages[page_name]
            frame.tkraise()

    def on_enter(self, button, image):
        if button.cget('state') != 'disabled':
            button.config(image=image)

    def on_leave(self, button, image):
        button.config(image=image)

    def HelpButton(self, source, page='', row=0, col=0, location=''):
        if not location:
            location = source
        source.help_button = tk.Button(location, image=self.img_help['inactive'],
            bd=0.1, command=lambda: self.change_page('%sHelpPage' % page))
        source.help_button.grid(row=row, column=col)
        source.help_button.bind('<Enter>', lambda event: self.on_enter(source.help_button, self.img_help['active']))
        source.help_button.bind('<Leave>', lambda event: self.on_leave(source.help_button, self.img_help['inactive']))

    def BackButton(self):
        if not location:
            location = source
        source.back_button = tk.Button(location, image=self.img_back['inactive'], bd=0.1)
        self.back_button = tk.Button(self, image=self.controller.img_back['inactive'], bd=0.1, command=lambda page=page: exit(self, page))
        # TODO FIXME
        self.back_button.grid(row=9, column=1, columnspan=2, padx=5, pady=5, sticky='nsew')
        self.back_button.bind('<Enter>', lambda event: self.controller.on_enter(self.back_button, self.controller.img_back['active']))
        self.back_button.bind('<Leave>', lambda event: self.controller.on_leave(self.back_button, self.controller.img_back['inactive']))


class Sidebar(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        for i in range(3):
            self.grid_rowconfigure(i, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # section | buttons
        self.text = {
            'battle': ['Draft', 'Random'],
            'league': ['Players', 'Store'],
            'settings': ['game_settings', 'pkmn_settings', 'Game', 'Sets']
        }

        self.frame_section = {}
        self.label_section = {}
        self.buttons = {}
        self.img_buttons = {}
        self.img_labels = {}

        # initialize images
        for section in self.text:
            self.img_labels[section] = RGBAImage(os.path.join(COMMON, '%s.png' %section))
        for section in self.text:
            for item in self.text[section]:
                self.img_buttons[item] = {}
        for key in self.img_buttons:
            for state in ['active', 'inactive']:
                self.img_buttons[key][state] = RGBAImage(os.path.join(COMMON, 'button_%s_%s.png' % (state, key)))
        self.empty_space = RGBAImage(os.path.join(COMMON, '3_empty_buttons.png'))

        tmp_ctr = 0 # keep track of which row to place the current section

        # construct each section
        for section in self.text:
            # special case: 3rd section should fill up space
            if tmp_ctr == 2:
                self.empty_space_label = tk.Label(self, image=self.empty_space)
                self.empty_space_label.grid(row=tmp_ctr, column=0, sticky='nsew')
                tmp_ctr += 1

            # initialize section frames
            self.frame_section[section] = tk.Frame(self)
            self.frame_section[section].grid(row=tmp_ctr, column=0, sticky='nsew')

            # initialize section labels
            self.label_section[section] = tk.Label(self.frame_section[section], image=self.img_labels[section])
            self.label_section[section].grid(row=0, column=0, sticky='nsew')

            # initialize the current section's buttons
            for button in self.text[section]: # button = Draft, etc.
                self.buttons[button] = tk.Button(self.frame_section[section], image=self.img_buttons[button]['active' if (button == 'Draft') else 'inactive'], bd=0.1)
                row = self.text[section].index(button) + 1 # skip over the first row for section title
                self.buttons[button].grid(row=row, column=0, sticky='nsew')
                self.buttons[button].bind('<Enter>', lambda event, button=button: self.controller.on_enter(self.buttons[button], self.img_buttons[button]['active']))
                self.buttons[button].bind('<Leave>', lambda event, button=button: self.controller.on_leave(self.buttons[button], self.img_buttons[button]['inactive']))

            tmp_ctr += 1

        # assign each button's command
        for section in self.text:
            if section == 'settings':
                self.buttons['game_settings'].config(command=lambda: self.controller.change_page('DraftSettings'))
                self.buttons['pkmn_settings'].config(command=lambda: self.controller.change_page('DraftGenerateSettings'))
            else:
                for button in self.text[section]:
                    self.buttons[button].config(command=lambda button=button: self.controller.change_page(button))


class Draft(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.bind('<Button-3>', lambda event: self.frame_popup(event))
        for i in range(1, 11):
            self.grid_rowconfigure(i, weight=1)
        for i in range(6):
            self.grid_columnconfigure(i, weight=1)

        self.init_vars()
        self.init_pool()
        self.init_bans()
        self.init_teams()

    def init_vars(self):
        self.turn = 0
        self.fp_team_order = [0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 2]
        self.fp_slot_order = [0, 1, 0, 1, 2, 3, 2, 3, 4, 5, 4, 5]
        self.game_activated = False
        self.pkmn_not_picked = [True for i in range(18)]
        self.img_pkmn = {}
        self.separators = [ttk.Separator(self, orient='horizontal') for i in range(2)]

        # game settings variables
        self.battle_mode = tk.StringVar()
        self.battle_mode.set('Singles')
        self.draft_mode = tk.StringVar()
        self.draft_mode.set('Standard')
        self.draft_num = 0
        self.ban_phase_finished = False
        self.ban_number = tk.IntVar()
        self.ban_number.set(0)
        self.show_megas = tk.StringVar()
        self.show_megas.set('No')
        self.hidden = tk.StringVar()
        self.hidden.set('No')
        self.current_player = [tk.StringVar(), tk.StringVar()]
        for i in range(2):
            self.current_player[i].set('' if (len(playerNames) < 2) else playerNames[i])

        # pokemon settings variables
        self.pkmn_excl_tiers_s = [tk.StringVar() for i in range(len(TIERS_SINGLES))]
        self.pkmn_excl_tiers_d = [tk.StringVar() for i in range(len(TIERS_DOUBLES))]
        self.pkmn_excl_gens = [tk.StringVar() for i in range(len(GENERATIONS))]
        self.pkmn_excl_types = [tk.StringVar() for i in range(len(TYPES))]
        self.pkmn_excl_items = [tk.StringVar() for i in range(len(ITEMS))]
        self.pkmn_excl_gimmicks = [tk.StringVar() for i in range(len(GIMMICKS))]
        self.pkmn_excl_usage = [] # unused

        self.checks = [[] for i in range(18)] # checks [unusued]
        self.ban_list = [[None, None], [None, None]]
        self.pkmn_team_list = [[None for i in range(6)] for j in range(2)]

    def init_pool(self):
        self.img_pool = RGBAImage(os.path.join(COMMON, 'label_pool.png'))
        self.label_pool = tk.Label(self, image=self.img_pool)
        self.label_pool.bind('<Button-3>', lambda event: self.frame_popup(event))
        self.label_pool.grid(row=0, column=0, columnspan=5, sticky='nsw')
        self.pkmn_pool_list = []
        self.pool_buttons = []
        for i in range(3):
            for j in range(6):
                x = (i*6) + j
                self.pool_buttons.append(tk.Button(self, image=self.controller.img_blank['inactive'], bd=0.1))
                self.pool_buttons[x].grid(row=i+1, column=j, pady=5)
                self.pool_buttons[x].bind('<Enter>', lambda event, x=x: self.controller.on_enter(self.pool_buttons[x], self.controller.img_blank['active']))
                self.pool_buttons[x].bind('<Leave>', lambda event, x=x: self.controller.on_leave(self.pool_buttons[x], self.controller.img_blank['inactive']))

    def init_bans(self):
        self.separators[0].grid(row=4, column=0, columnspan=6, sticky='nsew')
        self.img_ban = RGBAImage(os.path.join(COMMON, 'bans.png'))
        self.ban_text = tk.Button(self, image=self.img_ban, bd=0.1, state='disabled')
        self.ban_text.bind('<Button-3>', lambda event: self.frame_popup(event))
        self.ban_text.grid(row=5, column=2, columnspan=2, sticky='nsew')

        self.ban_buttons = [[], []]
        for i in range(2):
            for j in range(2):
                self.ban_buttons[i].append(tk.Button(self, image=self.controller.img_blank['inactive'], bd=0.1, state='disabled'))
                # order of buttons is 1 2 | 2 1
                self.ban_buttons[i][j].grid(row=5, column=(i*4+j) if (i == 0) else (i*5-j), pady=5)
        self.separators[1].grid(row=6, column=0, columnspan=6, sticky='nsew')

    def init_teams(self):
        self.team_text = []
        self.team_buttons = [[], []]
        for team in range(2):
            self.team_text.append(tk.Label(self, image=self.controller.img_team_text['team %d' % int(team+1)]))
            self.team_text[team].bind('<Button-3>', lambda event: self.frame_popup(event))
            self.team_text[team].grid(row=7, column=team*4, columnspan=2, sticky='nsew')
            for row in range(3):
                for column in range(2):
                    slot = (row * 2) + column
                    self.team_buttons[team].append(tk.Button(self, image=self.controller.img_blank['inactive'], bd=0.1))
                    self.team_buttons[team][slot].grid(row=row+8, column=(team*4)+column, pady=5)
                    self.team_buttons[team][slot].bind('<Enter>', lambda event, team=team, slot=slot: self.team_on_enter(team, slot))
                    self.team_buttons[team][slot].bind('<Leave>', lambda event, team=team, slot=slot: self.team_on_leave(team, slot))
        self.img_indicator = {'player 1': {}, 'player 2': {}}
        for i in range(1, 3):
            self.img_indicator['player %s' %i]['pick'] = RGBAImage(os.path.join(COMMON, 'p%sp.png' %i))
            self.img_indicator['player %s' %i]['ban'] = RGBAImage(os.path.join(COMMON, 'p%sb.png' %i))
        self.indicator = tk.Label(self)
        self.indicator.bind('<Button-3>', lambda event: self.frame_popup(event))
        self.indicator.grid(row=8, column=2, rowspan=3, columnspan=2, sticky='nsew')
        self.indicator.grid_remove()
        self.finished = RGBAImage(os.path.join(COMMON, 'finished.png'))

    def frame_popup(self, event):
        # popup menu
        self.rclick_menu = tk.Menu(self, tearoff=0)
        self.rclick_menu.add_command(label='New Game', command=self.new_game)
        self.rclick_menu.add_command(label='Reset Game', command=self.reset_game)
        self.rclick_menu.add_command(label='Get Pool', command=lambda: self.export(self.pkmn_pool_list))
        self.rclick_menu.add_command(label='Get Team 1', command=lambda: self.export(self.pkmn_team_list[0]))
        self.rclick_menu.add_command(label='Get Team 2', command=lambda: self.export(self.pkmn_team_list[1]))
        try:
            self.rclick_menu.tk_popup(event.x_root+40, event.y_root+10, 0)
        finally:
            self.rclick_menu.grab_release()

    def button_popup(self, event, pkmn):
        # popup menu
        self.rclick_menu = tk.Menu(self, tearoff=0)
        self.rclick_menu.add_command(label='Export Set', command=lambda pkmn=pkmn: self.export([pkmn]))
        try:
            self.rclick_menu.tk_popup(event.x_root+20, event.y_root+10, 0)
        finally:
            self.rclick_menu.grab_release()

    def reset_game(self):
        self.turn = 0
        self.ban_phase_finished = False
        # reset pool buttons
        for i in range(18):
            self.pkmn_not_picked[i] = True
            self.pool_buttons[i].config(image=self.img_pkmn[i]['inactive' if (self.hidden.get() == 'No') else 'unknown'], command=lambda i=i: self.add(i))
        # reset team and ban buttons
        for i in range(2):
            for j in range(6):
                self.pkmn_team_list[i][j] = None
                self.team_buttons[i][j].config(image=self.controller.img_blank['inactive'], command=lambda: None)
            for j in range(2):
                self.ban_list[i][j] = None
                self.ban_buttons[i][j].config(image=self.controller.img_blank['inactive'], command=lambda: None)

        self.indicator.config(image=self.img_indicator['player 2']['ban'] if (self.ban_number.get() > 0) else self.img_indicator['player 1']['pick'])
        self.controller.sidebar.buttons['Sets'].config(state='disabled')
        self.indicator.grid()

    def new_game(self):
        def filter_pkmn():
            if ((pkmn.name in [i.name for i in temp_list]) or
                (pkmn.tier in temp_excl_tiers) or
                (pkmn.type[0] in temp_excl_types) or
                (pkmn.type[1] and pkmn.type[1] in temp_excl_types) or
                (check_valid_generation(self, pkmn)) or
                (check_valid_item(self, pkmn)) or
                (pkmn.tag in temp_excl_gimmicks)):
                return True
            else:
                return False

        # reset private variables
        self.game_activated = True
        self.draft_num = 8 if (self.draft_mode.get() == 'First Pick') else 6
        self.pkmn_pool_list = []
        self.img_pkmn = {}


        if self.battle_mode.get() == 'SRL':
            # get each player's roster
            list1 = PLAYERS[playerNames.index(self.current_player[0].get())].pkmn_list
            list2 = PLAYERS[playerNames.index(self.current_player[1].get())].pkmn_list
            temp_list = list1 + list2
        else:
            # get all exclusions
            temp_excl_tiers = list(filter(None, [i.get() for i in self.pkmn_excl_tiers_s]))
            temp_excl_types = list(filter(None, [i.get() for i in self.pkmn_excl_types]))
            temp_excl_gimmicks = list(filter(None, [i.get() for i in self.pkmn_excl_gimmicks]))
            # generate a random list based on the rules selected
            temp_list = []
            for pkmn in ALL_POKEMON_S:
                if not filter_pkmn():
                    temp_list.append(pkmn)

        # generate random pool of Pokemon
        index = 0
        while index < 18:
            temp_new_pkmn = random.choice(temp_list)
            if (check_validity(self, temp_new_pkmn)):
                self.pkmn_pool_list.append(temp_new_pkmn)
                # get Pokemon images
                pkmn_name = get_mega_name(self.pkmn_pool_list[index]) if (self.show_megas.get() == 'Yes') else self.pkmn_pool_list[index].name
                self.get_pkmn_imgs(index, pkmn_name)

                # configure the pool buttons
                self.pool_buttons[index].config(image=self.img_pkmn[index]['inactive' if (self.hidden.get() == 'No') else 'unknown'],
                    bd=0.1, command=lambda index=index: self.add(index))
                self.pool_buttons[index].bind('<Enter>', lambda event, button=self.pool_buttons[index], index=index: self.on_enter(button, index))
                self.pool_buttons[index].bind('<Leave>', lambda event, button=self.pool_buttons[index], index=index: self.on_leave(button, index))
                self.pool_buttons[index].bind('<Button-3>', lambda event, pkmn=self.pkmn_pool_list[index]: self.button_popup(event, pkmn))
                index += 1

        self.get_checks()
        self.reset_game()

    def get_pkmn_imgs(self, pool_num, pkmn_name):
        # get filename
        pkmn_filename = pkmn_name.replace('-Small', '').replace('-Large', '').replace('-Super', '').replace(':', '')
        self.img_pkmn[pool_num] = {}
        for i in ['inactive', 'active', 'unknown', 'banned', 'picked']:
            # create images
            img_pkmn_base = RGBAImage2(os.path.join(IMG_PKMN_DIR, pkmn_filename + '_' + i + '.png'))
            create_image(img_pkmn_base, self.controller.img_border[self.draft_mode.get()])
            self.img_pkmn[pool_num][i] = ImageTk.PhotoImage(img_pkmn_base)

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

    def get_team_and_slot(self):
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
        return team_number, slot_number

    def add(self, pool_number):
        if self.game_activated:
            if self.pkmn_not_picked[pool_number]: # the pokemon must be available
                if self.turn < 12:
                    team_number, slot_number = self.get_team_and_slot()
                    # check if the pokemon being added is breaking species clause
                    if self.pkmn_pool_list[pool_number].dex in [i.dex for i in self.pkmn_team_list[team_number] if i is not None]:
                        popup_message(self.controller, 'ERROR', "Sorry, you cannot add %s to Player %s's team" % (self.pkmn_pool_list[pool_number].name, str(team_number+1)), text2="\ndue to the Species Clause.")
                    else:
                        # start adding to teams or ban lists
                        self.pkmn_not_picked[pool_number] = False
                        if self.ban_number.get() != 0 and not self.ban_phase_finished:
                            self.pool_buttons[pool_number].config(image=self.img_pkmn[pool_number]['banned'], command=lambda: None)
                            self.ban(pool_number)
                        else:
                            self.pool_buttons[pool_number].config(image=self.img_pkmn[pool_number]['picked'], command=lambda: None)
                            self.pkmn_team_list[team_number][slot_number] = self.pkmn_pool_list[pool_number]
                            self.team_buttons[team_number][slot_number].config(image=self.img_pkmn[pool_number]['inactive'],
                                command=lambda i=pool_number, j=team_number, k=slot_number: self.remove(i, j, k, self.pkmn_team_list, self.team_buttons))
                        self.update_turns()
                        self.update_turn_indicator()

    def remove(self, pool_number, team_number, slot_number, list, button):
        if self.game_activated:
            # reset variables
            self.pkmn_not_picked[pool_number] = True
            list[team_number][slot_number] = None
            if list == self.ban_list:
                self.ban_phase_finished = False
            self.pool_buttons[pool_number].config(image=self.img_pkmn[pool_number]['inactive' if (self.hidden.get() == 'No') else 'unknown'],
                                                  command=lambda pool_number=pool_number: self.add(pool_number))
            button[team_number][slot_number].config(image=self.controller.img_blank['inactive'], command=lambda: None)
            self.update_turns()
            self.update_turn_indicator()

    def export(self, source):
        if self.game_activated:
            self.controller.clipboard_clear()
            sets = ''
            for pkmn in source:
                if pkmn == None:
                    continue
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
            self.controller.clipboard_append(sets)
            popup_message(self.controller, 'INFO', 'Copied to clipboard.')
        else:
            popup_message(self.controller, 'ERROR', 'No Pokemon to export.')

    def ban(self, pool_number):
        # add Pokemon to proper banlist
        temp_done = False
        for i in range(self.ban_number.get()):
            for j in range(2):
                if not self.ban_list[1-j][i]:
                    self.ban_list[1-j][i] = self.pkmn_pool_list[pool_number]
                    self.ban_buttons[1-j][i].config(image=self.img_pkmn[pool_number]['inactive'],
                        command=lambda pool_number=pool_number, i=i, j=j: self.remove(pool_number, 1-j, i, self.ban_list, self.ban_buttons))
                    temp_done = True
                    break
            if temp_done:
                break

        # end the ban phase
        if (self.ban_number.get() > 0 and self.ban_list[1][0] and
            self.ban_list[0][0] and self.turn < self.draft_num):
            self.ban_phase_finished = True
        if (self.ban_number.get() > 1 and self.ban_list[0][0] and
            self.ban_list[1][0] and self.ban_list[1][1] and self.ban_list[0][1]):
            self.ban_phase_finished = True

    def update_turns(self):
        # check slots to determine current turn
        next_turn = 0
        for i in range(12):
            if (self.draft_mode.get() == 'First Pick'):
                if (not self.pkmn_team_list[self.fp_team_order[i]][self.fp_slot_order[i]]):
                    break
            elif (self.draft_mode.get() == 'Standard'):
                if (not self.pkmn_team_list[int(i%2)][int(i/2)]):
                    break
            elif (self.draft_mode.get() == 'Nemesis'):
                if (not self.pkmn_team_list[int((i+1)%2)][int(i/2)]):
                    break
            next_turn += 1
        self.turn = next_turn

        # reactivate the ban phase if needed
        if (self.ban_number.get() > 1):
            if (not self.ban_list[1][1] or not self.ban_list[0][1]):
                if (self.turn >= self.draft_num):
                    self.ban_phase_finished = False

        # change sets button if game is or is not finished
        self.controller.sidebar.buttons['Sets'].config(state='normal' if (self.turn >= 12) else 'disabled', command=lambda: get_sets(self))

    def update_turn_indicator(self):
        turn = self.fp_team_order[self.turn] if (self.draft_mode.get() == 'First Pick') else (self.turn % 2) + 1
        # configure indicator based on open ban slots
        if self.ban_number.get() > 0 and not self.ban_phase_finished: # there must be a ban phase
            if self.ban_list[1][0]: # team 2 slot 1 is filled
                if self.ban_list[0][0]: # team 1 slot 1 is filled
                    if self.ban_number.get() > 1 and self.turn >= self.draft_num: # second ban phase only
                        if self.ban_list[1][1]: # team 2 slot 2 is filled
                            if self.ban_list[0][1]: # team 1 slot 2 is filled
                                pass # should never reach here
                            else:
                                self.indicator.config(image=self.img_indicator['player 1']['ban'])
                        else:
                            self.indicator.config(image=self.img_indicator['player 2']['ban'])
                    else:
                        self.indicator.config(image=self.img_indicator['player %s' %turn]['pick'])
                else:
                    self.indicator.config(image=self.img_indicator['player 1']['ban'])
            else:
                self.indicator.config(image=self.img_indicator['player 2']['ban'])
        else:
            self.indicator.config(image=self.img_indicator['player %s' %turn]['pick'] if (self.turn < 12) else self.finished)
        self.indicator.grid()

    def on_enter(self, button, index):
        if self.game_activated:
            if self.pkmn_not_picked[index] and self.hidden.get() == 'No':
                button.config(image=self.img_pkmn[index]['active'])
        else:
            if self.pkmn_not_picked[index] and self.hidden.get() == 'No':
                self.pool_buttons[index].config(image=self.controller.img_blank['active'])

    def on_leave(self, button, index):
        if self.game_activated:
            if self.pkmn_not_picked[index] and self.hidden.get() == 'No':
                    button.config(image=self.img_pkmn[index]['inactive'])
        else:
            self.pool_buttons[index].config(image=self.controller.img_blank['inactive'])

    def team_on_enter(self, team, slot):
        if (self.pkmn_team_list[team][slot]):
            pool_num = self.pkmn_pool_list.index(self.pkmn_team_list[team][slot])
            self.team_buttons[team][slot].config(image=self.img_pkmn[pool_num]['active'] if (self.pkmn_team_list[team][slot]) else self.controller.img_blank['active'])
        else:
            self.team_buttons[team][slot].config(image=self.controller.img_blank['active'])

    def team_on_leave(self, team, slot):
        if (self.pkmn_team_list[team][slot]):
            pool_num = self.pkmn_pool_list.index(self.pkmn_team_list[team][slot])
            self.team_buttons[team][slot].config(image=self.img_pkmn[pool_num]['inactive'] if (self.pkmn_team_list[team][slot]) else self.controller.img_blank['inactive'])
        else:
            self.team_buttons[team][slot].config(image=self.controller.img_blank['inactive'])

    def replace_images(self):
        if self.game_activated:
            # clear all images
            self.img_pkmn = {}
            for pkmn in self.pkmn_pool_list:
                # replace all images
                pkmn_name = get_mega_name(pkmn) if (self.show_megas.get() == 'Yes') else pkmn.name
                self.get_pkmn_imgs(self.pkmn_pool_list.index(pkmn), pkmn_name)

            # replace the pool button images
            for index in range(len(self.pkmn_pool_list)):
                if self.pkmn_not_picked[index]:
                    self.pool_buttons[index].config(image=self.img_pkmn[index]['inactive' if (self.hidden.get() == 'No') else 'unknown'])
                else:
                    self.pool_buttons[index].config(image=self.img_pkmn[index]['picked'])

            # replace the ban button images
            for team in range(len(self.ban_list)):
                for slot in range(len(self.ban_list[team])):
                    if self.ban_list[team][slot]:
                        pool_num = self.get_pool_num(self.ban_list[team][slot].name)
                        self.ban_buttons[team][slot].config(image=self.img_pkmn[pool_num]['inactive'])

            # replace the team button images
            for team in range(len(self.pkmn_team_list)):
                for slot in range(len(self.pkmn_team_list[team])):
                    if self.pkmn_team_list[team][slot]:
                        pool_num = self.get_pool_num(self.pkmn_team_list[team][slot].name)
                        self.team_buttons[team][slot].config(image=self.img_pkmn[pool_num]['inactive'])

    def get_pool_num(self, pkmn_name):
        for slot in range(len(self.pkmn_pool_list)):
            if self.pkmn_pool_list[slot].name == pkmn_name:
                return slot


class DraftSettings(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        setup_game_settings(self, 'Draft')

    def update_gen_settings(self):
        # update the player and tier buttons
        mode = self.parent_page().battle_mode.get()
        for button in self.controller.pages['DraftGenerateSettings'].tier_buttons:
            button.config(state='normal' if (mode != 'Doubles') else 'disabled')
        for button in self.controller.pages['DraftGenerateSettings'].tier2_buttons:
            button.config(state='normal' if (mode == 'Doubles') else 'disabled')
        for button in self.player_option:
            button.grid() if (mode == 'SRL') else button.grid_remove()

    def reset_game(self):
        # end the current game
        if self.parent_page().game_activated:
            popup_message(self.controller, 'ERROR', 'Changing this setting has caused the current game to end.', text2='\nPlease start a new game.')
            self.parent_page().game_activated = False

        # clear the ban list and buttons
        for team in range(2):
            for slot in range(len(self.parent_page().ban_buttons[team])):
                self.parent_page().ban_buttons[team][slot].config(image=self.controller.img_blank['inactive'],
                    state='normal' if (slot < self.parent_page().ban_number.get()) else 'disabled', command=lambda: None)
        self.parent_page().ban_list = [[None, None], [None, None]]
        self.parent_page().ban_phase_finished = False
        self.parent_page().ban_text.config(state='normal' if (self.parent_page().ban_number.get()) else 'disabled')

        # clear the pool list and buttons
        for i in range(18):
            self.parent_page().pool_buttons[i].config(image=self.controller.img_blank['inactive'], command=lambda: None)
        self.parent_page().pkmn_pool_list = []
        self.parent_page().pkmn_not_picked = [True for i in range(18)]

        # clear the team lists, buttons, and indicator
        for team in self.parent_page().team_buttons:
            for button in team:
                button.config(image=self.controller.img_blank['inactive'], command=lambda: None)
        self.parent_page().pkmn_team_list = [[None for i in range(6)] for j in range(2)]
        self.parent_page().indicator.grid_remove()

    def parent_page(self):
        return self.controller.pages['Draft']


class DraftGenerateSettings(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        setup_pkmn_settings(self, 'Draft')

    def parent_page(self):
        return self.controller.pages['Draft']


class Random(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        for i in range(3):
            self.grid_rowconfigure(i, weight=1)

        self.init_vars()
        self.init_teams()

    def init_vars(self):
        self.game_activated = False
        # TODO FIXME: replace into a dictionary like in Draft
        self.img_pkmn = [[] for i in range(3)]

        # configure the page layout
        self.frames = []
        for i in range(3):
            self.frames.append(tk.Frame(self))
            self.frames[i].grid(row=i, column=0, sticky='nsew')
        for i in range(3):
            self.frames[1].grid_columnconfigure(i*3, weight=1)

        # page header
        self.img_random = RGBAImage(os.path.join(COMMON, 'label_random.png'))
        self.random_label = tk.Label(self.frames[0], image=self.img_random)
        self.random_label.grid(row=0, column=0, sticky='nsw')

        # game setting variables
        self.pkmn_list = []
        self.battle_mode = tk.StringVar()
        self.battle_mode.set('Singles')
        self.theme = tk.StringVar()
        self.theme.set('Random')
        self.show_megas = tk.StringVar()
        self.show_megas.set('No')
        self.hidden = tk.StringVar()
        self.hidden.set('No')
        self.current_player = [tk.StringVar(), tk.StringVar()]
        for i in range(2):
            self.current_player[i].set('' if (len(playerNames) < 2) else playerNames[i])
        self.type = [tk.StringVar(), tk.StringVar()]
        for i in range(2):
            self.type[i].set(TYPES[0])

        # pokemon settings variables
        self.pkmn_excl_tiers_s = [tk.StringVar() for i in range(len(TIERS_SINGLES))]
        self.pkmn_excl_tiers_d = [tk.StringVar() for i in range(len(TIERS_DOUBLES))]
        self.pkmn_excl_gens = [tk.StringVar() for i in range(len(GENERATIONS))]
        self.pkmn_excl_types = [tk.StringVar() for i in range(len(TYPES))]
        self.pkmn_excl_items = [tk.StringVar() for i in range(len(ITEMS))]
        self.pkmn_excl_gimmicks = [tk.StringVar() for i in range(len(GIMMICKS))]
        self.pkmn_excl_usage = [] # unused

        self.pkmn_team_list = [[None for i in range(6)] for j in range(2)]

    def init_teams(self):
        self.img_team_text = []
        self.team_text = []
        self.team_buttons = [[], []]

        for team in range(2):
            # create section labels
            self.img_team_text.append(RGBAImage(os.path.join(COMMON, 'team%d.png' %int(team+1))))
            self.team_text.append(tk.Label(self.frames[1], image=self.img_team_text[team]))
            self.team_text[team].grid(row=1, column=(team*3)+1, columnspan=2, sticky='nsew')

            # place buttons
            for row in range(3):
                for col in range(2):
                    slot = (row * 2) + col
                    self.team_buttons[team].append(tk.Button(self.frames[1], image=self.controller.img_blank['inactive'], bd=0.1))
                    self.team_buttons[team][slot].grid(row=row+2, column=(team*3)+col+1, padx=10, pady=10)
                    self.team_buttons[team][slot].bind('<Enter>', lambda event, team=team, slot=slot: self.team_on_enter(team, slot))
                    self.team_buttons[team][slot].bind('<Leave>', lambda event, team=team, slot=slot: self.team_on_leave(team, slot))

    def frame_popup(self, event):
        # popup menu
        self.rclick_menu = tk.Menu(self, tearoff=0)
        self.rclick_menu.add_command(label='New Game', command=self.new_game)
        self.rclick_menu.add_command(label='Reset Game', command=self.reset_game)
        self.rclick_menu.add_command(label='Get Team 1', command=lambda: self.export(self.pkmn_team_list[0]))
        self.rclick_menu.add_command(label='Get Team 2', command=lambda: self.export(self.pkmn_team_list[1]))
        try:
            self.rclick_menu.tk_popup(event.x_root+40, event.y_root+10, 0)
        finally:
            self.rclick_menu.grab_release()

    def new_game(self):
        def filter_pkmn():
            if self.theme.get() == 'Monotype':
                incl_type = [self.type[0].get(), self.type[1].get()]
                if ((pkmn.name in [i.name for i in self.pkmn_list]) or
                    (pkmn.tier in temp_excl_tiers) or
                    ((pkmn.type[0] not in incl_type) and
                     (pkmn.type[1] not in incl_type)) or
                    (check_valid_generation(self, pkmn)) or
                    (check_valid_item(self, pkmn)) or
                    (pkmn.tag in temp_excl_gimmicks)):
                    return True
                else:
                    return False
            else:
                if ((pkmn.name in [i.name for i in self.pkmn_list]) or
                    (pkmn.tier in temp_excl_tiers) or
                    (pkmn.type[0] in temp_excl_types) or
                    (pkmn.type[1] and pkmn.type[1] in temp_excl_types) or
                    (check_valid_generation(self, pkmn)) or
                    (check_valid_item(self, pkmn)) or
                    (pkmn.tag in temp_excl_gimmicks)):
                    return True
                else:
                    return False

        # reset private variables
        self.game_activated = True
        self.pkmn_team_list = [[None for i in range(6)] for j in range(2)]
        self.img_pkmn = [[None for i in range(12)] for j in range(3)]

        if self.battle_mode.get() == 'SRL':
            # get each player's roster
            list1 = PLAYERS[playerNames.index(self.current_player[0].get())].pkmn_list
            list2 = PLAYERS[playerNames.index(self.current_player[1].get())].pkmn_list # if self.current_player[1].get() else []
            self.pkmn_list = list1 + list2
        else:
            # get all exclusions
            temp_excl_tiers = list(filter(None, [i.get() for i in self.pkmn_excl_tiers_s]))
            temp_excl_types = list(filter(None, [i.get() for i in self.pkmn_excl_types]))
            temp_excl_gimmicks = list(filter(None, [i.get() for i in self.pkmn_excl_gimmicks]))
            # generate a random list based on the rules selected
            self.pkmn_list = []
            for pkmn in ALL_POKEMON_S:
                if not filter_pkmn():
                    self.pkmn_list.append(pkmn)

        # generate each player's team
        counter = 0
        for i in range(2):
            while counter < 6:
                temp_new_pkmn = random.choice(self.pkmn_list)
                # make team 2 on par with team 1 Pokemon based on tier
                if i == 1 and self.theme.get() == 'Balanced':
                    if ((check_validity(self, temp_new_pkmn, i)) and
                        (temp_new_pkmn.tier == self.pkmn_team_list[0][counter].tier)):
                        self.pkmn_team_list[i][counter] = temp_new_pkmn
                        counter += 1
                # check if the selected Pokemon matches the type
                elif self.theme.get() == 'Monotype':
                    if (check_validity(self, temp_new_pkmn, i) and
                        (self.type[i].get() in temp_new_pkmn.type)):
                        self.pkmn_team_list[i][counter] = temp_new_pkmn
                        counter += 1
                else:
                    if (check_validity(self, temp_new_pkmn, i)):
                        self.pkmn_team_list[i][counter] = temp_new_pkmn
                        counter += 1
            counter = 0

        # configure the team buttons
        for team in range(2):
            for slot in range(6):
                # get Pokemon images
                pkmn_name = get_mega_name(self.pkmn_team_list[team][slot]) if (self.show_megas.get() == 'Yes') else self.pkmn_team_list[team][slot].name
                index = (team * 6) + slot
                self.get_pkmn_imgs(pkmn_name, team, slot)
                self.team_buttons[team][slot].config(
                    image=self.img_pkmn[2 if (self.hidden.get() == 'Yes') else 0][index],
                    command=lambda team=team, slot=slot: self.reroll(team, slot))

        # configure Sets button
        self.controller.sidebar.buttons['Sets'].config(state='normal', command=lambda: get_sets(self))

    def get_pkmn_imgs(self, pkmn_name, team, slot):
        index = (team * 6) + slot
        pkmn_name = pkmn_name.replace('-Small', '').replace('-Large', '').replace('-Super', '').replace(':', '')
        img_pkmn_base = [RGBAImage2(os.path.join(IMG_PKMN_DIR, pkmn_name + '_inactive.png')),
                         RGBAImage2(os.path.join(IMG_PKMN_DIR, pkmn_name + '_active.png')),
                         RGBAImage2(os.path.join(IMG_PKMN_DIR, pkmn_name + '_unknown.png'))]
        for i in range(3):
            create_image(img_pkmn_base[i], self.controller.img_border['Random'])
            self.img_pkmn[i][index] = ImageTk.PhotoImage(img_pkmn_base[i])

    def reroll(self, team, slot):
        index = (team * 6) + slot
        while True:
            # pick a new random Pokemon
            temp_new_pkmn = random.choice(self.pkmn_list)
            if (check_validity(self, temp_new_pkmn, team)):
                self.pkmn_team_list[team][slot] = temp_new_pkmn
                # replace the images
                self.get_pkmn_imgs(self.pkmn_team_list[team][slot].name, team, slot)
                self.team_buttons[team][slot].config(image=self.img_pkmn[0 if self.hidden.get() == 'No' else 2][index])
                break

    def team_on_enter(self, team, x):
        if self.hidden.get() == 'No':
            pool_num = (team * 6) + x
            self.team_buttons[team][x].config(image=self.img_pkmn[1][pool_num] if (self.pkmn_team_list[team][x]) else self.controller.img_blank['active'])

    def team_on_leave(self, team, x):
        if self.hidden.get() == 'No':
            pool_num = (team * 6) + x
            self.team_buttons[team][x].config(image=self.img_pkmn[0][pool_num] if (self.pkmn_team_list[team][x]) else self.controller.img_blank['inactive'])

    def replace_images(self):
        if self.game_activated:
            for team in range(2):
                for slot in range(6):
                    pkmn_name = get_mega_name(self.pkmn_team_list[team][slot]) if (self.show_megas.get() == 'Yes') else self.pkmn_team_list[team][slot].name
                    self.get_pkmn_imgs(pkmn_name, team, slot)
                    index = (team * 6) + slot
                    self.team_buttons[team][slot].config(image=self.img_pkmn[0 if (self.hidden.get() == 'No') else 2][index])


class RandomSettings(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        setup_game_settings(self, 'Random')

    def update_gen_settings(self):
        page = self.controller.pages['RandomGenerateSettings']
        mode = self.parent_page().battle_mode.get()
        theme = self.parent_page().theme.get()
        for button in page.tier_buttons:
            button.config(state='normal' if (mode != 'Doubles') else 'disabled')
        for button in page.tier2_buttons:
            button.config(state='normal' if (mode == 'Doubles') else 'disabled')
        for button in self.player_option:
            button.grid() if (mode == 'SRL') else button.grid_remove()
        for button in self.type_option:
            button.grid() if (theme == 'Monotype') else button.grid_remove()
        for button in page.type_buttons:
            button.config(state='disabled' if (theme == 'Monotype') else 'normal')

    def parent_page(self):
        return self.controller.pages['Random']


class RandomGenerateSettings(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        setup_pkmn_settings(self, 'Random')

    def parent_page(self):
        return self.controller.pages['Random']


class Store(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        for i in range(9):
            self.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.grid_columnconfigure(i, weight=1)


        self.init_vars()
        self.init_banners()
        self.init_canvas()
        self.init_buttons()
        # display the current player's information
        self.switch_player(self.current_player.get())

    def init_vars(self):
        self.banner_num = get_banner_num()
        self.current_player = tk.StringVar()
        self.current_player.set(PLAYERS[0].name)

    def init_banners(self):
        # page variables
        self.current_page = 0
        self.remaining = 44
        # get list of Pokemon in current banners
        self.banner_pkmn_list = [[], []]
        for pkmn in ALL_POKEMON_S:
            if get_mega_name(pkmn) in ALL_BANNERS[self.banner_num]:
                self.banner_pkmn_list[0].append(pkmn)
            if get_mega_name(pkmn) in ALL_BANNERS[self.banner_num+1]:
                self.banner_pkmn_list[1].append(pkmn)

        # banner section
        self.img_banners = []
        self.img_banner_buttons = []
        for i in range(self.banner_num, self.banner_num+2):
            self.img_banners.append(RGBAImage(os.path.join(COMMON, 'banner%s_fit.png' % i)))
            self.img_banner_buttons.append(RGBAImage(os.path.join(COMMON, 'banner%s_button.png' % i)))
        self.banner_image = tk.Label(self)
        self.banner_image.config(image=self.img_banners[0])
        self.banner_image.bind('<Button-3>', lambda event: self.banner_popup(event))
        self.banner_image.grid(row=0, column=0, columnspan=4, sticky='nsew')
        # page button section
        self.page_frame = tk.Frame(self)
        self.page_frame.grid(row=2, column=0, columnspan=4, padx=5, sticky='nsew')
        for i in range(4):
            self.page_frame.grid_columnconfigure(i, weight=1)
        self.page_buttons = []
        self.controller.HelpButton(self, page='Store', row=0, col=2, location=self.page_frame)
        for i in range(2):
            self.page_buttons.append(tk.Button(self.page_frame, image=self.img_banner_buttons[i], bd=0.1, command=lambda i=i: self.change_page(i)))
            self.page_buttons[i].grid(row=0, column=i, padx=5, sticky='nsew')

    def init_canvas(self):
        # create canvas section
        self.scrollframe = tk.LabelFrame(self, text='Available Pokemon')
        self.scrollframe.grid(row=3, column=0, rowspan=5, columnspan=4, padx=5, pady=5, sticky='nsew')
        self.container = tk.Canvas(self.scrollframe, scrollregion=(0, 0, 400, 640))
        self.scrollbar = ttk.Scrollbar(self.scrollframe, orient='vertical', command=self.container.yview)
        self.container.config(yscrollcommand=self.scrollbar.set)
        self.container.bind('<Enter>', self._on_mousewheel)
        self.container.bind('<Leave>', self._off_mousewheel)
        self.scrollbar.pack(side='right', fill='y')
        self.container.pack(side='left', expand=True, fill='both')

        # get Pokemon images
        self.img_pkmn = [[[] for i in range(3)] for j in range(2)]
        self.get_pkmn_imgs()

        # create buttons on canvas
        self.pkmn_buttons = [[None for i in range(5)] for j in range(8)]
        self.pkmn_buttons.append([None for i in range(4)])
        for i in range(9):
            for j in range(len(self.pkmn_buttons[i])):
                x = (i * 5) + j
                self.pkmn_buttons[i][j] = tk.Button(self.container, image=self.img_pkmn[self.current_page][0][x], bd=0.1)
                # place the buttons on the canvas
                self.container.create_window((j*100)+50, (i*70)+30, window=self.pkmn_buttons[i][j])

    def init_buttons(self):
        # display 'current pull' section
        self.pull_result = tk.Label(self, image=self.controller.img_blank['inactive'])
        self.pull_result.grid(row=8, column=0, padx=5, pady=5, sticky='nsew')
        self.player_option = tk.OptionMenu(self, self.current_player, *playerNames, command=self.switch_player)
        self.player_option.config(width=10)
        self.player_option.grid(row=8, column=1, padx=5, pady=5, sticky='ew')

        # pull button
        self.img_pull = []
        for i in ['inactive', 'active']:
            self.img_pull.append(RGBAImage(os.path.join(COMMON, 'button_%s_Pull.png' % i)))
        self.pull_button = tk.Button(self, image=self.img_pull[0], bd=0.1, command=self.pull)
        self.pull_button.grid(row=8, column=2)
        self.pull_button.bind('<Enter>', lambda event: self.on_enter())
        self.pull_button.bind('<Leave>', lambda event: self.on_leave())
        self.remaining_label = tk.Label(self, text='Remaining:\n%d/44' % self.remaining)
        self.remaining_label.grid(row=8, column=3, padx=5, pady=5, sticky='nsew')

    def get_pkmn_imgs(self):
        for i in range(2): # loop over each banner
            for j in range(44): # loop over every Pokemon in each banner
                cur_banner = self.banner_num + i
                pkmn_name = ALL_BANNERS[cur_banner][j].replace('-Small', '').replace('-Large', '').replace('-Super', '').replace(':', '')
                img_pkmn_base = [RGBAImage2(os.path.join(IMG_PKMN_DIR, pkmn_name + '_inactive.png')),
                                 RGBAImage2(os.path.join(IMG_PKMN_DIR, pkmn_name + '_active.png')),
                                 RGBAImage2(os.path.join(IMG_PKMN_DIR, pkmn_name + '_picked.png'))]
                for k in range(3):
                    create_image(img_pkmn_base[k], self.controller.img_border[get_rarity(pkmn_name)])
                    self.img_pkmn[i][k].append(ImageTk.PhotoImage(img_pkmn_base[k]))

    def _on_mousewheel(self, event):
        self.container.bind_all('<MouseWheel>', self._scroll)

    def _off_mousewheel(self, event):
        self.container.unbind_all('<MouseWheel>')

    def _scroll(self, event):
        self.container.yview_scroll(int(-1*(event.delta/120)), 'units')

    def change_week(self):
        self.current_page = 0
        # get list of Pokemon in current banners
        self.banner_pkmn_list = [[], []]
        for pkmn in ALL_POKEMON_S:
            if get_mega_name(pkmn) in ALL_BANNERS[self.banner_num]:
                self.banner_pkmn_list[0].append(pkmn)
            if get_mega_name(pkmn) in ALL_BANNERS[self.banner_num+1]:
                self.banner_pkmn_list[1].append(pkmn)

        # banner section
        self.img_banners = []
        self.img_banner_buttons = []
        for i in range(self.banner_num, self.banner_num+2):
            self.img_banners.append(RGBAImage(os.path.join(COMMON, 'banner%s_fit.png' % i)))
            self.img_banner_buttons.append(RGBAImage(os.path.join(COMMON, 'banner%s_button.png' % i)))
        self.banner_image.config(image=self.img_banners[0])
        for i in range(2):
            self.page_buttons[i].config(image=self.img_banner_buttons[i])

        # get Pokemon images
        self.img_pkmn = [[[] for i in range(3)] for j in range(2)]
        self.get_pkmn_imgs()

        # change all of the page's information
        self.switch_player(self.current_player.get())
        self.pull_result.config(image=self.controller.img_blank['inactive'])
        # if it is an auction, turn off pull button
        self.pull_button.config(state='disabled' if (self.current_page + self.banner_num == 7 or self.current_page + self.banner_num == 15) else 'normal')

    def banner_popup(self, event):
        # popup menu
        self.rclick_menu = tk.Menu(self, tearoff=0)
        self.rclick_menu.add_command(label='Banner Settings', command=lambda: self.controller.change_page('StoreSettings'))
        try:
            self.rclick_menu.tk_popup(event.x_root+50, event.y_root+10, 0)
        finally:
            self.rclick_menu.grab_release()

    def switch_player(self, player):
        # recalculate information based on new current player
        self.current_player.set(player)
        self.remaining = 44
        slot = playerNames.index(player)
        player_pkmn_list = PLAYERS[slot].pkmn_list
        player_pkmn_name_list = [get_mega_name(i) for i in player_pkmn_list]
        cur_banner = self.banner_num + self.current_page

        # configure each button according to the player's list of Pokemon
        for row in range(len(self.pkmn_buttons)):
            for column in range(len(self.pkmn_buttons[row])):
                index = (row * 5) + column
                if ALL_BANNERS[cur_banner][index] in player_pkmn_name_list:
                    self.pkmn_buttons[row][column].config(
                        image=self.img_pkmn[self.current_page][2][index],
                        command=lambda index=index, row=row, column=column: self.remove(index, self.pkmn_buttons[row][column]))
                    self.remaining -= 1
                else:
                    self.pkmn_buttons[row][column].config(
                        image=self.img_pkmn[self.current_page][0][index],
                        command=lambda index=index, row=row, column=column: self.add(index, self.pkmn_buttons[row][column]))
                self.pkmn_buttons[row][column].bind('<Button-3>', lambda event, index=index: self.popup(event, index))

        # update display status
        self.remaining_label.config(text='Remaining:\n%d/44' % self.remaining)

    def pull(self):
        if self.remaining < 1:
            popup_message(self.controller, 'ERROR', 'No Pokemon remaining!')
            return

        # collect player info
        slot = playerNames.index(self.current_player.get())
        player_pkmn_list = PLAYERS[slot].pkmn_list
        player_pkmn_name_list = [get_mega_name(i) for i in player_pkmn_list]
        while True:
            # select a random Pokemon
            temp_new_pkmn = random.choice(self.banner_pkmn_list[self.current_page])
            if get_mega_name(temp_new_pkmn) not in player_pkmn_name_list:
                # add Pokemon to current Player's roster
                PLAYERS[slot].pkmn_list.append(temp_new_pkmn)

                # update canvas buttons and display status
                pkmn_index = ALL_BANNERS[self.banner_num + self.current_page].index(get_mega_name(temp_new_pkmn))
                for row in range(len(self.pkmn_buttons)):
                    for column in range(len(self.pkmn_buttons[row])):
                        index = (row * 5) + column
                        if index == pkmn_index:
                            self.pkmn_buttons[row][column].config(
                                image=self.img_pkmn[self.current_page][2][index],
                                command=lambda index=index: self.remove(index, self.pkmn_buttons[row][column]))
                            self.pull_result.config(image=self.img_pkmn[self.current_page][0][index])
                            self.remaining -= 1
                            self.remaining_label.config(text='Remaining:\n%d/44' % self.remaining)
                            break
                self.update_player_csv()
                break

    def add(self, index, button):
        slot = playerNames.index(self.current_player.get())

        # get all sets for the Pokemon
        temp_pkmn_list = []
        for pkmn in self.banner_pkmn_list[self.current_page]:
            if pkmn.name == strip_mega_name(ALL_BANNERS[self.banner_num + self.current_page][index]):
                temp_pkmn_list.append(pkmn)

        # pick a random set and add it to the current player's roster
        temp_new_pkmn = random.choice(temp_pkmn_list)
        PLAYERS[slot].pkmn_list.append(temp_new_pkmn)

        # update the number of remaining Pokemon display
        self.remaining -= 1
        self.remaining_label.config(text='Remaining:\n%d/44' % self.remaining)

        # modify the selected button
        button.config(image=self.img_pkmn[self.current_page][2][index], command=lambda: self.remove(index, button))
        self.update_player_csv()

    def remove(self, index, button):
        slot = playerNames.index(self.current_player.get())

        # find the Pokemon in the current player's roster and delete it
        for pkmn in PLAYERS[slot].pkmn_list:
            if pkmn.name == strip_mega_name(ALL_BANNERS[self.banner_num + self.current_page][index]):
                del PLAYERS[slot].pkmn_list[PLAYERS[slot].pkmn_list.index(pkmn)]
                break

        # update the number of remaining Pokemon display
        self.remaining += 1
        self.remaining_label.config(text='Remaining:\n%d/44' % self.remaining)

        # modify the selected button
        button.config(image=self.img_pkmn[self.current_page][0][index], command=lambda: self.add(index, button))
        self.update_player_csv()

    def change_page(self, page_num):
        if self.current_page != page_num:
            self.current_page = page_num
            # change all of the page's information
            self.banner_image.config(image=self.img_banners[self.current_page])
            self.switch_player(self.current_player.get())
            # if it is an auction, turn off pull button
            self.pull_button.config(state='disabled' if (self.current_page + self.banner_num == 7 or self.current_page + self.banner_num == 15) else 'normal')

    def popup(self, event, index):
        # popup menu
        pkmn_name = ALL_BANNERS[self.banner_num+self.current_page][index]
        self.rclick_menu = tk.Menu(self, tearoff=0)
        self.rclick_menu.add_command(label='View Sets', command=lambda pkmn_name=pkmn_name: self.view_more_details(pkmn_name))
        try:
            self.rclick_menu.tk_popup(event.x_root+40, event.y_root+10, 0)
        finally:
            self.rclick_menu.grab_release()

    def view_more_details(self, pkmn_name):
        for pkmn in ALL_POKEMON_S:
            if pkmn_name.endswith('-Mega') or pkmn_name.endswith('Mega-Y') or pkmn_name.endswith('Mega-X') or pkmn_name.endswith('-Ash'):
                temp_name = strip_mega_name(pkmn_name)
                if pkmn.item == 'Eviolite':
                    continue
                if pkmn.name == temp_name:
                    if (pkmn.item.endswith('ite') or pkmn.item.endswith('ite X') or pkmn.item.endswith('ite Y') or pkmn.ability == 'Battle Bond'):
                        temp_pkmn = pkmn
                        break
            else:
                temp_name = pkmn_name
                if pkmn.name == temp_name:
                    temp_pkmn = pkmn
                    break
        self.controller.pages['Details'].display_pkmn(temp_pkmn, prev_page='Store')
        self.controller.change_page('Details')

    def on_enter(self):
        if self.pull_button.cget('state') != 'disabled':
            self.pull_button.config(image=self.img_pull[1])

    def on_leave(self):
        if self.pull_button.cget('state') != 'disabled':
            self.pull_button.config(image=self.img_pull[0])

    def update_player_csv(self):
        file = os.path.join(PLAYER_DIR, self.current_player.get() + '.csv')
        with open(file, 'w', encoding='utf-8', newline='') as fileName:
            writer = csv.writer(fileName, delimiter=',')
            writer.writerow([PLAYERS[playerNames.index(self.current_player.get())].portrait])
            for pkmn in PLAYERS[playerNames.index(self.current_player.get())].pkmn_list:
                writer.writerow(
                    [pkmn.name, pkmn.dex, pkmn.type[0], pkmn.type[1],
                     pkmn.tier, pkmn.rarity, pkmn.tag, pkmn.item, pkmn.ability,
                     pkmn.evSpread, pkmn.nature, pkmn.ivSpread,
                     pkmn.moves[0], pkmn.moves[1], pkmn.moves[2], pkmn.moves[3],
                     str(pkmn.generated_draft), str(pkmn.generated_nemesis),
                     str(pkmn.generated_random), str(pkmn.picked_draft),
                     str(pkmn.picked_nemesis), str(pkmn.banned)])


class StoreSettings(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.banner_img = [RGBAImage(os.path.join(COMMON, 'week%s.png' % i)) for i in range(8)]
        self.cur_week = tk.IntVar()
        self.cur_week.set(int(get_banner_num()/2))
        # current banner
        self.banner = tk.Label(self, image=self.banner_img[self.cur_week.get()])
        self.banner.grid(row=0, column=0, columnspan=2, pady=5, sticky='nsew')

        # change weeks
        self.week_frame.grid(row=1, column=0, sticky='nsew')
        self.week_frame.grid_columnconfigure(0, weight=1)
        self.week_label = tk.Label(self.week_frame, text='Change the Current Week')
        self.week_label.grid(row=0, column=0, pady=5, sticky='nsew')
        self.week_buttons = []
        for i in range(8):
            self.week_buttons.append(tk.Radiobutton(
                self.week_frame,
                text='Week #%s' %str(i+1),
                variable=self.cur_week,
                value=i,
                command=self.change_banner_img))
            self.week_buttons[i].grid(row=i+1, column=0, pady=5)
        # change dates of weeks
        self.date_frame.grid(row=1, column=1, sticky='nsew')
        for i in range(4):
            self.date_frame.grid_columnconfigure(i, weight=1)
        self.date_label = tk.Label(self.date_frame, text='Modify Banner Schedule (Format: M/DD)')
        self.date_label.grid(row=0, column=0, pady=5, columnspan=4, sticky='nsew')
        self.start_label = [tk.Label(self.date_frame, text='Week %s Start Date:' %str(i+1)) for i in range(8)]
        self.end_label = [tk.Label(self.date_frame, text='End Date:') for i in range(8)]
        self.entry_box = [[tk.Entry(self.date_frame, width=10) for i in range(8)] for j in range(2)]
        for i in range(8):
            self.start_label[i].grid(row=i+1, column=0, padx=5, pady=7)
            self.end_label[i].grid(row=i+1, column=2, padx=5, pady=7)
        for i in range(2):
            for j in range(8):
                self.entry_box[i][j].grid(row=j+1, column=i*2+1, padx=5, pady=8)
        self.init_dates()

        # save buttons
        self.save_button = []
        self.save_button.append(tk.Button(self.week_frame, text="Change Week", command=self.save))
        self.save_button.append(tk.Button(self.date_frame, text="Save Schedule", state='disabled', width=20, command=self.save_schedule))
        self.save_button[0].grid(row=10, column=0, padx=5, pady=5, sticky='nsew')
        self.save_button[1].grid(row=10, column=0, columnspan=4, padx=5, pady=5)
        # back button
        self.back_button = tk.Button(self, image=self.controller.img_back['inactive'], bd=0.1, command=lambda: self.controller.change_page('Store'))
        self.back_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        self.back_button.bind('<Enter>', lambda event: self.controller.on_enter(self.back_button, self.controller.img_back['active']))
        self.back_button.bind('<Leave>', lambda event: self.controller.on_leave(self.back_button, self.controller.img_back['inactive']))

    def init_dates(self):
        self.entry_box[0][0].insert(0, '6/1')
        self.entry_box[1][0].insert(0, '6/8')
        self.entry_box[0][1].insert(0, '6/9')
        self.entry_box[1][1].insert(0, '6/15')
        self.entry_box[0][2].insert(0, '6/16')
        self.entry_box[1][2].insert(0, '6/22')
        self.entry_box[0][3].insert(0, '6/23')
        self.entry_box[1][3].insert(0, '6/29')
        self.entry_box[0][4].insert(0, '6/30')
        self.entry_box[1][4].insert(0, '7/6')
        self.entry_box[0][5].insert(0, '7/7')
        self.entry_box[1][5].insert(0, '7/13')
        self.entry_box[0][6].insert(0, '7/14')
        self.entry_box[1][6].insert(0, '7/20')
        self.entry_box[0][7].insert(0, '7/21')
        self.entry_box[1][7].insert(0, '7/27')
        for group in self.entry_box:
            for box in group:
                box.config(state='disabled')

    def save(self):
        self.change_week()

    def save_schedule(self):
        pass

    def change_banner_img(self):
        self.banner.config(image=self.banner_img[self.cur_week.get()])

    def change_week(self):
        self.controller.pages['Store'].banner_num = self.cur_week.get() * 2
        self.controller.pages['Store'].change_week()


class Players(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        for i in range(1, 3):
            self.grid_columnconfigure(i, weight=1)
        self.grid_rowconfigure(4, weight=1)

        self.init_vars()
        self.init_canvas()
        self.display_pkmn(self.current_player.get())

    def init_vars(self):
        self.current_player = tk.StringVar()
        self.current_player.set(PLAYERS[0].name)

        # add new player
        self.img_new_player = RGBAImage(os.path.join(COMMON, 'label_new_player.png'))
        self.new_player_label = tk.Label(self, image=self.img_new_player)
        self.new_player_label.grid(row=0, column=0, columnspan=2, sticky='nsw')
        # new player text | entry widget | add button?
        self.name_img = RGBAImage(os.path.join(COMMON, 'label_name.png'))
        self.name_text = tk.Label(self, image=self.name_img, justify='right')
        self.name_text.grid(row=1, column=0, sticky='nse')
        self.enter_name = tk.Entry(self)
        self.enter_name.grid(row=1, column=1, sticky='ew')
        self.add_button = tk.Button(self, text='Get Starter Pokemon', command=self.add_player)
        self.add_button.grid(row=1, column=2, padx=10, sticky='ew')
        # view player inventories
        self.collect_img = RGBAImage(os.path.join(COMMON, 'label_collections.png'))
        self.collect_text = tk.Label(self, image=self.collect_img)
        self.collect_text.grid(row=2, column=0, columnspan=2, pady=(20,10), sticky='nsw')
        # portrait | drop down | get all set details
        self.portrait_img = RGBAImage(os.path.join(TRAINERS, 'trainer_portrait%d.png' %PLAYERS[playerNames.index(self.current_player.get())].portrait))
        self.portrait_button = tk.Button(self, bd=0.1, image=self.portrait_img, command=lambda: self.controller.change_page('Portrait'))
        self.portrait_button.grid(row=3, column=0, padx=5, sticky='nsew')
        self.player_option = tk.OptionMenu(self, self.current_player, *playerNames, command=self.display_pkmn)
        self.player_option.config(width=5)
        self.player_option.grid(row=3, column=1, padx=5, sticky='ew')
        self.get_sets_button = tk.Button(self, text='Export All Sets', command=self.get_all_sets)
        self.get_sets_button.grid(row=3, column=2, padx=10, sticky='ew')

    def init_canvas(self):
        # [grid with pokemon icons]
        self.scrollframe = tk.LabelFrame(self, text='Pokemon Collection (%d Total)' %len(PLAYERS[0].pkmn_list))
        self.scrollframe.grid(row=4, column=0, rowspan=3, columnspan=3, padx=5, pady=5, sticky='nsew')
        self.container = tk.Canvas(self.scrollframe, scrollregion=(0, 0, 400, 1640))
        self.scrollbar = ttk.Scrollbar(self.scrollframe, orient='vertical', command=self.container.yview)
        self.container.config(yscrollcommand=self.scrollbar.set)
        self.container.bind('<Enter>', self._on_mousewheel)
        self.container.bind('<Leave>', self._off_mousewheel)
        self.scrollbar.pack(side='right', fill='y')
        self.container.pack(side='left', expand=True, fill='both')

        # related canvas variables
        self.pkmn_img = [[], []]
        self.pkmn_buttons = []
        self.button_id = []

    def add_player(self):
        player_name = self.enter_name.get().strip()
        # clear entry widget
        self.enter_name.delete(0, 'end')

        # check name validity
        if player_name.lower() in [i.lower() for i in playerNames]:
            popup_message(self.controller,
                          'ERROR',
                          player_name + ' is already in use. Please choose another name.')
        elif player_name and player_name.lower() not in [i.lower() for i in playerNames]:
            # add the player to the player list and dropdown menus
            PLAYERS.append(Player(player_name, random.randint(0, 91), []))
            playerNames.append(player_name)
            update_all_optionmenus(self.controller)

            # change to starter page
            for key, button in self.controller.sidebar.buttons.items():
                button.config(state='disabled')
            self.controller.pages['NewPull'].clear()
            self.controller.change_page('NewPull')
        else:
            pass

    def display_pkmn(self, player_name):
        # set the current player
        self.current_player.set(player_name)
        cur_player = PLAYERS[playerNames.index(self.current_player.get())]
        # update the displayed information
        self.scrollframe.config(text='Pokemon Collection (%d Total)' %len(cur_player.pkmn_list))
        self.portrait_img = RGBAImage(os.path.join(TRAINERS, 'trainer_portrait%d.png' %cur_player.portrait))
        self.portrait_button.config(image=self.portrait_img)

        # clear all buttons and images
        self.pkmn_buttons = []
        if self.button_id:
            for id in self.button_id:
                self.container.delete(id)
        self.button_id = []
        self.pkmn_img = [[], []]

        # reconstruct canvas with new current player's Pokemon
        for i in range(len(cur_player.pkmn_list)):
            # create new buttons with new Pokemon info
            self.get_pkmn_imgs(get_mega_name(cur_player.pkmn_list[i]))
            self.pkmn_buttons.append(tk.Button(self.container, image=self.pkmn_img[0][i], bd=0.1,
                command=lambda i=i: self.get_specific_set(cur_player.pkmn_list[i])))
            self.pkmn_buttons[i].bind('<Enter>', lambda event, i=i: self.on_enter(i))
            self.pkmn_buttons[i].bind('<Leave>', lambda event, i=i: self.on_leave(i))
            self.pkmn_buttons[i].bind('<Button-3>', lambda event, i=i: self.popup(event, i))

            # place new buttons on canvas
            self.button_id.append(self.container.create_window(((i%6)*80)+50, (int(i/6)*70)+30, window=self.pkmn_buttons[i]))

    def popup(self, event, index):
        # popup menu
        pkmn = PLAYERS[playerNames.index(self.current_player.get())].pkmn_list[index]
        self.rclick_menu = tk.Menu(self, tearoff=0)
        self.rclick_menu.add_command(label='View Details', command=lambda pkmn=pkmn: self.view_more_details(pkmn))
        self.rclick_menu.add_command(label='Export Set', command=lambda pkmn=pkmn: self.get_specific_set(pkmn))
        self.rclick_menu.add_command(label='Remove From Team', command=lambda index=index: self.remove(index))
        try:
            self.rclick_menu.tk_popup(event.x_root+60, event.y_root+10, 0)
        finally:
            self.rclick_menu.grab_release()

    def view_more_details(self, pkmn):
        # get Pokemon information
        self.controller.pages['Details'].display_pkmn(pkmn)
        self.controller.change_page('Details')

    def remove(self, index):
        if index < 6:
            popup_message(self.controller, 'ERROR', 'You are not allowed to delete your starter Pokemon.')
            return
        # remove pokemon from list
        del PLAYERS[playerNames.index(self.current_player.get())].pkmn_list[index]
        file = os.path.join(PLAYER_DIR, self.current_player.get() + '.csv')
        with open(file, 'w', encoding='utf-8', newline='') as fileName:
            writer = csv.writer(fileName, delimiter=',')
            writer.writerow([PLAYERS[playerNames.index(self.current_player.get())].portrait])
            for pkmn in PLAYERS[playerNames.index(self.current_player.get())].pkmn_list:
                writer.writerow(
                    [pkmn.name, pkmn.dex, pkmn.type[0], pkmn.type[1],
                     pkmn.tier, pkmn.rarity, pkmn.tag, pkmn.item, pkmn.ability,
                     pkmn.evSpread, pkmn.nature, pkmn.ivSpread,
                     pkmn.moves[0], pkmn.moves[1], pkmn.moves[2], pkmn.moves[3],
                     str(pkmn.generated_draft), str(pkmn.generated_nemesis),
                     str(pkmn.generated_random), str(pkmn.picked_draft),
                     str(pkmn.picked_nemesis), str(pkmn.banned)])
        # redraw canvas
        self.display_pkmn(self.current_player.get())
        # update Store (if needed)
        self.controller.pages['Store'].switch_player(self.current_player.get())

    def get_pkmn_imgs(self, pkmn_name):
        pkmn_name = pkmn_name.replace('-Small', '').replace('-Large', '').replace('-Super', '').replace(':', '')
        img_pkmn_base = [RGBAImage2(os.path.join(IMG_PKMN_DIR, pkmn_name + '_inactive.png')),
                         RGBAImage2(os.path.join(IMG_PKMN_DIR, pkmn_name + '_active.png'))]
        for i in range(2):
            create_image(img_pkmn_base[i], self.controller.img_border[get_rarity(pkmn_name)])
            self.pkmn_img[i].append(ImageTk.PhotoImage(img_pkmn_base[i]))

    def format_sets(self, pkmn):
        sets = ''
        if pkmn.item:
            sets += pkmn.name + ' @ ' + pkmn.item + '\n'
        else:
            sets += pkmn.name + '\n'
        sets += 'Ability: ' + pkmn.ability + '\n'
        sets += 'EVs: ' + pkmn.evSpread + '\n'
        sets += pkmn.nature + ' Nature\n'
        if pkmn.ivSpread:
            sets += 'IVs: ' + pkmn.ivSpread + '\n'
        for move in pkmn.moves:
            if move:
                sets += '- ' + move + '\n'
        return sets

    def get_all_sets(self):
        cur_player = PLAYERS[playerNames.index(self.current_player.get())]
        self.controller.clipboard_clear()
        sets = ''
        for pkmn in cur_player.pkmn_list:
            sets += self.format_sets(pkmn) + '\n'
        self.controller.clipboard_append(sets)
        popup_message(self.controller, 'INFO', "Copied all of %s's Pokemon to clipboard." % cur_player.name)

    def get_specific_set(self, pkmn):
        self.controller.clipboard_clear()
        sets = self.format_sets(pkmn)
        self.controller.clipboard_append(sets)
        popup_message(self.controller, 'INFO', "Copied %s's set to clipboard." % pkmn.name)

    def _on_mousewheel(self, event):
        self.container.bind_all('<MouseWheel>', self._scroll)

    def _off_mousewheel(self, event):
        self.container.unbind_all('<MouseWheel>')

    def _scroll(self, event):
        self.container.yview_scroll(int(-1*(event.delta/120)), 'units')

    def on_enter(self, slot):
        self.pkmn_buttons[slot].config(image=self.pkmn_img[1][slot])

    def on_leave(self, slot):
        self.pkmn_buttons[slot].config(image=self.pkmn_img[0][slot])


class NewPull(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        for i in [0, 1, 3]:
            self.grid_rowconfigure(i, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.init_boxes()
        self.init_pulls()

    def init_boxes(self):
        self.box_buttons = [[], []]
        self.box_images = [[], []]
        for i in ['A', 'B', 'C', 'D']:
            self.box_images[0].append(RGBAImage(os.path.join(COMMON, 'button_inactive_Mystery%s.png' %i)))
            self.box_images[1].append(RGBAImage(os.path.join(COMMON, 'button_active_Mystery%s.png' %i)))

    def init_pulls(self):
        self.pkmn_list = []
        self.img_pkmn = [[], []]
        self.pkmn_buttons = []

        self.frames = []
        for i in range(4):
            self.frames.append(tk.Frame(self))
            self.frames[i].grid(row=i, column=0, sticky='nsew')
        for i in [0, 4, 5, 6]:
            self.frames[1].grid_columnconfigure(i, weight=1)
        for i in range(2):
            self.frames[0].grid_columnconfigure(i, weight=1)
            self.frames[3].grid_rowconfigure(i, weight=1)
            self.frames[3].grid_columnconfigure(i, weight=1)

        self.newimg_pull = RGBAImage(os.path.join(COMMON, 'label_newpull.png'))
        self.newpull_label = tk.Label(self.frames[0], image=self.newimg_pull)
        self.newpull_label.grid(row=0, column=0, sticky='nsw')
        self.controller.HelpButton(self, page='NewPull', row=0, col=1, location=self.frames[0])

        for row in range(2):
            for column in range(3):
                x = (row * 3) + column
                self.pkmn_buttons.append(tk.Button(self.frames[1], image=self.controller.img_blank['inactive'], bd=0.1))
                self.pkmn_buttons[x].grid(row=row, column=column+1, padx=10, pady=10)
                self.pkmn_buttons[x].bind('<Enter>', lambda event, x=x: self.team_on_enter(x))
                self.pkmn_buttons[x].bind('<Leave>', lambda event, x=x: self.team_on_leave(x))

        self.img_done = []
        self.button_states = ['inactive', 'active']
        for i in range(2):
            self.img_done.append(RGBAImage(os.path.join(COMMON, 'button_' + self.button_states[i] + '_finishpull.png')))
        self.back_button = tk.Button(self.frames[1], image=self.img_done[0], bd=0.1, state='disabled', command=self.back)
        self.back_button.grid(row=0, column=5, rowspan=2, sticky="nsew")
        self.box_img = RGBAImage(os.path.join(COMMON, 'label_box.png'))
        self.box_label = tk.Label(self.frames[2], image=self.box_img)
        self.box_label.grid(row=0, column=0, sticky='nsw')
        for i in range(4):
            self.box_buttons[int(i/2)].append(tk.Button(self.frames[3], image=self.box_images[0][i], bd=0.1, command=lambda i=i: self.pullbox(i)))
            self.box_buttons[int(i/2)][i%2].grid(row=int(i/2), column=i%2)
            self.box_buttons[int(i/2)][i%2].bind('<Enter>', lambda event, i=i: self.box_on_enter(i))
            self.box_buttons[int(i/2)][i%2].bind('<Leave>', lambda event, i=i: self.box_on_leave(i))

        self.box_list = [[] for i in range(4)]
        for pkmn in ALL_POKEMON_S:
            if (pkmn.tier == 'NFE' or pkmn.tier == 'Untiered' or
                pkmn.tier == 'PU' or pkmn.tier == 'NU'):
                if ('Bug' in pkmn.type or 'Electric' in pkmn.type or
                    'Flying' in pkmn.type or 'Ice' in pkmn.type):
                    self.box_list[0].append(pkmn)
                if ('Fire' in pkmn.type or 'Poison' in pkmn.type or
                    'Water' in pkmn.type or 'Ground' in pkmn.type):
                    self.box_list[1].append(pkmn)
                if ('Grass' in pkmn.type or 'Rock' in pkmn.type or
                    'Psychic' in pkmn.type or 'Dark' in pkmn.type):
                    self.box_list[2].append(pkmn)
                if ('Steel' in pkmn.type or 'Ghost' in pkmn.type or
                    'Fighting' in pkmn.type or 'Normal' in pkmn.type):
                    self.box_list[3].append(pkmn)


    def get_pkmn_imgs(self, pkmn_name):
        pkmn_name = pkmn_name.replace('-Small', '').replace('-Large', '').replace('-Super', '').replace(':', '')
        img_pkmn_base = [RGBAImage2(os.path.join(IMG_PKMN_DIR, pkmn_name + '_inactive.png')),
                              RGBAImage2(os.path.join(IMG_PKMN_DIR, pkmn_name + '_active.png'))]
        for i in range(2):
            create_image(img_pkmn_base[i], self.controller.img_border[get_rarity(pkmn_name)])
            self.img_pkmn[i].append(ImageTk.PhotoImage(img_pkmn_base[i]))

    def pullbox(self, boxnum):
        self.pkmn_list = []
        self.img_pkmn = [[], []]
        counter = 0
        while counter < 6:
            if counter < 4:
                box = boxnum
            else:
                box = random.choice([0, 1, 2, 3])
            temp_new_pkmn = random.choice(self.box_list[box])
            if temp_new_pkmn not in self.pkmn_list:
                if get_mega_name(temp_new_pkmn) not in [get_mega_name(i) for i in self.pkmn_list]:
                    self.get_pkmn_imgs(get_mega_name(temp_new_pkmn))
                    self.pkmn_list.append(temp_new_pkmn)
                    counter += 1
        for i in range(2):
            for j in range(2):
                self.box_buttons[i][j].config(state='disabled')
        for i in range(6):
            self.pkmn_buttons[i].config(image=self.img_pkmn[0][i],
                command=lambda i=i: self.reroll(i))
        self.back_button.config(image=self.img_done[1], state='normal')

    def reroll(self, slot):
        self.pkmn_list[slot] = None
        while True:
            box = random.choice([0, 1, 2, 3])
            temp_new_pkmn = random.choice(self.box_list[box])
            if get_mega_name(temp_new_pkmn) not in [get_mega_name(i) for i in self.pkmn_list if i is not None]:
                self.pkmn_list[slot] = temp_new_pkmn
                name = get_mega_name(temp_new_pkmn)
                name = name.replace('-Small', '').replace('-Large', '').replace('-Super', '').replace(':', '')
                self.img_pkmn_base = [RGBAImage2(os.path.join(IMG_PKMN_DIR, name + '_inactive.png')),
                                      RGBAImage2(os.path.join(IMG_PKMN_DIR, name + '_active.png'))]
                for i in range(2):
                    create_image(self.img_pkmn_base[i], self.controller.img_border[get_rarity(name)])
                    self.img_pkmn[i][slot] = ImageTk.PhotoImage(self.img_pkmn_base[i])
                break
        self.pkmn_buttons[slot].config(image=self.img_pkmn[1][slot])

    def clear(self):
        self.pkmn_list = []
        for i in range(6):
            self.img_pkmn = []
            self.pkmn_buttons[i].config(image=self.controller.img_blank['inactive'], command=lambda: None)
        for i in range(2):
            for j in range(2):
                self.box_buttons[i][j].config(state='normal')
        self.back_button.config(image=self.img_done[0], state='disabled')

    def back(self):
        PLAYERS[-1].pkmn_list = self.pkmn_list
        filename = PLAYERS[-1].name + '.csv'
        with open(os.path.join(PLAYER_DIR, filename), 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow([PLAYERS[-1].portrait])
            for pkmn in PLAYERS[-1].pkmn_list:
                writer.writerow(
                    [pkmn.name, pkmn.dex, pkmn.type[0], pkmn.type[1],
                     pkmn.tier, pkmn.rarity, pkmn.tag, pkmn.item, pkmn.ability,
                     pkmn.evSpread, pkmn.nature, pkmn.ivSpread,
                     pkmn.moves[0], pkmn.moves[1], pkmn.moves[2], pkmn.moves[3],
                     str(pkmn.generated_draft), str(pkmn.generated_nemesis),
                     str(pkmn.generated_random), str(pkmn.picked_draft),
                     str(pkmn.picked_nemesis), str(pkmn.banned)])

        update_all_optionmenus(self.controller)
        for key, button in self.controller.sidebar.buttons.items():
            button.config(state='normal')
        self.controller.pages['Players'].display_pkmn(PLAYERS[-1].name)
        self.controller.change_page('Players')

    def team_on_enter(self, slot):
        if not self.pkmn_list:
            self.pkmn_buttons[slot].config(image=self.controller.img_blank['active'])
        else:
            self.pkmn_buttons[slot].config(image=self.img_pkmn[1][slot])

    def team_on_leave(self, slot):
        if not self.pkmn_list:
            self.pkmn_buttons[slot].config(image=self.controller.img_blank['inactive'])
        else:
            self.pkmn_buttons[slot].config(image=self.img_pkmn[0][slot])

    def box_on_enter(self, boxnum):
        if self.box_buttons[int(boxnum/2)][boxnum%2].cget('state') != 'disabled':
            self.box_buttons[int(boxnum/2)][boxnum%2].config(image=self.box_images[1][boxnum])

    def box_on_leave(self, boxnum):
        self.box_buttons[int(boxnum/2)][boxnum%2].config(image=self.box_images[0][boxnum])


class Details(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # fix the rows with the sets
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # create each frame/row
        self.frames = []
        for i in range(5):
            self.frames.append(tk.Frame(self))
            self.frames[i].grid(row=i, column=0, sticky='nsew')

        # general information stuff and banner image
        self.font = Font(size=16, weight='bold')
        self.banner_txt = tk.Label(self.frames[0], text='Appears in:', font=self.font)
        self.banner_txt.grid(row=0, column=0, sticky='nsew')
        self.banner = tk.Label(self.frames[1])
        self.banner.grid(row=0, column=0, sticky='nsew')
        self.detail_header = tk.Label(self.frames[2], text='All Possible Sets (Singles):', font=self.font)
        self.detail_header.grid(row=0, column=0, sticky='nsew')
        self.set_details = []

        # back button
        self.back_button = tk.Button(self, image=self.controller.img_back['inactive'], bd=0.1, command=lambda: self.controller.change_page('Players'))
        self.back_button.grid(row=5, column=0, padx=5, pady=5)
        self.back_button.bind('<Enter>', lambda event: self.controller.on_enter(self.back_button, self.controller.img_back['active']))
        self.back_button.bind('<Leave>', lambda event: self.controller.on_leave(self.back_button, self.controller.img_back['inactive']))

    def display_pkmn(self, pkmn, prev_page='Players'):
        # get all similar Pokemon
        temp_list = [i for i in ALL_POKEMON_S if i.name == pkmn.name]
        pkmn_list = [i for i in temp_list if i.item == pkmn.item] if (is_mega(pkmn)) else temp_list
        pkmn_name = get_mega_name(pkmn)

        # determine banner number
        banner_num = -1
        for banner in range(len(ALL_BANNERS)):
            if pkmn_name in ALL_BANNERS[banner]:
                banner_num = banner if (banner <= get_banner_num() + 1) else -1
                break
        self.banner_img = RGBAImage(os.path.join(COMMON, 'banner%s_fit.png' % banner_num))
        self.banner.config(image=self.banner_img)

        # get details of all sets
        for widget in self.set_details:
            widget.grid_forget()
        self.set_details = []
        for i in range(len(pkmn_list)):
            sets = ''
            if pkmn_list[i].item:
                sets += pkmn_list[i].name + ' @ ' + pkmn_list[i].item + '\n'
            else:
                sets += pkmn_list[i].name + '\n'
            sets += 'Ability: ' + pkmn_list[i].ability + '\n'
            sets += 'EVs: ' + pkmn_list[i].evSpread + '\n'
            sets += pkmn_list[i].nature + ' Nature\n'
            if pkmn_list[i].ivSpread:
                sets += 'IVs: ' + pkmn_list[i].ivSpread + '\n'
            for move in pkmn_list[i].moves:
                if move:
                    sets += '- ' + move + '\n'
            if not pkmn_list[i].ivSpread:
                sets += '\n'
            # place formatted set information
            self.set_details.append(tk.Label(self.frames[3 if (int(i/3) == 0) else 4], text=sets, justify='left'))
            if prev_page == 'Players':
                self.set_details[i].config(fg='red' if self.is_current_set(pkmn, pkmn_list[i]) else 'black')
            self.set_details[i].grid(row=0, column=i, padx=5, pady=5, sticky='nsew')
            self.set_details[i].bind('<Button-3>', lambda event, sets=sets: self.popup(event, sets))

        self.back_button.config(command=lambda prev_page=prev_page: self.controller.change_page(prev_page))

    def popup(self, event, sets):
        # popup menu
        self.rclick_menu = tk.Menu(self, tearoff=0)
        self.rclick_menu.add_command(label='Export Set', command=lambda sets=sets: self.export(sets))
        try:
            self.rclick_menu.tk_popup(event.x_root+30, event.y_root+10, 0)
        finally:
            self.rclick_menu.grab_release()

    def export(self, sets):
        self.controller.clipboard_clear()
        self.controller.clipboard_append(sets)
        popup_message(self.controller, 'INFO', "Copied to clipboard.")

    def is_current_set(self, pkmn1, pkmn2):
        if ((pkmn1.name != pkmn2.name) or
            ((pkmn1.item and pkmn2.item) and (pkmn1.item != pkmn2.item)) or
            (pkmn1.ability != pkmn2.ability) or
            (pkmn1.evSpread != pkmn2.evSpread) or
            (pkmn1.nature != pkmn2.nature)):
            return False
        if pkmn1.ivSpread and pkmn2.ivSpread:
            if pkmn1.ivSpread != pkmn2.ivSpread:
                return False
        if (((pkmn1.moves[0] and pkmn2.moves[0]) and (pkmn1.moves[0] != pkmn2.moves[0])) or
            ((pkmn1.moves[1] and pkmn2.moves[1]) and (pkmn1.moves[1] != pkmn2.moves[1])) or
            ((pkmn1.moves[2] and pkmn2.moves[2]) and (pkmn1.moves[2] != pkmn2.moves[2])) or
            ((pkmn1.moves[3] and pkmn2.moves[3]) and (pkmn1.moves[3] != pkmn2.moves[3]))):
            return False
        return True


class StoreHelpPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # create canvas
        self.scrollframe = tk.Frame(self)
        self.scrollframe.grid(row=0, column=0, sticky='nsew')
        self.container = tk.Canvas(self.scrollframe, scrollregion=(0, 0, 400, 1200))
        self.scrollbar = ttk.Scrollbar(self.scrollframe, orient='vertical', command=self.container.yview)
        self.container.config(yscrollcommand=self.scrollbar.set)
        self.container.bind('<Enter>', self._on_mousewheel)
        self.container.bind('<Leave>', self._off_mousewheel)
        self.scrollbar.pack(side='right', fill='y')
        self.container.pack(side='left', expand=True, fill='both')

        # create help image
        self.img_help = RGBAImage(os.path.join(COMMON, 'help_store.png'))
        self.help = tk.Label(self.container, image=self.img_help)
        self.container.create_window(255, 590, window=self.help)

        # back button
        self.back_button = tk.Button(self, image=self.controller.img_back['inactive'], bd=0.1, command=lambda: self.controller.change_page('Store'))
        self.back_button.grid(row=1, column=0, padx=5, pady=5)
        self.back_button.bind('<Enter>', lambda event: self.controller.on_enter(self.back_button, self.controller.img_back['active']))
        self.back_button.bind('<Leave>', lambda event: self.controller.on_leave(self.back_button, self.controller.img_back['inactive']))

    def _on_mousewheel(self, event):
        self.container.bind_all('<MouseWheel>', self._scroll)

    def _off_mousewheel(self, event):
        self.container.unbind_all('<MouseWheel>')

    def _scroll(self, event):
        self.container.yview_scroll(int(-1*(event.delta/120)), 'units')


class NewPullHelpPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # create help image
        self.img_help = RGBAImage(os.path.join(COMMON, 'help_starter.png'))
        self.help_label = tk.Label(self, image=self.img_help)
        self.help_label.grid(row=0, column=0, sticky='nsew')

        # back button
        self.back_button = tk.Button(self, image=self.controller.img_back['inactive'], bd=0.1, command=lambda: self.controller.change_page('NewPull'))
        self.back_button.grid(row=1, column=0, padx=5, pady=5)
        self.back_button.bind('<Enter>', lambda event: self.controller.on_enter(self.back_button, self.controller.img_back['active']))
        self.back_button.bind('<Leave>', lambda event: self.controller.on_leave(self.back_button, self.controller.img_back['inactive']))


class Portrait(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.init_canvas()

    def init_canvas(self):
        # create canvas
        self.scrollframe = tk.Frame(self)
        self.scrollframe.grid(row=0, column=0, sticky='nsew')
        self.container = tk.Canvas(self.scrollframe, scrollregion=(0, 0, 400, 5430))
        self.scrollbar = ttk.Scrollbar(self.scrollframe, orient='vertical', command=self.container.yview)
        self.container.config(yscrollcommand=self.scrollbar.set)
        self.container.bind('<Enter>', self._on_mousewheel)
        self.container.bind('<Leave>', self._off_mousewheel)
        self.scrollbar.pack(side='right', fill='y')
        self.container.pack(side='left', expand=True, fill='both')

        # get the current player
        cur_player = PLAYERS[playerNames.index(self.controller.pages['Players'].current_player.get())]
        self.cur_portrait = tk.IntVar()
        self.cur_portrait.set(cur_player.portrait)

        self.portrait_buttons = []
        self.button_id = []
        self.portrait_img = []

        # construct canvas
        for i in range(92):
            # create buttons
            self.portrait_img.append(RGBAImage(os.path.join(TRAINERS, 'trainer_portrait%d.png' %i)))
            self.portrait_buttons.append(tk.Radiobutton(
                self.container,
                image=self.portrait_img[i], bd=0.1,
                variable=self.cur_portrait,
                value=i,
                indicatoron=0,
                command=self.change_portrait))
            # place buttons on canvas
            self.button_id.append(self.container.create_window(((i%3)*175)+90, (int(i/3)*175)+90, window=self.portrait_buttons[i]))

    def _on_mousewheel(self, event):
        self.container.bind_all('<MouseWheel>', self._scroll)

    def _off_mousewheel(self, event):
        self.container.unbind_all('<MouseWheel>')

    def _scroll(self, event):
        self.container.yview_scroll(int(-1*(event.delta/120)), 'units')

    def change_portrait(self):
        # overwrite and save player's portrait value
        PLAYERS[playerNames.index(self.controller.pages['Players'].current_player.get())].portrait = self.cur_portrait.get()
        file = os.path.join(PLAYER_DIR, PLAYERS[playerNames.index(self.controller.pages['Players'].current_player.get())].name + '.csv')
        with open(file, 'w', encoding='utf-8', newline='') as fileName:
            writer = csv.writer(fileName, delimiter=',')
            writer.writerow([PLAYERS[playerNames.index(self.controller.pages['Players'].current_player.get())].portrait])
            for pkmn in PLAYERS[playerNames.index(self.controller.pages['Players'].current_player.get())].pkmn_list:
                writer.writerow(
                    [pkmn.name, pkmn.dex, pkmn.type[0], pkmn.type[1],
                     pkmn.tier, pkmn.rarity, pkmn.tag, pkmn.item, pkmn.ability,
                     pkmn.evSpread, pkmn.nature, pkmn.ivSpread,
                     pkmn.moves[0], pkmn.moves[1], pkmn.moves[2], pkmn.moves[3],
                     str(pkmn.generated_draft), str(pkmn.generated_nemesis),
                     str(pkmn.generated_random), str(pkmn.picked_draft),
                     str(pkmn.picked_nemesis), str(pkmn.banned)])
        # update and show the Players page
        self.controller.pages['Players'].display_pkmn(PLAYERS[playerNames.index(self.controller.pages['Players'].current_player.get())].name)
        self.controller.change_page('Players')

################################################################################
# global helper functions
################################################################################
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


def RGBAImage(path):
    return ImageTk.PhotoImage(Image.open(path).convert('RGBA'))


def RGBAImage2(path):
    return Image.open(path).convert('RGBA')


def init_player_information():
    # create player directory
    if not os.path.isdir(PLAYER_DIR):
        os.mkdir(PLAYER_DIR)
    if not os.listdir(PLAYER_DIR):
        with open(os.path.join(PLAYER_DIR, 'Virgo.csv'), 'w', encoding='utf-8', newline='') as file:
            pass
    # get Pokemon information
    for filename in os.listdir(PLAYER_DIR):
        if filename.endswith('.csv'):
            with open(os.path.join(PLAYER_DIR, filename), 'r', encoding='utf-8') as file:
                player_name = os.path.splitext(os.path.basename(file.name))[0]
                reader = csv.reader(file)
                # get trainer portrait info
                portrait = int(next(reader)[0]) if os.stat(os.path.join(PLAYER_DIR, filename)).st_size != 0 else random.randint(0, 91)
                temp_pkmn_list = []
                for row in reader:
                    if row:
                        temp_pkmn_list.append(Pokemon(row))
                PLAYERS.append(Player(player_name, portrait, temp_pkmn_list))
                playerNames.append(player_name)


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


def create_image(base_image, image):
    base_image.paste(image, (0, 0), image)


class Player:
    def __init__(self, name, portrait, pkmn_list):
        self.name = name
        self.portrait = portrait
        self.pkmn_list = pkmn_list


if __name__ == '__main__':
    # global variables
    VERSION = '2.8.0'
    ROOT = os.path.dirname(os.path.realpath(__file__))
    COMMON = os.path.join(ROOT, 'media', 'Common')
    TRAINERS = os.path.join(ROOT, 'media', 'trainers')
    IMG_PKMN_DIR = os.path.join(ROOT, 'media', 'pokemon')
    PLAYER_DIR = os.path.join(ROOT, 'players')
    DATA = os.path.join(ROOT, 'data')
    month = int(date.today().strftime('%m'))
    day = int(date.today().strftime('%d'))

    # before starting the GUI, gather player information
    init_player_information()
    app = MainApp()

    # disable resizing of window
    app.resizable(False, False)

    # set the title of the windows
    app.title('Rentals v%s' %VERSION)
    app.mainloop()
