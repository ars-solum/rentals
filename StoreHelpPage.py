from Pokemon import *

class StoreHelpPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # create canvas
        self.scrollframe = tk.Frame(self)
        self.scrollframe.grid(row=0, column=0, sticky='nsew')
        self.container = tk.Canvas(self.scrollframe, scrollregion=(0, 0, 400, 1200))
        self.scrollbar = ttk.Scrollbar(self.scrollframe, orient='vertical', command=self.container.yview)
        self.container.config(yscrollcommand=self.scrollbar.set)
        self.container.bind('<Enter>', self._on_mousewheel)
        self.container.bind('<Leave>', self._off_mousewheel)
        self.scrollbar.pack(side='right', fill='y')
        self.container.pack(side='left', expand=True, fill='both')

        # create help image
        self.img_help = RGBAImage(os.path.join(COMMON, 'help_store.png'))
        self.help = tk.Label(self.container, image=self.img_help)
        self.container.create_window(255, 590, window=self.help)

        # back button
        self.back_button = tk.Button(self, image=self.controller.img_back['inactive'], bd=0.1, command=lambda: self.controller.change_page('Store'))
        self.back_button.grid(row=1, column=0, padx=5, pady=5)
        self.back_button.bind('<Enter>', lambda event: self.controller.on_enter(self.back_button, self.controller.img_back['active']))
        self.back_button.bind('<Leave>', lambda event: self.controller.on_leave(self.back_button, self.controller.img_back['inactive']))

    def _on_mousewheel(self, event):
        self.container.bind_all('<MouseWheel>', self._scroll)

    def _off_mousewheel(self, event):
        self.container.unbind_all('<MouseWheel>')

    def _scroll(self, event):
        self.container.yview_scroll(int(-1*(event.delta/120)), 'units')
