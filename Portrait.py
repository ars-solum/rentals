from Pokemon import *

TRAINERS = os.path.join(ROOT, 'media', 'trainers')

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
