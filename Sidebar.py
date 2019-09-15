import tkinter as tk

from Pokemon import *

class Sidebar(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        for i in range(3):
            self.grid_rowconfigure(i, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # section | buttons
        self.text = {
            'battle': ['Draft', 'Random'],
            'league': ['Players', 'Store'],
            'settings': ['game_settings', 'pkmn_settings', 'Game', 'Sets']
        }

        self.frame_section = {}
        self.label_section = {}
        self.buttons = {}
        self.img_buttons = {}
        self.img_labels = {}

        # initialize images
        for section in self.text:
            self.img_labels[section] = RGBAImage(os.path.join(COMMON, '%s.png' %section))
        for section in self.text:
            for item in self.text[section]:
                self.img_buttons[item] = {}
        for key in self.img_buttons:
            for state in ['active', 'inactive']:
                self.img_buttons[key][state] = RGBAImage(os.path.join(COMMON, 'button_%s_%s.png' % (state, key)))
        self.empty_space = RGBAImage(os.path.join(COMMON, '3_empty_buttons.png'))

        tmp_ctr = 0 # keep track of which row to place the current section

        # construct each section
        for section in self.text:
            # special case: 3rd section should fill up space
            if tmp_ctr == 2:
                self.empty_space_label = tk.Label(self, image=self.empty_space)
                self.empty_space_label.grid(row=tmp_ctr, column=0, sticky='nsew')
                tmp_ctr += 1

            # initialize section frames
            self.frame_section[section] = tk.Frame(self)
            self.frame_section[section].grid(row=tmp_ctr, column=0, sticky='nsew')

            # initialize section labels
            self.label_section[section] = tk.Label(self.frame_section[section], image=self.img_labels[section])
            self.label_section[section].grid(row=0, column=0, sticky='nsew')

            # initialize the current section's buttons
            for button in self.text[section]: # button = Draft, etc.
                self.buttons[button] = tk.Button(self.frame_section[section], image=self.img_buttons[button]['active' if (button == 'Draft') else 'inactive'], bd=0.1)
                row = self.text[section].index(button) + 1 # skip over the first row for section title
                self.buttons[button].grid(row=row, column=0, sticky='nsew')
                self.buttons[button].bind('<Enter>', lambda event, button=button: self.controller.on_enter(self.buttons[button], self.img_buttons[button]['active']))
                self.buttons[button].bind('<Leave>', lambda event, button=button: self.controller.on_leave(self.buttons[button], self.img_buttons[button]['inactive']))

            tmp_ctr += 1

        # assign each button's command
        for section in self.text:
            if section == 'settings':
                self.buttons['game_settings'].config(command=lambda: self.controller.change_page('DraftSettings'))
                self.buttons['pkmn_settings'].config(command=lambda: self.controller.change_page('DraftGenerateSettings'))
            else:
                for button in self.text[section]:
                    self.buttons[button].config(command=lambda button=button: self.controller.change_page(button))
