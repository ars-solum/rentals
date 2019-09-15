from Pokemon import *

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
