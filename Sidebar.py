try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk
import os
from PIL import Image, ImageTk
from RGBAImage import RGBAImage
from Pokemon import Pokemon, ALL_POKEMON, ABILITIES , TypeChart, type_logic

ROOT = os.path.dirname(os.path.realpath(__file__))

SIDEBAR_OPTIONS = ['Draft', 'Random',
                   'GeneralSettings', 'AdvancedSettings',
                   'Trainers', 'Auctions', 'Leaderboards', 'Prizes']

class Sidebar(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # private variables
        self.currPageSelected = 'Draft'
        self.prevPageSelected = None

        self.grid_columnconfigure(1, weight=1)

        # labels
        self.label_text = ['battle', 'settings', 'league']
        self.img_labels = []
        for i in range(len(self.label_text)):
            self.img_labels.append(RGBAImage(os.path.join(ROOT, 'media', 'Common', 'label_%s.png' % self.label_text[i])))

        # buttons
        # [1] active [2] inactive
        self.img_buttons = [[], []]
        self.button_states = ['active', 'inactive']
        self.buttons = []
        for i in range(len(self.button_states)):
            for j in range(len(SIDEBAR_OPTIONS)):
                self.img_buttons[i].append(RGBAImage(os.path.join(ROOT, 'media', 'Common', 'button_%s_%s.png' %(self.button_states[i], SIDEBAR_OPTIONS[j]))))
                if 0 == i and 0 == j:
                    self.b_buttons.append(tk.Button(self, image=self.img_buttons[0][0], bd=0.1, command=lambda: self.controller.show_frame(SIDEBAR_OPTIONS[0])))
                if 1 == i and j > 0:
                    self.b_buttons.append(tk.Button(self, image=self.img_buttons[i][j], bd=0.1, command=lambda i=i, j=j: self.controller.show_frame(SIDEBAR_OPTIONS[i*2+j])))

            self.b_battleOptions[i].grid(row=i+1, column=0)
            self.b_battleOptions[i].bind("<Enter>", lambda event, i=i: self.on_enter(i))
            self.b_battleOptions[i].bind("<Leave>", lambda event, i=i: self.on_leave(i))

        self.l_auctionModes = tk.Label(self.f_menuOptions[1], image=self.img_auctionModes)
        self.l_auctionModes.grid(row=0, column=0, pady=(20, 5))

        self.b_auctionOptions = []
        for i in range(len(AUCTION_OPTIONS)):
            self.img_selected_button.append(ImageTk.PhotoImage(RGBAImage('media\\Common\\button_selected_{0}.png'.format(AUCTION_OPTIONS[i]))))
            self.img_inactive_button.append(ImageTk.PhotoImage(RGBAImage('media\\Common\\button_inactive_{0}.png'.format(AUCTION_OPTIONS[i]))))

            self.b_auctionOptions.append(tk.Button(self.f_menuOptions[1], image=self.img_inactive_button[i+len(BATTLE_OPTIONS)], bd=0.1,
                                                command=lambda i=i: controller.show_frame(AUCTION_OPTIONS[i])))
            self.b_auctionOptions[i].grid(row=i+1, column=0)
            self.b_auctionOptions[i].bind("<Enter>", lambda event, i=i: self.on_enter(i+4))
            self.b_auctionOptions[i].bind("<Leave>", lambda event, i=i: self.on_leave(i+4))

    def on_enter(self, option):
        if option < 4:
            if self.currPageSelected == BATTLE_OPTIONS[option]:
                pass
            else:
                self.b_battleOptions[option].config(image=self.img_selected_button[option])
        else:
            if self.currPageSelected == AUCTION_OPTIONS[option-4]:
                pass
            else:
                self.b_auctionOptions[option-4].config(image=self.img_selected_button[option])

    def on_leave(self, option):
        if option < 4:
            if self.currPageSelected == BATTLE_OPTIONS[option]:
                self.b_battleOptions[option].config(image=self.img_selected_button[option])
            else:
                self.b_battleOptions[option].config(image=self.img_inactive_button[option])
        else:
            if self.currPageSelected == AUCTION_OPTIONS[option-4]:
                self.b_auctionOptions[option-4].config(image=self.img_selected_button[option])
            else:
                self.b_auctionOptions[option-4].config(image=self.img_inactive_button[option])

    def set_selected(self, mode):
        self.prevPageSelected = self.currPageSelected
        self.currPageSelected = mode

    def get_currSelected(self):
        return self.currPageSelected

    def get_prevSelected(self):
        return self.prevPageSelected

    def update_media(self):
        if self.currPageSelected != self.prevPageSelected:
            for i in range(4):
                if self.prevPageSelected == BATTLE_OPTIONS[i]:
                    self.b_battleOptions[i].config(image=self.img_inactive_button[i])
                    break
                if self.prevPageSelected == AUCTION_OPTIONS[i]:
                    self.b_auctionOptions[i].config(image=self.img_inactive_button[i+4])
                    break
        else:
            for i in range(4):
                if self.currPageSelected == BATTLE_OPTIONS[i]:
                    self.b_battleOptions[i].config(image=self.img_selected_button[i])
                    break
                if self.currPageSelected == AUCTION_OPTIONS[i]:
                    self.b_auctionOptions[i].config(image=self.img_selected_button[i+4])
                    break
