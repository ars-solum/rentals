"""
main.py
Purpose : Creates an interactive GUI for the Pokemon Rentals Database and
          related streaming activities.

Author  : Ars Solum
Version : 2.2.0
"""

################################################################################
# system includes                                                              #
################################################################################
import csv
from datetime import date
import os
from PIL import Image, ImageTk
import random
from random import shuffle
import tkinter as tk
from tkinter import ttk

################################################################################
# local includes                                                               #
################################################################################
from Pokemon import *

class MainApp(tk.Tk):

    """function : __init__
    purpose     : Initializes the GUI's base window and its components.
    @param[in]  : *args Any required Tk arguments.
    @param[in]  : **kwargs Any optional Tk arguments.
    @return     : None.
    """
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # initialize everything
        self.init_vars()
        self.init_side_menu()
        self.init_main_menu()

        self.show_frame('Draft')

    """function : init_vars
    purpose     : Initializes MainApp's private and pseudo-global variables.
    @param[in]  : self An instance of MainApp [Tk].
    @return     : None.
    """
    def init_vars(self):
        # TODO FIXME: Move these image-related variables to a global space
        #             and potentially refactor by making one large nested
        #             dictionary.
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
            self.img_blank_base[key].paste(self.img_border['Standard'],
                                           (0, 0),
                                           self.img_border['Standard'])

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

    """function : init_side_menu
    purpose     : Initializes the sidebar menu and its components for the GUI.
    @param[in]  : self An instance of MainApp [Tk].
    @return     : None.
    """
    def init_side_menu(self):
        self.frame_side_menu = tk.Frame(self)
        self.frame_side_menu.grid(row=0, column=0, sticky='nsew')

        # Allot a 1x1 space for the Sidemenu
        self.frame_side_menu.grid_rowconfigure(0, weight=1)
        self.frame_side_menu.grid_columnconfigure(0, weight=1)

        self.sidebar = Sidebar(parent=self.frame_side_menu, controller=self)
        self.sidebar.grid(row=0, column=0, sticky='nsew')

    """function : init_main_menu
    purpose     : Initializes the main frame and its components for the GUI.
    @param[in]  : self An instance of MainApp [Tk].
    @return     : None.
    """
    def init_main_menu(self):
        self.main_frame = tk.Frame(self)
        self.main_frame.grid(row=0, column=1, sticky='nsew')

        # Allot a 1x1 space for the contents of the main space
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.pages = {}

        # TODO FIXME: refactor the page creation process
        for page in (Draft, Random, DraftSettings, DraftGenerateSettings,
                      RandomSettings, RandomGenerateSettings, Store, Players,
                      DraftHelpPage, StoreHelpPage, PullHelpPage, NewPull):
            page_name = page.__name__
            frame = page(parent=self.main_frame, controller=self)
            self.pages[page_name] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        # modify the start button
        self.sidebar.buttons['Game'].config(command=self.pages['Draft'].new_game)

    """function : show_frame
    purpose     : Changes the current page based on the button clicked.  The
                  function will also check the state of each page and modify
                  the sidebar's buttons accordingly.
    @param[in]  : self An instance of MainApp [Tk].
    @param[in]  : page_name The name of the page to switch to [string].
    @return     : None.
    """
    def show_frame(self, page_name):
        if (page_name == 'Store' and
            len(PLAYERS) == 1 and
            len(PLAYERS[0].pkmn_list) == 0):
            popup_message(self, 'ERROR', 'You cannot visit the store right now.',
                          text2='\nPlease roll for your first team.')
        elif (page_name == 'Players' and len(PLAYERS) == 1 and
              len(PLAYERS[0].pkmn_list) == 0):
            popup_message(self, 'INFO', "Welcome Virgo! Let's get your starter Pokemon!")

            # disable all sidebar buttons
            for key, button in self.sidebar.buttons.items():
                button.config(state='disabled')

            frame = self.pages['NewPull']
            frame.tkraise()
        else:
            if (page_name == 'Draft' or page_name == 'Random'):
                for key, button in self.sidebar.buttons.items():
                    button.config(state='normal')
                    button.grid()
                # check if game is actually finished
                if (self.pages[page_name].game_activated == False or
                    (hasattr(self.pages[page_name], 'turn') and
                     self.pages[page_name].turn < 12)):
                    self.sidebar.buttons['Sets'].config(state='disabled')
                self.sidebar.buttons['game_settings'].config(command=lambda:self.show_frame('%sSettings' % page_name))
                self.sidebar.buttons['pkmn_settings'].config(command=lambda:self.show_frame('%sGenerateSettings' % page_name))
                self.sidebar.buttons['Game'].config(command=self.pages[page_name].new_game)
            else:
                if ('Settings' in page_name or 'Help' in page_name or 'NewPull' in page_name):
                    # disable page-related buttons
                    for key, button in self.sidebar.buttons.items():
                        button.config(state='disabled')
                else:
                    # enable page-related buttons
                    for key, button in self.sidebar.buttons.items():
                        button.config(state='normal')
            if page_name == 'Players':
                # get the current player's pokemon information and display it
                self.pages[page_name].display_pkmn(self.pages[page_name].current_player.get())

            # change the page
            frame = self.pages[page_name]
            frame.tkraise()


    def on_enter(self, button, type):
        if type == 'help':
            button.config(image=self.img_help['active'])
        if type == 'back':
            button.config(image=self.img_back['active'])
        if type == 'blank':
            button.config(image=self.img_blank['active'])

    def on_leave(self, button, type):
        if type == 'help':
            button.config(image=self.img_help['inactive'])
        if type == 'back':
            button.config(image=self.img_back['inactive'])
        if type == 'blank':
            button.config(image=self.img_blank['inactive'])

    def HelpButton(self, source, page, row, col, location=''):
        if not location:
            location = source
        source.help_button = tk.Button(location, image=self.img_help['inactive'],
            bd=0.1, command=lambda: self.show_frame('%sHelpPage' % page))
        source.help_button.grid(row=row, column=col)
        source.help_button.bind('<Enter>', lambda event: self.on_enter(source.help_button, 'help'))
        source.help_button.bind('<Leave>', lambda event: self.on_leave(source.help_button, 'help'))

