from Pokemon import *

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
