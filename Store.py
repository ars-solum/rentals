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

    # create buttons on canvas
    self.pkmn_buttons = [[None for i in range(5)] for j in range(8)]
    self.pkmn_buttons.append([None for i in range(4)])
    for i in range(9):
        for j in range(len(self.pkmn_buttons[i])):
            x = (i * 5) + j
            self.pkmn_buttons[i][j] = tk.Button(self.container, image=self.img_pkmn[self.current_page][0][x], bd=0.1)
            # place the buttons on the canvas
            self.container.create_window((j*100)+50, (i*70)+30, window=self.pkmn_buttons[i][j])

def _on_mousewheel(self, event):
    self.container.bind_all('<MouseWheel>', self._scroll)

def _off_mousewheel(self, event):
    self.container.unbind_all('<MouseWheel>')

def _scroll(self, event):
    self.container.yview_scroll(int(-1*(event.delta/120)), 'units')


def banner_popup(self, event):
    # popup menu
    self.rclick_menu = tk.Menu(self, tearoff=0)
    self.rclick_menu.add_command(label='Banner Settings', command=lambda: self.controller.change_page('StoreSettings'))
    try:
        self.rclick_menu.tk_popup(event.x_root+50, event.y_root+10, 0)
    finally:
        self.rclick_menu.grab_release()

def popup(self, event, index):
    # popup menu
    pkmn_name = ALL_BANNERS[self.banner_num+self.current_page][index]
    self.rclick_menu = tk.Menu(self, tearoff=0)
    self.rclick_menu.add_command(label='View Sets', command=lambda pkmn_name=pkmn_name: self.view_more_details(pkmn_name))
    try:
        self.rclick_menu.tk_popup(event.x_root+40, event.y_root+10, 0)
    finally:
        self.rclick_menu.grab_release()
