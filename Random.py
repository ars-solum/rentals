from Pokemon import *

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
