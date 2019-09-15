from Pokemon import *
from Sidebar import *
from Draft import *
from Random import *
from DraftSettings import *
from DraftGenerateSettings import *
from RandomSettings import *
from RandomGenerateSettings import *
from Store import *
from StoreSettings import *
from Players import *
from StoreHelpPage import *
from NewPull import *
from NewPullHelpPage import *
from Portrait import *
from Details import *

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
