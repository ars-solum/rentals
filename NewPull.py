from Pokemon import *

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
