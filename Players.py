from Pokemon import *

TRAINERS = os.path.join(ROOT, 'media', 'trainers')

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
