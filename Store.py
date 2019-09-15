from Pokemon import *

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