class Sidebar(tk.Frame):

    """function : __init__
    purpose     : Initializes the GUI's sidebar and its components.
    @param[in]  : self An instance of the Sidebar object [tk.Frame].
    @param[in]  : parent The object type to instantiate [tk.Frame].
    @param[in]  : controller The owner of Sidebar [MainApp].
    @return     : None.
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller # MainApp

        # Allot a 4x1 space for Sidebar's contents
        for i in range(4):
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

        # initialize section label images
        for section in self.text:
            self.img_labels[section] = RGBAImage(os.path.join(COMMON, '%s.png' %section))

        # initialize button images
        for section in self.text:
            for item in self.text[section]:
                self.img_buttons[item] = {}
        for key in self.img_buttons:
            for state in ['active', 'inactive']:
                self.img_buttons[key][state] = RGBAImage(os.path.join(COMMON, 'button_%s_%s.png' % (state, key)))

        self.empty_space = RGBAImage(os.path.join(COMMON, '2_empty_buttons.png'))

        tmp_ctr = 0 # keep track of which row to place the current section
        # construct each section
        for section in self.text:
            # special case: 3rd section should be empty for now
            if tmp_ctr == 2:
                self.empty_space_label = tk.Label(self, image=self.empty_space)
                self.empty_space_label.grid(row=tmp_ctr, column=0, sticky='nsew')
                tmp_ctr += 1 # now onto 4th section

            # initialize section frames
            self.frame_section[section] = tk.Frame(self)
            self.frame_section[section].grid(row=tmp_ctr, column=0, sticky='nsew')

            # initialize section labels
            self.label_section[section] = tk.Label(self.frame_section[section], image=self.img_labels[section])
            self.label_section[section].grid(row=0, column=0, sticky='nsew')

            # initialize the current section's buttons
            for button in self.text[section]: # button = Draft, etc.
                self.buttons[button] = tk.Button(self.frame_section[section], image=self.img_buttons[button]['inactive'], bd=0.1, command=lambda: None)
                row = self.text[section].index(button) + 1 # skip over the first row (reserved for section title)
                self.buttons[button].grid(row=row, column=0, sticky='nsew')

                # bind hover actions
                self.buttons[button].bind('<Enter>', lambda event, button=button: self.on_enter(button))
                self.buttons[button].bind('<Leave>', lambda event, button=button: self.on_leave(button))

            tmp_ctr += 1 # move onto next section

        # assign each button's command
        for section in self.text:
            if section == 'settings':
                self.buttons['game_settings'].config(command=lambda: self.controller.show_frame('DraftSettings'))
                self.buttons['pkmn_settings'].config(command=lambda: self.controller.show_frame('DraftGenerateSettings'))
                self.buttons['Game'].config(command=lambda: None)
                self.buttons['Sets'].config(command=lambda: None)
            else:
                for button in self.text[section]:
                    self.buttons[button].config(command=lambda button=button: self.controller.show_frame(button))

    """function : on_enter
    purpose     : Switches from inactive to active version of the button image.
    @param[in]  : self An instance of the Sidebar object [tk.Frame].
    @param[in]  : button The name of the button [string].
    @return     : None.
    """
    def on_enter(self, button):
        if self.buttons[button].cget('state') != 'disabled':
            self.buttons[button].config(image=self.img_buttons[button]['active'])

    """function : on_leave
    purpose     : Switches from active to inactive version of the button image.
    @param[in]  : self An instance of the Sidebar object [tk.Frame].
    @param[in]  : button The name of the button [string].
    @return     : None.
    """
    def on_leave(self, button):
        if self.buttons[button].cget('state') != 'disabled':
            self.buttons[button].config(image=self.img_buttons[button]['inactive'])


class Draft(tk.Frame):

    """function : __init__
    purpose     : Initializes the Draft page and its components.
    @param[in]  : self An instance of the Draft object [tk.Frame].
    @param[in]  : parent The object type to instantiate [tk.Frame].
    @param[in]  : controller The owner of Draft [MainApp].
    @return     : None.
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller # MainApp

        for i in range(11):
            self.grid_rowconfigure(i, weight=1)
        for i in range(6):
            self.grid_columnconfigure(i, weight=1)

        self.init_vars()
        self.init_pool()
        self.init_bans()
        self.init_teams()

    """function : init_vars
    purpose     : Initializes the Draft page's variables.
    @param[in]  : self An instance of the Draft object [tk.Frame].
    @return     : None.
    """
    def init_vars(self):
        self.alpha = 0 # for image transitions [unused]
        self.turn = 0
        self.game_activated = False # is the game active?
        self.pkmn_not_picked = [True for i in range(18)] # "this" pokemon in the pool available
        self.img_pkmn = {}
        self.separators = [ttk.Separator(self, orient='horizontal') for i in range(2)]

        # game settings variables
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
        self.hidden = tk.StringVar()
        self.hidden.set('No')
        self.current_player = [tk.StringVar(), tk.StringVar()]
        for i in range(2):
            if len(playerNames) < 2:
                self.current_player[i].set('')
            else:
                self.current_player[i].set(playerNames[i])

        # pokemon settings variables
        self.pkmn_excl_tiers_s = [tk.StringVar() for i in range(len(TIERS_SINGLES))]
        self.pkmn_excl_tiers_d = [tk.StringVar() for i in range(len(TIERS_DOUBLES))]
        self.pkmn_excl_gens = [tk.StringVar() for i in range(len(GENERATIONS))]
        self.pkmn_excl_types = [tk.StringVar() for i in range(len(TYPES))]
        self.pkmn_excl_items = [tk.StringVar() for i in range(len(ITEMS))]
        self.pkmn_excl_gimmicks = [tk.StringVar() for i in range(len(GIMMICKS))]
        self.pkmn_excl_usage = []

        self.checks = [[] for i in range(18)] # checks [unusued]
        self.pkmn_ban_list = [[None, None], [None, None]]
        self.pkmn_team_list = [[None for i in range(6)] for j in range(2)]
        self.fp_team_order = [0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 2]
        self.fp_slot_order = [0, 1, 0, 1, 2, 3, 2, 3, 4, 5, 4, 5]

    """function : init_pool
    purpose     : Initializes the Draft page's Pokemon pool section.
    @param[in]  : self An instance of the Draft object [tk.Frame].
    @return     : None.
    """
    def init_pool(self):
        self.img_pool = RGBAImage(os.path.join(COMMON, 'label_pool.png'))
        self.label_pool = tk.Label(self, image=self.img_pool)
        self.label_pool.grid(row=0, column=0, columnspan=5, sticky='nsw')

        self.controller.HelpButton(self, 'Draft', 0, 5, location=self)

        self.pkmn_pool_list = []
        self.pool_buttons = []
        for i in range(3):
            for j in range(6):
                x = (i*6) + j
                self.pool_buttons.append(tk.Button(self, image=self.controller.img_blank['inactive'], bd=0.1, command=lambda: None))
                self.pool_buttons[x].grid(row=i+1, column=j, pady=5)
                self.pool_buttons[x].bind('<Enter>', lambda event, x=x: self.controller.on_enter(self.pool_buttons[x], 'blank'))
                self.pool_buttons[x].bind('<Leave>', lambda event, x=x: self.controller.on_leave(self.pool_buttons[x], 'blank'))

    """function : init_bans
    purpose     : Initializes the Draft page's banned Pokemon section.
    @param[in]  : self An instance of the Draft object [tk.Frame].
    @return     : None.
    """
    def init_bans(self):
        self.separators[0].grid(row=4, column=0, columnspan=6, sticky='nsew')
        self.img_ban = RGBAImage(os.path.join(COMMON, 'bans.png'))
        self.ban_text = tk.Button(self, image=self.img_ban, bd=0.1, state='disabled')
        self.ban_text.grid(row=5, column=2, columnspan=2, sticky='nsew')

        self.ban_buttons = [[], []]
        for i in range(2):
            for j in range(2):
                self.ban_buttons[i].append(tk.Button(self, image=self.controller.img_blank['inactive'], bd=0.1, state='disabled', command=lambda: None))
                # order of buttons is 1 2 | 2 1
                if i == 0:
                    self.ban_buttons[i][j].grid(row=5, column=i*4+j, pady=5)
                else:
                    self.ban_buttons[i][j].grid(row=5, column=i*5-j, pady=5)
        self.separators[1].grid(row=6, column=0, columnspan=6, sticky='nsew')

    """function : init_teams
    purpose     : Initializes the Draft page's team Pokemon section.
    @param[in]  : self An instance of the Draft object [tk.Frame].
    @return     : None.
    """
    def init_teams(self):
        self.team_text = []
        self.team_buttons = [[], []]
        for team in range(2):
            self.team_text.append(tk.Label(self, image=self.controller.img_team_text['team %d' % int(team+1)]))
            self.team_text[team].grid(row=7, column=team*4, columnspan=2, sticky='nsew')
            for row in range(3):
                for column in range(2):
                    x = (row * 2) + column
                    self.team_buttons[team].append(tk.Button(self, image=self.controller.img_blank['inactive'], bd=0.1, command=lambda: None))
                    self.team_buttons[team][x].grid(row=row+8, column=(team*4)+column, pady=5)
                    self.team_buttons[team][x].bind('<Enter>', lambda event, team=team, x=x: self.team_on_enter(team, x))
                    self.team_buttons[team][x].bind('<Leave>', lambda event, team=team, x=x: self.team_on_leave(team, x))
        # TODO FIXME: refactor this to be a dictionary
        self.img_indicator = [[], []]
        for i in range(2):
            self.img_indicator[0].append(RGBAImage(os.path.join(COMMON, 'p%dp.png' %int(i+1))))
            self.img_indicator[1].append(RGBAImage(os.path.join(COMMON, 'p%db.png' %int(i+1))))
        self.indicator = tk.Label(self, image=self.img_indicator[0][0])
        self.indicator.grid(row=8, column=2, rowspan=3, columnspan=2, sticky='nsew')
        self.indicator.grid_remove()
        self.finished = RGBAImage(os.path.join(COMMON, 'finished.png'))

    """function : new_game
    purpose     : Starts a brand new Draft game using the current settings.
    @param[in]  : self An instance of the Draft object [tk.Frame].
    @return     : None.
    """
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
        self.img_pkmn = {}

        temp_excl_tiers = list(filter(None, [i.get() for i in self.pkmn_excl_tiers_s]))
        temp_excl_types = list(filter(None, [i.get() for i in self.pkmn_excl_types]))
        temp_excl_gimmicks = list(filter(None, [i.get() for i in self.pkmn_excl_gimmicks]))
        if self.battle_mode.get() == 'SRL':
            # get each player's roster
            if self.current_player[0].get():
                list1 = PLAYERS[playerNames.index(self.current_player[0].get())].pkmn_list
            else:
                list1 = []
            if self.current_player[1].get():
                list2 = PLAYERS[playerNames.index(self.current_player[1].get())].pkmn_list
            else:
                list2 = []
            temp_list = list1 + list2
        else:
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
                pkmn_name = get_mega_name(self.pkmn_pool_list[i])
            else:
                pkmn_name = self.pkmn_pool_list[i].name
            self.get_pkmn_imgs(i, pkmn_name)
            if self.hidden.get() == 'No':
                self.pool_buttons[i].config(image=self.img_pkmn[i]['inactive'], bd=0.1, command=lambda i=i: self.add_to_team(i))
            else:
                self.pool_buttons[i].config(image=self.img_pkmn[i]['unknown'], bd=0.1, command=lambda i=i: self.add_to_team(i))
            self.pool_buttons[i].bind('<Enter>', lambda event, button=self.pool_buttons[i], i=i: self.on_enter(button, i))
            self.pool_buttons[i].bind('<Leave>', lambda event, button=self.pool_buttons[i], i=i: self.on_leave(button, i))
        for i in range(2):
            for j in range(2):
                self.ban_buttons[i][j].config(image=self.controller.img_blank['inactive'], command=lambda: None)
            for j in range(6):
                self.team_buttons[i][j].config(image=self.controller.img_blank['inactive'], command=lambda: None)
        self.controller.sidebar.buttons['Sets'].config(state='disabled', command=lambda: None)
        if self.ban_number.get() > 0:
            self.indicator.config(image=self.img_indicator[1][1])
        else:
            self.indicator.config(image=self.img_indicator[0][0])
        self.indicator.grid()

    """function : get_pkmn_imgs
    purpose     : Determines the correct filename to load and adds the Pokemon
                  image to add to the list.
    @param[in]  : self An instance of the Draft object [tk.Frame].
    @param[in]  : pkmn_name The raw name of the Pokemon [string].
    @return     : None.
    """
    def get_pkmn_imgs(self, pool_num, pkmn_name):
        pkmn_filename = pkmn_name.replace('-Small', '').replace('-Large', '').replace('-Super', '').replace(':', '')
        self.img_pkmn[pool_num] = {}
        for i in ['inactive', 'active', 'unknown', 'banned', 'picked']:
            self.img_pkmn_base = RGBAImage2(os.path.join(IMG_PKMN_DIR, pkmn_filename + '_' + i + '.png'))
            self.img_pkmn_base.paste(self.controller.img_border[self.draft_mode.get()], (0, 0), self.controller.img_border[self.draft_mode.get()])
            self.img_pkmn[pool_num][i] = ImageTk.PhotoImage(self.img_pkmn_base)

    """function : get_checks
    purpose     : Creates a list of checks and counters to every Pokemon that
                  was generated this game.
    @param[in]  : self An instance of the Draft object [tk.Frame].
    @return     : None.
    """
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

    """function : add_to_team
    purpose     : Appends the Pokemon object to the correct team.
    @param[in]  : self An instance of the Draft object [tk.Frame].
    @param[in]  : pool_number The index of the Pokemon object in the pool [int].
    @return     : None.
    """
    def add_to_team(self, pool_number):
        if self.game_activated: # there must be an active game
            if self.pkmn_not_picked[pool_number]: # the pokemon being picked must be available
                if self.turn < 12: # the drafting phase is not over yet
                    # determine the team to add the pokemon to and the slot number on the team
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

                    # TODO FIXME: Check order of events
                    # check if the pokemon being added is breaking species clause
                    if self.pkmn_pool_list[pool_number].dex in [i.dex for i in self.pkmn_team_list[team_number] if i is not None]:
                        popup_message(self.controller,
                                      'ERROR',
                                      "Sorry, you cannot add %s to Player %s's team" % (self.pkmn_pool_list[pool_number].name, str(team_number+1)),
                                      text2="\ndue to the Species Clause.")
                    else:
                        # everything is valid, start adding to team or banning
                        self.pkmn_not_picked[pool_number] = False
                        if self.ban_number.get() != 0 and not self.ban_phase_finished:
                            self.pool_buttons[pool_number].config(image=self.img_pkmn[pool_number]['banned'], command=lambda: None)
                            self.ban_pkmn(pool_number)
                        else:
                            self.pool_buttons[pool_number].config(image=self.img_pkmn[pool_number]['picked'], command=lambda: None)
                            self.pkmn_team_list[team_number][slot_number] = self.pkmn_pool_list[pool_number]
                            self.team_buttons[team_number][slot_number].config(image=self.img_pkmn[pool_number]['inactive'],
                                command=lambda i=pool_number, j=team_number, k=slot_number: self.remove(i, j, k, self.pkmn_team_list, self.team_buttons))
                            self.update_turns()
                        self.update_turn_indicator()


    """function : remove_from_team
    purpose     : Removes the Pokemon object from the selected team and slot
                  and makes it available in the pool again.
    @param[in]  : self An instance of the Draft object [tk.Frame].
    @param[in]  : pool_number The index of the Pokemon object in the pool [int].
    @param[in]  : team_number The index of the selected team [int].
    @param[in]  : slot_number The index of the Pokemon in the team [int].
    @param[in]  : list The source list of Pokemon to remove from [Pokemon list].
    @param[in]  : button The source list of buttons to modify [tk.Button list].
    @return     : None.
    """
    def remove(self, pool_number, team_number, slot_number, list, button):
        if self.game_activated:
            # reset/clear variables
            self.pkmn_not_picked[pool_number] = True
            list[team_number][slot_number] = None
            if list == self.pkmn_ban_list:
                print("hi")
                self.ban_phase_finished = False
            if self.hidden.get() == 'No':
                self.pool_buttons[pool_number].config(image=self.img_pkmn[pool_number]['inactive'], command=lambda i=pool_number: self.add_to_team(i))
            else:
                self.pool_buttons[pool_number].config(image=self.img_pkmn[pool_number]['unknown'], command=lambda i=pool_number: self.add_to_team(i))
            button[team_number][slot_number].config(image=self.controller.img_blank['inactive'], command=lambda: None)
            self.update_turns()
            self.update_turn_indicator()

    """function : ban_pkmn
    purpose     : Appends the Pokemon object to the current player's ban list.
    @param[in]  : self An instance of the Draft object [tk.Frame].
    @param[in]  : pool_number The index of the Pokemon object in the pool [int].
    @return     : None.
    """
    def ban_pkmn(self, pool_number):
        # add pkmn to proper banlist
        temp_done = False
        for i in range(self.ban_number.get()):
            for j in range(2):
                if not self.pkmn_ban_list[1-j][i]:
                    self.pkmn_ban_list[1-j][i] = self.pkmn_pool_list[pool_number]
                    self.ban_buttons[1-j][i].config(image=self.img_pkmn[pool_number]['inactive'],
                        command=lambda pool_number=pool_number, i=i, j=j: self.remove(pool_number, 1-j, i, self.pkmn_ban_list, self.ban_buttons))
                    temp_done = True
                    break
            if temp_done:
                break

        # TODO FIXME: reset each phase to false?
        # end the ban phase
        if ((self.turn >= 0 and self.pkmn_ban_list[0][0]) and
            (self.turn >= 0 and self.pkmn_ban_list[1][0])):
            self.ban_phase_1_finished = True
        if (((self.turn >= 8 and self.pkmn_ban_list[0][1] and self.draft_mode.get() == 'First Pick') and
             (self.turn >= 8 and self.pkmn_ban_list[1][1] and self.draft_mode.get() == 'First Pick')) or
            ((self.turn >= 6 and self.pkmn_ban_list[0][1] and self.draft_mode.get() != 'First Pick') and
             (self.turn >= 6 and self.pkmn_ban_list[1][1] and self.draft_mode.get() != 'First Pick'))):
            self.ban_phase_2_finished = True
        if ((self.turn >= 0 and self.ban_phase_1_finished) or
            ((self.turn >= 8 and self.ban_phase_2_finished and self.draft_mode.get() == 'First Pick') or
            (self.turn >= 6 and self.ban_phase_2_finished and self.draft_mode.get() != 'First Pick'))):
            self.ban_phase_finished = True


    """function : update_turns
    purpose     : Determines the next turn based on the game mode.
    @param[in]  : self An instance of the Draft object [tk.Frame].
    @return     : None.
    """
    def update_turns(self):
        # from the start, check if each team slot is empty
        next_turn = 0
        for i in range(12):
            if self.draft_mode.get() == 'First Pick':
                if not self.pkmn_team_list[self.fp_team_order[i]][self.fp_slot_order[i]]:
                    break
            elif self.draft_mode.get() == 'Standard':
                if not self.pkmn_team_list[int(i%2)][int(i/2)]:
                    break
            elif self.draft_mode.get() == 'Nemesis':
                if not self.pkmn_team_list[int((i+1)%2)][int(i/2)]:
                    break
            next_turn += 1
        self.turn = next_turn

        # TODO FIXME: Update ban phase properly

        # change sets button if game is or is not finished
        if self.turn >= 12:
            state = 'normal'
        else:
            state = 'disabled'
        self.controller.sidebar.buttons['Sets'].config(state=state, command=lambda: get_sets(self))


    """function : update_turn_indicator
    purpose     : Updates the indicator to reflect the current turn.
    @param[in]  : self An instance of the Draft object [tk.Frame].
    @return     : None.
    """
    def update_turn_indicator(self):
        if self.ban_number.get() > 0 and not self.ban_phase_finished:
            if not self.pkmn_ban_list[0][0] and self.pkmn_ban_list[1][0]:
                self.indicator.config(image=self.img_indicator[1][0])
            elif self.pkmn_ban_list[0][0] and self.turn == 0:
                self.indicator.config(image=self.img_indicator[0][0])
            elif not self.pkmn_ban_list[1][1] and not self.ban_phase_finished and self.ban_number.get() == 2:
                self.indicator.config(image=self.img_indicator[1][1])
            elif not self.pkmn_ban_list[0][1] and self.pkmn_ban_list[1][1]:
                self.indicator.config(image=self.img_indicator[1][0])
            else:
                self.indicator.config(image=self.img_indicator[0][0])
        else:
            if self.turn >= 12:
                self.indicator.config(image=self.finished)
            else:
                if self.draft_mode.get() == 'First Pick':
                    turn = self.fp_team_order[self.turn]
                else:
                    turn = self.turn % 2
                self.indicator.config(image=self.img_indicator[0][turn])
        self.indicator.grid()


    def on_enter(self, button, index):
        if self.game_activated:
            if self.pkmn_not_picked[index]:
                if self.hidden.get() == 'No':
                    button.config(image=self.img_pkmn[index]['active'])
                else:
                    pass
            else:
                pass
        else:
            if self.pkmn_not_picked[index]:
                if self.hidden.get() == 'No':
                    self.pool_buttons[index].config(image=self.controller.img_blank['active'])
                else:
                    pass
            else:
                pass

    def on_leave(self, button, index):
        if self.game_activated:
            if self.pkmn_not_picked[index]:
                if self.hidden.get() == 'No':
                    button.config(image=self.img_pkmn[index]['inactive'])
                else:
                    pass
            else:
                pass
        else:
            self.pool_buttons[index].config(image=self.controller.img_blank['inactive'])

    def team_on_enter(self, team, x):
        if self.pkmn_team_list[team][x]:
            pool_num = self.pkmn_pool_list.index(self.pkmn_team_list[team][x])
            self.team_buttons[team][x].config(image=self.img_pkmn[pool_num]['active'])
        else:
            self.team_buttons[team][x].config(image=self.controller.img_blank['active'])

    def team_on_leave(self, team, x):
        if self.pkmn_team_list[team][x]:
            pool_num = self.pkmn_pool_list.index(self.pkmn_team_list[team][x])
            self.team_buttons[team][x].config(image=self.img_pkmn[pool_num]['inactive'])
        else:
            self.team_buttons[team][x].config(image=self.controller.img_blank['inactive'])

    def replace_images(self):
        if self.game_activated:
            self.img_pkmn = {}
            for i in range(len(self.pkmn_pool_list)):
                self.img_pkmn[i] = {}
                for j in ['inactive', 'active', 'unknown', 'banned', 'picked']:
                    if self.show_megas.get() == 'Yes':
                        pkmn_name = get_mega_name(self.pkmn_pool_list[i].name)
                    else:
                        pkmn_name = self.pkmn_pool_list[i].name
                    pkmn_name = pkmn_name.replace('-Small', '').replace('-Large', '').replace('-Super', '').replace(':', '')
                    self.img_pkmn_base = RGBAImage2(os.path.join(IMG_PKMN_DIR, pkmn_name + '_' + j + '.png'))
                    self.img_pkmn_base.paste(self.controller.img_border[self.draft_mode.get()], (0, 0), self.controller.img_border[self.draft_mode.get()])
                    self.img_pkmn[i][j] = ImageTk.PhotoImage(self.img_pkmn_base)

            for i in range(len(self.pkmn_pool_list)):
                if self.pkmn_not_picked[i]:
                    if self.hidden.get() == 'No':
                        self.pool_buttons[i].config(image=self.img_pkmn[i]['inactive'])
                    else:
                        self.pool_buttons[i].config(image=self.img_pkmn[i]['unknown'])
                else:
                    self.pool_buttons[i].config(image=self.img_pkmn[i]['picked'])

            for i in range(2):
                for j in range(6):
                    if self.pkmn_team_list[i][j] != None:
                        pool_num = self.get_pool_num(self.pkmn_team_list[i][j].name)
                        self.team_buttons[i][j].config(image=self.img_pkmn[pool_num]['inactive'])

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
        if self.parent_page().battle_mode.get() == 'SRL':
            for i in range(2):
                self.player_option[i].grid()
        else:
            for i in range(2):
                self.player_option[i].grid_remove()

    def change_draft_mode(self):
        if self.parent_page().game_activated:
            popup_message(self.controller,
                          'ERROR',
                          'Changing the draft mode has caused the current game to be erased.',
                          text2='\nPlease start a new game.')
            self.parent_page().game_activated = False
        for i in range(2):
            for j in range(0, self.parent_page().ban_number.get()):
                self.parent_page().ban_buttons[i][j].config(image=self.controller.img_blank['inactive'],
                                                            state='normal',
                                                            command=lambda: None)
            for j in range(self.parent_page().ban_number.get(), 2):
                self.parent_page().ban_buttons[i][j].config(image=self.controller.img_blank['inactive'],
                                                            state='disabled',
                                                            command=lambda: None)
        for i in range(18):
            self.parent_page().pool_buttons[i].config(image=self.controller.img_blank['inactive'],
                                                      command=lambda: None)
        self.parent_page().pkmn_pool_list = []
        self.parent_page().pkmn_not_picked = [True for i in range(18)]
        for i in range(2):
            for j in range(6):
                self.parent_page().team_buttons[i][j].config(image=self.controller.img_blank['inactive'],
                                                             command=lambda: None)
                self.parent_page().pkmn_team_list[i][j] = None
        self.parent_page().ban_phase_finished = False
        if self.parent_page().ban_number.get() == 0:
            self.parent_page().ban_text.config(state='disabled')
        else:
            self.parent_page().ban_text.config(state='normal')
        self.parent_page().indicator.grid_remove()

    def activate_bans(self):
        if self.parent_page().game_activated:
            popup_message(self.controller,
                          'ERROR',
                          'Changing the number of bans has caused the current game to be erased.',
                          text2='\nPlease start a new game.')
            self.parent_page().game_activated = False
        for i in range(2):
            for j in range(0, self.parent_page().ban_number.get()):
                self.parent_page().ban_buttons[i][j].config(image=self.controller.img_blank['inactive'],
                                                            state='normal',
                                                            command=lambda: None)
            for j in range(self.parent_page().ban_number.get(), 2):
                self.parent_page().ban_buttons[i][j].config(image=self.controller.img_blank['inactive'],
                                                            state='disabled',
                                                            command=lambda: None)
        for i in range(18):
            self.parent_page().pool_buttons[i].config(image=self.controller.img_blank['inactive'],
                                                      command=lambda: None)
        self.parent_page().pkmn_pool_list = []
        self.parent_page().pkmn_not_picked = [True for i in range(18)]
        for i in range(2):
            for j in range(6):
                self.parent_page().team_buttons[i][j].config(image=self.controller.img_blank['inactive'],
                                                             command=lambda: None)
                self.parent_page().pkmn_team_list[i][j] = None
        self.parent_page().ban_phase_finished = False
        if self.parent_page().ban_number.get() == 0:
            self.parent_page().ban_text.config(state='disabled')
        else:
            self.parent_page().ban_text.config(state='normal')
        self.parent_page().indicator.grid_remove()

    def parent_page(self):
        return self.controller.pages['Draft']


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
        for i in range(3):
            self.grid_rowconfigure(i, weight=1)
        self.hidden = tk.StringVar()
        self.hidden.set('No')
        self.current_player = [tk.StringVar(), tk.StringVar()]
        for i in range(2):
            if len(playerNames) < 2:
                self.current_player[i].set('')
            else:
                self.current_player[i].set(playerNames[i])
        self.type = [tk.StringVar(), tk.StringVar()]
        for i in range(2):
            self.type[i].set(TYPES[0])

        self.img_pkmn = [[] for i in range(3)]
        self.frames = []
        for i in range(3):
            self.frames.append(tk.Frame(self))
            self.frames[i].grid(row=i, column=0, sticky='nsew')
        self.frames[1].grid_columnconfigure(0, weight=1)
        self.frames[1].grid_columnconfigure(3, weight=1)
        self.frames[1].grid_columnconfigure(6, weight=1)

        self.pkmn_excl_tiers_s = [tk.StringVar() for i in range(len(TIERS_SINGLES))]
        self.pkmn_excl_tiers_d = [tk.StringVar() for i in range(len(TIERS_DOUBLES))]
        self.pkmn_excl_gens = [tk.StringVar() for i in range(len(GENERATIONS))]
        self.pkmn_excl_types = [tk.StringVar() for i in range(len(TYPES))]
        self.pkmn_excl_items = [tk.StringVar() for i in range(len(ITEMS))]
        self.pkmn_excl_gimmicks = [tk.StringVar() for i in range(len(GIMMICKS))]
        self.pkmn_excl_usage = []

        ##### Team Boxes #####
        self.img_random = RGBAImage(os.path.join(COMMON, 'label_random.png'))
        self.random_label = tk.Label(self.frames[0], image=self.img_random)
        self.random_label.grid(row=0, column=0, pady=2, sticky='nsw')
        self.img_team_text = []
        for i in range(2):
            self.img_team_text.append(RGBAImage(os.path.join(COMMON, 'team%d.png' %int(i+1))))
        self.team_text = []
        self.pkmn_team_list = [[None for i in range(6)] for j in range(2)]
        self.team_buttons = [[], []]
        for team in range(2):
            self.team_text.append(tk.Label(self.frames[1], image=self.img_team_text[team]))
            self.team_text[team].grid(row=1, column=(team*3)+1, columnspan=2,
                                      sticky='nsew')
            for row in range(3):
                for column in range(2):
                    x = (row * 2) + column
                    self.team_buttons[team].append(tk.Button(self.frames[1],
                                                             image=self.controller.img_blank['inactive'],
                                                             bd=0.1,
                                                             command=lambda: None))
                    self.team_buttons[team][x].grid(row=row+2,
                                                    column=(team*3)+column+1,
                                                    padx=10, pady=10)
                    self.team_buttons[team][x].bind('<Enter>', lambda event, team=team, x=x: self.team_on_enter(team, x))
                    self.team_buttons[team][x].bind('<Leave>', lambda event, team=team, x=x: self.team_on_leave(team, x))

    def new_game(self):
        # reset private variables
        self.game_activated = True
        self.pkmn_team_list = [[None for i in range(6)] for j in range(2)]
        self.img_pkmn = [[] for i in range(3)]

        temp_excl_tiers = list(filter(None, [i.get() for i in self.pkmn_excl_tiers_s]))
        temp_excl_types = list(filter(None, [i.get() for i in self.pkmn_excl_types]))
        temp_excl_gimmicks = list(filter(None, [i.get() for i in self.pkmn_excl_gimmicks]))
        if self.battle_mode.get() == 'SRL':
            if self.current_player[0].get():
                list1 = PLAYERS[playerNames.index(self.current_player[0].get())].pkmn_list
            else:
                list1 = []
            if self.current_player[1].get():
                list2 = PLAYERS[playerNames.index(self.current_player[1].get())].pkmn_list
            else:
                list2 = []
            self.temp_list = list1 + list2
        else:
            self.temp_list = []
        for pkmn in ALL_POKEMON_S:
            if self.theme.get() == 'Monotype':
                incl_type = [self.type[0].get(), self.type[1].get()]
                if ((pkmn.name in [i.name for i in self.temp_list]) or
                    (pkmn.tier in temp_excl_tiers) or
                    ((pkmn.type[0] not in incl_type) and
                     (pkmn.type[1] not in incl_type)) or
                    (check_valid_generation(self, pkmn)) or
                    (check_valid_item(self, pkmn)) or
                    (pkmn.tag in temp_excl_gimmicks)):
                    continue
                else:
                    self.temp_list.append(pkmn)
            else:
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
                temp_new_pkmn = random.choice(self.temp_list)
                if i == 1 and self.theme.get() == 'Balanced':
                    if ((check_validity(self, temp_new_pkmn, i)) and
                        (temp_new_pkmn.tier == self.pkmn_team_list[0][counter].tier)):
                        self.pkmn_team_list[i][counter] = temp_new_pkmn
                        counter += 1
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
                if self.hidden.get() == 'Yes':
                    self.team_buttons[i][j].config(image=self.img_pkmn[2][x],
                        command=lambda i=i, j=j: self.reroll(i, j))
                else:
                    self.team_buttons[i][j].config(image=self.img_pkmn[0][x],
                        command=lambda i=i, j=j: self.reroll(i, j))
        self.controller.sidebar.buttons['Sets'].config(state='normal', command=lambda: get_sets(self))

    def get_pkmn_imgs(self, pkmn_name):
        pkmn_name = pkmn_name.replace('-Small', '').replace('-Large', '').replace('-Super', '').replace(':', '')
        self.img_pkmn_base = [RGBAImage2(os.path.join(IMG_PKMN_DIR, pkmn_name + '_inactive.png')),
                              RGBAImage2(os.path.join(IMG_PKMN_DIR, pkmn_name + '_active.png')),
                              RGBAImage2(os.path.join(IMG_PKMN_DIR, pkmn_name + '_unknown.png'))]
        for i in range(3):
            self.img_pkmn_base[i].paste(self.controller.img_border['Random'],
                                        (0, 0),
                                        self.controller.img_border['Random'])
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
        if self.hidden.get() == 'No':
            if self.pkmn_team_list[team][x]:
                pool_num = (team * 6) + x
                self.team_buttons[team][x].config(image=self.img_pkmn[1][pool_num])
            else:
                self.team_buttons[team][x].config(image=self.controller.img_blank['active'])

    def team_on_leave(self, team, x):
        if self.hidden.get() == 'No':
            if self.pkmn_team_list[team][x]:
                pool_num = (team * 6) + x
                self.team_buttons[team][x].config(image=self.img_pkmn[0][pool_num])
            else:
                self.team_buttons[team][x].config(image=self.controller.img_blank['inactive'])

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
                            for k in range(3):
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
                        for k in range(3):
                            self.img_pkmn_base[k].paste(
                                self.controller.img_border['Random'],
                                (0, 0),
                                self.controller.img_border['Random'])
                            self.img_pkmn[k][x] = ImageTk.PhotoImage(self.img_pkmn_base[k])
            for i in range(2):
                for j in range(6):
                    x = (i * 6) + j
                    if self.hidden.get() == 'No':
                        self.team_buttons[i][j].config(image=self.img_pkmn[0][x])
                    else:
                        self.team_buttons[i][j].config(image=self.img_pkmn[2][x])


