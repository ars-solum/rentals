from Pokemon import *

class NewPullHelpPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # create help image
        self.img_help = RGBAImage(os.path.join(COMMON, 'help_starter.png'))
        self.help_label = tk.Label(self, image=self.img_help)
        self.help_label.grid(row=0, column=0, sticky='nsew')

        # back button
        self.back_button = tk.Button(self, image=self.controller.img_back['inactive'], bd=0.1, command=lambda: self.controller.change_page('NewPull'))
        self.back_button.grid(row=1, column=0, padx=5, pady=5)
        self.back_button.bind('<Enter>', lambda event: self.controller.on_enter(self.back_button, self.controller.img_back['active']))
        self.back_button.bind('<Leave>', lambda event: self.controller.on_leave(self.back_button, self.controller.img_back['inactive']))