class RandomSettings(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        setup_game_settings(self, 'Random')

    def update_gen_settings(self):
        if self.parent_page().battle_mode.get() == 'Singles' or self.parent_page().battle_mode.get() == 'SRL':
            for button in self.controller.pages['RandomGenerateSettings'].tier_buttons:
                button.config(state='normal')
            for button in self.controller.pages['RandomGenerateSettings'].tier2_buttons:
                button.config(state='disabled')
        if self.parent_page().battle_mode.get() == 'Doubles':
            for button in self.controller.pages['RandomGenerateSettings'].tier_buttons:
                button.config(state='disabled')
            for button in self.controller.pages['RandomGenerateSettings'].tier2_buttons:
                button.config(state='normal')
        if self.parent_page().battle_mode.get() == 'SRL':
            for button in self.player_option:
                button.grid()
        else:
            for button in self.player_option:
                button.grid_remove()
        if self.parent_page().theme.get() == 'Monotype':
            for button in self.type_option:
                button.grid()
            for button in self.controller.pages['RandomGenerateSettings'].type_buttons:
                button.config(state='disabled')
        else:
            for button in self.type_option:
                button.grid_remove()
            for button in self.controller.pages['RandomGenerateSettings'].type_buttons:
                button.config(state='normal')

    def parent_page(self):
        return self.controller.pages['Random']


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

        if month <= 6 or (month == 6 and 1 <= day <= 8):
            self.banner_num = 0
        if month == 6 and 9 <= day <= 15:
            self.banner_num = 2
        if month == 6 and 16 <= day <= 22:
            self.banner_num = 4
        if month == 6 and 23 <= day <= 29:
            self.banner_num = 6
        if (month == 6 and 30 == day) or (month == 7 and 1 <= day <= 6):
            self.banner_num = 8
        if month == 7 and 7 <= day <= 13:
            self.banner_num = 10
        if month == 7 and 14 <= day <= 20:
            self.banner_num = 12
        if month == 7 and 21 <= day <= 27:
            self.banner_num = 14
        # self.banner_num = 0
        self.current_page = 0
        self.remaining = 44
        self.current_player = tk.StringVar()
        self.current_player.set(PLAYERS[0].name)

        self.img_banners = []
        self.img_banner_buttons = []
        for i in range(self.banner_num, self.banner_num+2):
            self.img_banners.append(
                RGBAImage(os.path.join(COMMON, 'banner%s_fit.png' % i)))
            self.img_banner_buttons.append(
                RGBAImage(os.path.join(COMMON, 'banner%s_button.png' % i)))
        self.banner_image = tk.Label(self, image=self.img_banners[0])
        self.banner_image.grid(row=0, column=0, columnspan=4, sticky='nsew')
        self.page_frame = tk.Frame(self)
        self.page_frame.grid(row=2, column=0, columnspan=4, sticky='nsew')
        for i in range(4):
            self.page_frame.grid_columnconfigure(i, weight=1)
        self.page_buttons = []
        self.controller.HelpButton(self, 'Store', 0, 2, location=self.page_frame)
        for i in range(2):
            self.page_buttons.append(tk.Button(self.page_frame,
                image=self.img_banner_buttons[i],
                bd=0.1,
                command=lambda i=i: self.change_page(i)))
            self.page_buttons[i].grid(row=0, column=i, padx=5, sticky='nsew')

        self.scrollframe = tk.LabelFrame(self, text='Available Pokemon')
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
                    command=lambda: None)
                self.container.create_window((j*100)+50, (i*70)+30,
                                             window=self.pkmn_buttons[i][j])

        self.pull_result = tk.Label(self, image=self.controller.img_blank['inactive'])
        self.pull_result.grid(row=8, column=0, padx=5, pady=5, sticky='nsew')
        self.player_option = tk.OptionMenu(self, self.current_player,
                                         *playerNames, command=self.switch_player)
        self.player_option.grid(row=8, column=1, padx=5, pady=5, sticky='ew')

        self.img_pull = []
        for i in ['inactive', 'active']:
            self.img_pull.append(RGBAImage(os.path.join(COMMON,
                                                        'button_%s_Pull.png' % i)))
        self.pull_button = tk.Button(self, image=self.img_pull[0], bd=0.1,
                                     command=self.pull)
        self.pull_button.grid(row=8, column=2)
        self.pull_button.bind('<Enter>', lambda event: self.on_enter())
        self.pull_button.bind('<Leave>', lambda event: self.on_leave())
        self.remaining_label = tk.Label(self, text='Available:\n%d/44' % self.remaining)
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
        for i in range(2):
            for j in range(44):
                cur_banner = self.banner_num + i
                pkmn_name = ALL_BANNERS[cur_banner][j].replace('-Small', '').replace('-Large', '').replace('-Super', '').replace(':', '')
                if pkmn_name == 'Blank':
                    for k in range(3):
                        self.img_pkmn[i][k].append(self.controller.img_blank['inactive'])
                else:
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
        self.current_player.set(player)
        self.remaining = 44
        slot = playerNames.index(player)
        player_pkmn_list = PLAYERS[slot].pkmn_list
        player_pkmn_name_list = [get_mega_name(i) for i in player_pkmn_list]
        for i in range(9):
            for j in range(len(self.pkmn_buttons[i])):
                x = (i * 5) + j
                if ALL_BANNERS[self.banner_num+self.current_page][x] == 'Blank':
                    self.pkmn_buttons[i][j].config(
                        image=self.img_pkmn[self.current_page][2][x],
                        command=lambda: None)
                else:
                    if ALL_BANNERS[self.banner_num+self.current_page][x] in player_pkmn_name_list:
                        self.pkmn_buttons[i][j].config(
                            image=self.img_pkmn[self.current_page][2][x],
                            command=lambda x=x: self.remove_from_team(x))
                        self.remaining -= 1
                    else:
                        self.pkmn_buttons[i][j].config(
                            image=self.img_pkmn[self.current_page][0][x],
                            command=lambda x=x: self.add_to_team(x))
        self.remaining_label.config(text='Available:\n%d/44' % self.remaining)
        if ALL_BANNERS[self.banner_num+self.current_page][0] == 'Blank':
            self.pull_button.config(state='disabled')
        else:
            self.pull_button.config(state='normal')

    def pull(self):
        if self.remaining <= 0:
            popup_message(self.controller,
                          'ERROR',
                          'No Pokemon remaining!')
        else:
            slot = playerNames.index(self.current_player.get())
            player_pkmn_list = PLAYERS[slot].pkmn_list
            player_pkmn_name_list = [get_mega_name(i) for i in player_pkmn_list]
            while True:
                temp_new_pkmn = random.choice(self.pkmn_lists[self.current_page])
                if get_mega_name(temp_new_pkmn) not in player_pkmn_name_list:
                    PLAYERS[slot].pkmn_list.append(temp_new_pkmn)
                    pkmn_index = ALL_BANNERS[self.banner_num + self.current_page].index(
                        get_mega_name(temp_new_pkmn))
                    for i in range(9):
                        for j in range(len(self.pkmn_buttons[i])):
                            x = (i * 5) + j
                            if x == pkmn_index:
                                self.pkmn_buttons[i][j].config(
                                    image=self.img_pkmn[self.current_page][2][x],
                                    command=lambda x=x: self.remove_from_team(x))
                                self.pull_result.config(
                                    image=self.img_pkmn[self.current_page][0][x])
                                self.remaining -= 1
                                self.remaining_label.config(text='Available:\n%d/44' % self.remaining)
                    self.update_player_csv(slot)
                    break

    def add_to_team(self, x):
        current_banner = self.banner_num + self.current_page
        slot = playerNames.index(self.current_player.get())
        player_pkmn_list = PLAYERS[slot].pkmn_list
        player_pkmn_name_list = [i.name for i in player_pkmn_list]

        temp_pkmn_list = []
        for pkmn in self.pkmn_lists[self.current_page]:
            if pkmn.name == get_true_name(ALL_BANNERS[current_banner][x]):
                temp_pkmn_list.append(pkmn)
        temp_new_pkmn = random.choice(temp_pkmn_list)
        PLAYERS[slot].pkmn_list.append(temp_new_pkmn)
        self.remaining -= 1
        self.remaining_label.config(text='Available:\n%d/44' % self.remaining)

        for i in range(9):
            for j in range(len(self.pkmn_buttons[i])):
                y = (i * 5) + j
                if y == x:
                    self.pkmn_buttons[i][j].config(
                        image=self.img_pkmn[self.current_page][2][y],
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
        self.remaining_label.config(text='Available:\n%d/44' % self.remaining)

        for i in range(9):
            for j in range(len(self.pkmn_buttons[i])):
                y = (i * 5) + j
                if y == x:
                    self.pkmn_buttons[i][j].config(
                        image=self.img_pkmn[self.current_page][0][y],
                        command=lambda y=y: self.add_to_team(y))
        self.update_player_csv(slot)

    def change_page(self, page_num):
        if self.current_page != page_num:
            self.current_page = page_num
            self.banner_image.config(image=self.img_banners[self.current_page])
            self.switch_player(self.current_player.get())
            if self.current_page + self.banner_num == 7 or self.current_page + self.banner_num == 15:
                self.pull_button.config(state='disabled')
            else:
                self.pull_button.config(state='normal')

    def on_enter(self):
        if self.pull_button.cget('state') != 'disabled':
            self.pull_button.config(image=self.img_pull[1])

    def on_leave(self):
        if self.pull_button.cget('state') != 'disabled':
            self.pull_button.config(image=self.img_pull[0])

    def update_player_csv(self, slot):
        file = os.path.join(PLAYER_DIR, self.current_player.get() + '.csv')
        with open(file, 'w', encoding='utf-8', newline='') as fileName:
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
        self.controller.show_frame('StoreHelpPage')


class Players(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.current_player = tk.StringVar()
        self.current_player.set(PLAYERS[0].name)

        # add new player
        self.img_new_player = RGBAImage(os.path.join(COMMON, 'label_new_player.png'))
        self.new_player_label = tk.Label(self, image=self.img_new_player)
        self.new_player_label.grid(row=0, column=0, columnspan=2, pady=2, sticky='nsw')
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
        # text instructions | drop down | get all set details
        self.player_instruct_img = RGBAImage(os.path.join(COMMON, 'label_instruct.png'))
        self.player_instruct_text = tk.Label(self, image=self.player_instruct_img)
        self.player_instruct_text.grid(row=3, column=0, sticky='nse')
        self.player_option = tk.OptionMenu(self, self.current_player,
                                         *playerNames, command=self.display_pkmn)
        self.player_option.grid(row=3, column=1, sticky='ew')
        self.get_sets_button = tk.Button(self, text='Copy All Sets', command=self.get_sets)
        self.get_sets_button.grid(row=3, column=2, padx=10, sticky='ew')
        # [grid with pokemon icons]
        self.scrollframe = tk.LabelFrame(self,
            text='Pokemon Collection (%d Total)' %len(PLAYERS[0].pkmn_list))
        self.scrollframe.grid(row=4, column=0, rowspan=3, columnspan=3, padx=5,
                              pady=5, sticky='nsew')
        self.container = tk.Canvas(self.scrollframe,
                                   scrollregion=(0, 0, 400, 1640))
        self.scrollbar = ttk.Scrollbar(self.scrollframe, orient='vertical',
                                       command=self.container.yview)
        self.container.config(yscrollcommand=self.scrollbar.set)
        self.container.bind('<Enter>', self._on_mousewheel)
        self.container.bind('<Leave>', self._off_mousewheel)
        self.scrollbar.pack(side='right', fill='y')
        self.container.pack(side='left', expand=True, fill='both')
        self.pkmn_img = [[], []]
        self.pkmn_buttons = []
        self.button_id = []
        self.display_pkmn(self.current_player.get())

        for i in range(1, 3):
            self.grid_columnconfigure(i, weight=1)
        self.grid_rowconfigure(4, weight=1)

    def add_player(self):
        player_name = self.enter_name.get().strip()
        self.enter_name.delete(0, 'end')
        if player_name and player_name.lower() not in [i.lower() for i in playerNames]:
            PLAYERS.append(Player(player_name, []))
            playerNames.append(player_name)
            update_all_optionmenus(self.controller)
            for key, button in self.controller.sidebar.buttons.items():
                button.config(state='disabled')
            self.controller.pages['NewPull'].clear()
            self.controller.show_frame('NewPull')

        elif player_name.lower() in [i.lower() for i in playerNames]:
            popup_message(self.controller,
                          'ERROR',
                          player_name + ' is already in use. Please choose another name.')
        else:
            pass

    def display_pkmn(self, player_name):
        self.current_player.set(player_name)
        cur_player = PLAYERS[playerNames.index(self.current_player.get())]
        self.scrollframe.config(text='Pokemon Collection (%d Total)' %len(cur_player.pkmn_list))
        self.pkmn_buttons = []
        if self.button_id:
            for id in self.button_id:
                self.container.delete(id)
        self.button_id = []
        self.pkmn_img = [[], []]
        for i in range(len(cur_player.pkmn_list)):
            self.get_pkmn_imgs(get_mega_name(cur_player.pkmn_list[i]))
            self.pkmn_buttons.append(tk.Button(self.container,
                image=self.pkmn_img[0][i],
                bd=0.1,
                command=lambda i=i: self.get_specific_set(cur_player.pkmn_list[i])))
            self.pkmn_buttons[i].bind('<Enter>', lambda event, i=i: self.on_enter(i))
            self.pkmn_buttons[i].bind('<Leave>', lambda event, i=i: self.on_leave(i))
            self.button_id.append(self.container.create_window(
                ((i%6)*80)+50, (int(i/6)*70)+30, window=self.pkmn_buttons[i]))

    def get_pkmn_imgs(self, pkmn_name):
        pkmn_name = pkmn_name.replace('-Small', '').replace('-Large', '').replace('-Super', '').replace(':', '')
        self.img_pkmn_base = [RGBAImage2(os.path.join(IMG_PKMN_DIR, pkmn_name + '_inactive.png')),
                              RGBAImage2(os.path.join(IMG_PKMN_DIR, pkmn_name + '_active.png'))]
        for i in range(2):
            self.img_pkmn_base[i].paste(self.controller.img_border[get_rarity(pkmn_name)],
                                        (0, 0),
                                        self.controller.img_border[get_rarity(pkmn_name)])
        for i in range(2):
            self.pkmn_img[i].append(ImageTk.PhotoImage(self.img_pkmn_base[i]))

    def get_sets(self):
        cur_player = PLAYERS[playerNames.index(self.current_player.get())]
        self.controller.clipboard_clear()
        sets = ''
        for pkmn in cur_player.pkmn_list:
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
            sets += '\n'
        self.controller.clipboard_append(sets)
        popup_message(self.controller,
                      'INFO',
                      "Copied all of %s's Pokemon to clipboard." % cur_player.name)

    def get_specific_set(self, pkmn):
        self.controller.clipboard_clear()
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
        self.controller.clipboard_append(sets)
        popup_message(self.controller,
                      'INFO',
                      "Copied %s's set to clipboard." % pkmn.name)

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


class DraftHelpPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.scrollframe = tk.Frame(self)
        self.scrollframe.grid(row=0, column=0, sticky='nsew')
        self.container = tk.Canvas(self.scrollframe,
                                   scrollregion=(0, 0, 400, 3000))
        self.scrollbar = ttk.Scrollbar(self.scrollframe, orient='vertical',
                                       command=self.container.yview)
        self.container.config(yscrollcommand=self.scrollbar.set)
        self.container.bind('<Enter>', self._on_mousewheel)
        self.container.bind('<Leave>', self._off_mousewheel)
        self.scrollbar.pack(side='right', fill='y')
        self.container.pack(side='left', expand=True, fill='both')

        self.img_help = RGBAImage(os.path.join(COMMON, 'help_play.png'))
        self.help = tk.Label(self.container, image=self.img_help)
        self.container.create_window(255, 1480,
                                     window=self.help)

        self.back_button = tk.Button(self, image=self.controller.img_back['inactive'], bd=0.1,
                                     command=lambda: self.controller.show_frame('Draft'))
        self.back_button.grid(row=1, column=0, padx=5, pady=5)
        self.back_button.bind('<Enter>', lambda event: self.controller.on_enter(self.back_button, 'back'))
        self.back_button.bind('<Leave>', lambda event: self.controller.on_leave(self.back_button, 'back'))
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def _on_mousewheel(self, event):
        self.container.bind_all('<MouseWheel>', self._scroll)

    def _off_mousewheel(self, event):
        self.container.unbind_all('<MouseWheel>')

    def _scroll(self, event):
        self.container.yview_scroll(int(-1*(event.delta/120)), 'units')


class StoreHelpPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.scrollframe = tk.Frame(self)
        self.scrollframe.grid(row=0, column=0, sticky='nsew')
        self.container = tk.Canvas(self.scrollframe,
                                   scrollregion=(0, 0, 400, 1200))
        self.scrollbar = ttk.Scrollbar(self.scrollframe, orient='vertical',
                                       command=self.container.yview)
        self.container.config(yscrollcommand=self.scrollbar.set)
        self.container.bind('<Enter>', self._on_mousewheel)
        self.container.bind('<Leave>', self._off_mousewheel)
        self.scrollbar.pack(side='right', fill='y')
        self.container.pack(side='left', expand=True, fill='both')

        self.img_help = RGBAImage(os.path.join(COMMON, 'help_store.png'))
        self.help = tk.Label(self.container, image=self.img_help)
        self.container.create_window(255, 590,
                                     window=self.help)

        self.back_button = tk.Button(self, image=self.controller.img_back['inactive'], bd=0.1,
                                     command=lambda: self.controller.show_frame('Store'))
        self.back_button.grid(row=1, column=0, padx=5, pady=5)
        self.back_button.bind('<Enter>', lambda event: self.controller.on_enter(self.back_button, 'back'))
        self.back_button.bind('<Leave>', lambda event: self.controller.on_leave(self.back_button, 'back'))
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def _on_mousewheel(self, event):
        self.container.bind_all('<MouseWheel>', self._scroll)

    def _off_mousewheel(self, event):
        self.container.unbind_all('<MouseWheel>')

    def _scroll(self, event):
        self.container.yview_scroll(int(-1*(event.delta/120)), 'units')


class PullHelpPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.img_help = RGBAImage(os.path.join(COMMON, 'help_starter.png'))
        self.help_label = tk.Label(self, image=self.img_help)
        self.help_label.grid(row=0, column=0, sticky='nsew')

        self.back_button = tk.Button(self, image=self.controller.img_back['inactive'], bd=0.1, command=lambda: self.controller.show_frame('NewPull'))
        self.back_button.grid(row=1, column=0, padx=5, pady=5)
        self.back_button.bind('<Enter>', lambda event: self.controller.on_enter(self.back_button, 'back'))
        self.back_button.bind('<Leave>', lambda event: self.controller.on_leave(self.back_button, 'back'))


class NewPull(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.pkmn_list = []
        self.img_pkmn = [[], []]
        self.pkmn_buttons = []
        self.box_buttons = [[], []]
        self.box_images = [[], []]
        for i in ['A', 'B', 'C', 'D']:
            self.box_images[0].append(RGBAImage(os.path.join(COMMON, 'button_inactive_Mystery%s.png' %i)))
            self.box_images[1].append(RGBAImage(os.path.join(COMMON, 'button_active_Mystery%s.png' %i)))
        self.frames = []
        for i in range(4):
            self.frames.append(tk.Frame(self))
            self.frames[i].grid(row=i, column=0, sticky='nsew')
        self.newimg_pull = RGBAImage(os.path.join(COMMON, 'label_newpull.png'))
        self.newpull_label = tk.Label(self.frames[0], image=self.newimg_pull)
        self.newpull_label.grid(row=0, column=0, sticky='nsw')
        self.help_button = tk.Button(self.frames[0], image=self.controller.img_help['inactive'], bd=0.1,
                                     command=lambda: self.controller.show_frame('PullHelpPage'))
        self.help_button.grid(row=0, column=1)
        self.frames[0].grid_columnconfigure(0, weight=1)
        self.frames[0].grid_columnconfigure(1, weight=1)
        for row in range(2):
            for column in range(3):
                x = (row * 3) + column
                self.pkmn_buttons.append(tk.Button(self.frames[1],
                                                   image=self.controller.img_blank['inactive'],
                                                   bd=0.1, command=lambda: None))
                self.pkmn_buttons[x].grid(row=row, column=column+1, padx=10, pady=10)
                self.pkmn_buttons[x].bind('<Enter>', lambda event, x=x: self.team_on_enter(x))
                self.pkmn_buttons[x].bind('<Leave>', lambda event, x=x: self.team_on_leave(x))

        self.img_back = []
        self.button_states = ['inactive', 'active']
        for i in range(2):
            self.img_back.append(RGBAImage(os.path.join(COMMON, 'button_' + self.button_states[i] + '_finishpull.png')))
        self.back_button = tk.Button(self.frames[1], image=self.img_back[0],
                                     bd=0.1, state='disabled', command=self.back)
        self.back_button.grid(row=0, column=5, rowspan=2, sticky="nsew")
        self.box_img = RGBAImage(os.path.join(COMMON, 'label_box.png'))
        self.box_label = tk.Label(self.frames[2], image=self.box_img)
        self.box_label.grid(row=0, column=0, sticky='nsw')
        for i in range(4):
            self.box_buttons[int(i/2)].append(tk.Button(self.frames[3],
                image=self.box_images[0][i], bd=0.1,
                command=lambda i=i: self.pullbox(i)))
            self.box_buttons[int(i/2)][i%2].grid(row=int(i/2), column=i%2)
            self.box_buttons[int(i/2)][i%2].bind('<Enter>',
                lambda event, i=i: self.box_on_enter(i))
            self.box_buttons[int(i/2)][i%2].bind('<Leave>',
                lambda event, i=i: self.box_on_leave(i))

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

        self.frames[1].grid_columnconfigure(0, weight=1)
        self.frames[1].grid_columnconfigure(4, weight=1)
        self.frames[1].grid_columnconfigure(5, weight=1)
        self.frames[1].grid_columnconfigure(6, weight=1)
        for i in range(2):
            self.frames[3].grid_rowconfigure(i, weight=1)
            self.frames[3].grid_columnconfigure(i, weight=1)
        for i in [0, 1, 3]:
            self.grid_rowconfigure(i, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def get_pkmn_imgs(self, pkmn_name):
        pkmn_name = pkmn_name.replace('-Small', '').replace('-Large', '').replace('-Super', '').replace(':', '')
        self.img_pkmn_base = [RGBAImage2(os.path.join(IMG_PKMN_DIR, pkmn_name + '_inactive.png')),
                              RGBAImage2(os.path.join(IMG_PKMN_DIR, pkmn_name + '_active.png'))]
        for i in range(2):
            self.img_pkmn_base[i].paste(self.controller.img_border[get_rarity(pkmn_name)],
                                        (0, 0),
                                        self.controller.img_border[get_rarity(pkmn_name)])
        for i in range(2):
            self.img_pkmn[i].append(ImageTk.PhotoImage(self.img_pkmn_base[i]))

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
        self.back_button.config(image=self.img_back[1], state='normal')

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
                    self.img_pkmn_base[i].paste(
                        self.controller.img_border[get_rarity(name)],
                        (0, 0),
                        self.controller.img_border[get_rarity(name)])
                for i in range(2):
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
        self.back_button.config(image=self.img_back[0], state='disabled')

    def back(self):
        PLAYERS[-1].pkmn_list = self.pkmn_list
        filename = PLAYERS[-1].name + '.csv'
        with open(os.path.join(PLAYER_DIR, filename), 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            for pkmn in PLAYERS[-1].pkmn_list:
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
        update_all_optionmenus(self.controller)
        for key, button in self.controller.sidebar.buttons.items():
            button.config(state='normal')
        self.controller.show_frame('Players')

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


def update_all_optionmenus(self):
    menu1 = self.pages['Store'].player_option['menu']
    menu2 = self.pages['Players'].player_option['menu']
    menu3 = self.pages['DraftSettings'].player_option[0]['menu']
    menu4 = self.pages['DraftSettings'].player_option[1]['menu']
    menu5 = self.pages['RandomSettings'].player_option[0]['menu']
    menu6 = self.pages['RandomSettings'].player_option[1]['menu']
    menu1.delete(0, 'end')
    menu2.delete(0, 'end')
    menu3.delete(0, 'end')
    menu4.delete(0, 'end')
    menu5.delete(0, 'end')
    menu6.delete(0, 'end')
    for player in playerNames:
        menu1.add_command(label=player,
            command=lambda player=player: self.pages['Store'].switch_player(player))
        menu2.add_command(label=player,
            command=lambda player=player: self.pages['Players'].display_pkmn(player))
        menu3.add_command(label=player,
            command=lambda player=player: self.pages['Draft'].current_player[0].set(player))
        menu4.add_command(label=player,
            command=lambda player=player: self.pages['Draft'].current_player[1].set(player))
        menu5.add_command(label=player,
            command=lambda player=player: self.pages['Random'].current_player[0].set(player))
        menu6.add_command(label=player,
            command=lambda player=player: self.pages['Random'].current_player[1].set(player))


def get_true_name(name):
    return name.replace('-Mega-X', '').replace('-Mega-Y', '').replace('-Ash', '').replace('-Mega', '')


def get_mega_name(pkmn):
    if ((pkmn.item != 'Eviolite' and (pkmn.item.endswith('ite')) or
        'Dragon Ascent' in pkmn.moves)):
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
        if name.endswith('-Mega') or name.endswith('Mega-Y') or name.endswith('Mega-X'):
            temp_name = name.replace('-Mega-Y', '').replace('-Mega-X', '').replace('-Mega', '')
            if pkmn.name == temp_name:
                if (pkmn.item.endswith('ite') or pkmn.item.endswith('ite X') or
                    pkmn.item.endswith('ite Y')):
                    rarity = pkmn.rarity
                    break
        elif name.endswith('-Ash'):
            temp_name = name.replace('-Ash', '')
            if pkmn.name == temp_name:
                if pkmn.ability == 'Battle Bond':
                    rarity = pkmn.rarity
                    break
        else:
            temp_name = name
            if pkmn.name == temp_name:
                if pkmn.item == 'Eviolite':
                    rarity = pkmn.rarity
                    break
                if not (pkmn.item.endswith('ite') or pkmn.item.endswith('ite X') or
                    pkmn.item.endswith('ite Y')):
                    rarity = pkmn.rarity
                    break
    return rarity


def check_validity(self, pkmn, team=0):
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
    popup_message(self.controller,
                  'INFO',
                  'Copied all sets to clipboard.')


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
    file = os.path.join(DATA, 'Singles_copy.csv')
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
            self.parent_page().pool_buttons[i].config(command=lambda: None)
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

    self.separators[5].grid(row=19, column=0, columnspan=6, sticky='nsew')

    self.usage_text = tk.Label(self, text='Usage')
    self.usage_text.grid(row=20, column=0, sticky='w')

    self.separators[6].grid(row=21, column=0, columnspan=6, sticky='nsew')
    self.img_back = []
    for i in ['inactive', 'active']:
        self.img_back.append(RGBAImage(os.path.join(COMMON, 'button_%s_back.png' %i)))
    self.back_button = tk.Button(self, image=self.img_back[0], bd=0.1,
                                 command=lambda: validate(self, page))
    self.back_button.grid(row=22, column=1, columnspan=4, padx=5, pady=5,
                          sticky='nsew')
    self.back_button.bind('<Enter>', lambda event: self.controller.on_enter(self.back_button, 'back'))
    self.back_button.bind('<Leave>', lambda event: self.controller.on_leave(self.back_button, 'back'))
    for i in range(22):
        self.grid_rowconfigure(i, weight=1)


def setup_game_settings(self, page):
    self.rules_img = RGBAImage(os.path.join(COMMON, 'label_rules.png'))
    self.rules_label = tk.Label(self, image=self.rules_img)
    self.rules_label.grid(row=0, column=0, columnspan=4, sticky='nsw')
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
                value=draft_modes[i],
                command=self.change_draft_mode))
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
                value=themes[i],
                command=self.update_gen_settings))
            self.theme_buttons[i].grid(row=2+int(i/5), column=(i % 5)+1, padx=5,
                                       pady=5, sticky='nsew')
        self.type_option = []
        for i in range(2):
            self.type_option.append(tk.OptionMenu(self, self.parent_page().type[i],
                                                  *TYPES))
            self.type_option[i].grid(row=7, column=i*2, columnspan=2, padx=5, pady=5, sticky='ew')
            self.type_option[i].grid_remove()

    self.mega_text = tk.Label(self, text='Show Megas')
    if page == 'Draft':
        self.mega_text.grid(row=4, column=0, padx=5, pady=5, sticky='w')
    else:
        self.mega_text.grid(row=3, column=0, padx=5, pady=5, sticky='w')
    self.mega_buttons = []
    megas = ['No', 'Yes']
    for i in range(len(megas)):
        self.mega_buttons.append(tk.Radiobutton(self,
            text=megas[i],
            variable=self.parent_page().show_megas,
            indicatoron=0,
            value=megas[i],
            command=self.parent_page().replace_images))
        if page == 'Draft':
            self.mega_buttons[i].grid(row=4 + int(i/5), column=(i % 5) + 1,
                                      padx=5, pady=5, sticky='nsew')
        else:
            self.mega_buttons[i].grid(row=3 + int(i/5), column=(i % 5) + 1,
                                      padx=5, pady=5, sticky='nsew')

    self.hidden_text = tk.Label(self, text='Hide Pokemon')
    if page == 'Draft':
        self.hidden_text.grid(row=5, column=0, padx=5, pady=5, sticky='w')
    else:
        self.hidden_text.grid(row=4, column=0, padx=5, pady=5, sticky='w')
    self.hidden_buttons = []
    hidden = ['No', 'Yes']
    for i in range(len(hidden)):
        self.hidden_buttons.append(tk.Radiobutton(self,
            text=hidden[i],
            variable=self.parent_page().hidden,
            indicatoron=0,
            value=hidden[i]))
        if page == 'Draft':
            self.hidden_buttons[i].grid(row=5 + int(i/5), column=(i % 5) + 1,
                                        padx=5, pady=5, sticky='nsew')
        else:
            self.hidden_buttons[i].grid(row=4 + int(i/5), column=(i % 5) + 1,
                                        padx=5, pady=5, sticky='nsew')

    self.player_option = []
    for i in range(2):
        self.player_option.append(tk.OptionMenu(self, self.parent_page().current_player[i],
                                                *playerNames))
        self.player_option[i].grid(row=6, column=i*2, columnspan=2, padx=5, pady=5, sticky='ew')
        self.player_option[i].grid_remove()

    self.back_button = tk.Button(self, image=self.controller.img_back['inactive'], bd=0.1,
                                 command=lambda page=page: exit(self, page))
    self.back_button.grid(row=9, column=1, columnspan=2,
                          padx=5, pady=5, sticky='nsew')
    self.back_button.bind('<Enter>', lambda event: self.controller.on_enter(self.back_button, 'back'))
    self.back_button.bind('<Leave>', lambda event: self.controller.on_leave(self.back_button, 'back'))

    for i in range(6):
        self.grid_rowconfigure(i, weight=1)
    for i in range(4):
        self.grid_columnconfigure(i, weight=1)


def exit(self, page):
    if self.parent_page().current_player[0].get():
        list1 = len(PLAYERS[playerNames.index(self.parent_page().current_player[0].get())].pkmn_list)
    else:
        list1 = 0
    if self.parent_page().current_player[1].get():
        list2 = len(PLAYERS[playerNames.index(self.parent_page().current_player[1].get())].pkmn_list)
    else:
        list2 = 0
    list_total = list1+list2
    if (self.parent_page().battle_mode.get() == 'SRL' and
        self.parent_page().current_player[0].get() == self.parent_page().current_player[1].get()):
        popup_message(self.controller,
                      'ERROR',
                      'Player 1 and Player 2 cannot be the same person.',
                      text2='\nPlease choose another person for Player 1 or 2.')
    elif (self.parent_page().battle_mode.get() == 'SRL' and list_total < 18 and
          page == 'Draft'):
        popup_message(self.controller,
                      'ERROR',
                      'Not enough Pokemon required to Draft (18 needed).')
    elif (self.parent_page().battle_mode.get() == 'SRL' and
          (list1 < 12 or list2 < 12) and
          page == 'Random'):
        popup_message(self.controller,
                      'ERROR',
                      'Not enough Pokemon required for Random (12 needed per player).')
    else:
        self.parent_page().replace_images()
        self.controller.show_frame(page)



def RGBAImage(path):
    return ImageTk.PhotoImage(Image.open(path).convert('RGBA'))


def RGBAImage2(path):
    return Image.open(path).convert('RGBA')


class Player:
    def __init__(self, name, pkmn_list):
        self.name = name
        self.pkmn_list = pkmn_list


def init_player_information():
    if not os.path.isdir(PLAYER_DIR):
        os.mkdir(PLAYER_DIR)
    if not os.listdir(PLAYER_DIR):
        with open(os.path.join(PLAYER_DIR, 'Virgo.csv'), 'w') as file:
            pass
    for filename in os.listdir(PLAYER_DIR):
        if filename.endswith('.csv'):
            with open(os.path.join(PLAYER_DIR, filename), 'r', encoding='utf-8') as file:
                player_name = os.path.splitext(os.path.basename(file.name))[0]
                reader = csv.reader(file)
                temp_pkmn_list = []
                for row in reader:
                    if row:
                        temp_pkmn_list.append(Pokemon(row))
                PLAYERS.append(Player(player_name, temp_pkmn_list))
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


if __name__ == '__main__':
    # global variables
    VERSION = '2.2.0'
    ROOT = os.path.dirname(os.path.realpath(__file__))
    COMMON = os.path.join(ROOT, 'media', 'Common')
    IMG_PKMN_DIR = os.path.join(ROOT, 'media', 'pokemon')
    PLAYER_DIR = os.path.join(ROOT, 'players')
    DATA = os.path.join(ROOT, 'data')
    month = int(date.today().strftime('%m'))
    day = int(date.today().strftime('%d'))

    # before starting the GUI, gather any player info
    init_player_information()
    app = MainApp()

    # disable resizing of window
    app.resizable(False, False)

    # set the title of the window (and top-level windows)
    app.title('Rentals v%s' %VERSION)
    app.mainloop()
