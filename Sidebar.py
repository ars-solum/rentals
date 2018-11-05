try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk
from PIL import Image, ImageTk
from RGBAImage import RGBAImage

from Pokemon import Pokemon, ALL_POKEMON, ABILITIES , TypeChart, type_logic

BATTLE_OPTIONS = ["StandardDraft", "RandomBattle", "NemesisDraft", "BanDraft"]
AUCTION_OPTIONS = ["Trainers", "Auctions", "Leaderboards", "Prizes"]
IMGTYPE = ["inactive", "active", "picked", "banned", "unknown"]

class Sidebar(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # initialize private variables
        self.currSelected = None
        self.prevSelected = None

        self.img_battleModes = ImageTk.PhotoImage(RGBAImage('media\\Common\\label_battle.png'))
        self.img_auctionModes = ImageTk.PhotoImage(RGBAImage('media\\Common\\label_auction.png'))

        # set up the menu buttons and images
        self.f_menuOptions = []
        for i in range(2):
            self.f_menuOptions.append(tk.Frame(self))
            self.f_menuOptions[i].grid(row=i, column=0, sticky="nsew")

        self.l_battleModes = tk.Label(self.f_menuOptions[0], image=self.img_battleModes)
        self.l_battleModes.grid(row=0, column=0, pady=5)

        self.img_selected_button = []
        self.img_inactive_button = []
        self.b_battleOptions = []
        for i in range(4):
            self.img_selected_button.append(ImageTk.PhotoImage(RGBAImage('media\\Common\\button_selected_{0}.png'.format(BATTLE_OPTIONS[i]))))
            self.img_inactive_button.append(ImageTk.PhotoImage(RGBAImage('media\\Common\\button_inactive_{0}.png'.format(BATTLE_OPTIONS[i]))))

            if i == 0:
                self.b_battleOptions.append(tk.Button(self.f_menuOptions[0], image=self.img_selected_button[i], bd=0.1,
                                                        command=lambda i=i: controller.show_frame(BATTLE_OPTIONS[i])))
                self.currSelected = BATTLE_OPTIONS[i]
            else:
                self.b_battleOptions.append(tk.Button(self.f_menuOptions[0], image=self.img_inactive_button[i], bd=0.1,
                                                        command=lambda i=i: controller.show_frame(BATTLE_OPTIONS[i])))
            self.b_battleOptions[i].grid(row=i+1, column=0)
            self.b_battleOptions[i].bind("<Enter>", lambda event, i=i: self.on_enter(i))
            self.b_battleOptions[i].bind("<Leave>", lambda event, i=i: self.on_leave(i))

        self.l_auctionModes = tk.Label(self.f_menuOptions[1], image=self.img_auctionModes)
        self.l_auctionModes.grid(row=0, column=0, pady=(20, 5))

        self.b_auctionOptions = []
        for i in range(4):
            self.img_selected_button.append(ImageTk.PhotoImage(RGBAImage('media\\Common\\button_selected_{0}.png'.format(AUCTION_OPTIONS[i]))))
            self.img_inactive_button.append(ImageTk.PhotoImage(RGBAImage('media\\Common\\button_inactive_{0}.png'.format(AUCTION_OPTIONS[i]))))

            self.b_auctionOptions.append(tk.Button(self.f_menuOptions[1], image=self.img_inactive_button[i+4], bd=0.1,
                                                command=lambda i=i: controller.show_frame(AUCTION_OPTIONS[i])))
            self.b_auctionOptions[i].grid(row=i+1, column=0)
            self.b_auctionOptions[i].bind("<Enter>", lambda event, i=i: self.on_enter(i+4))
            self.b_auctionOptions[i].bind("<Leave>", lambda event, i=i: self.on_leave(i+4))

    def on_enter(self, option):
        if option < 4:
            if self.currSelected == BATTLE_OPTIONS[option]:
                pass
            else:
                self.b_battleOptions[option].config(image=self.img_selected_button[option])
        else:
            if self.currSelected == AUCTION_OPTIONS[option-4]:
                pass
            else:
                self.b_auctionOptions[option-4].config(image=self.img_selected_button[option])

    def on_leave(self, option):
        if option < 4:
            if self.currSelected == BATTLE_OPTIONS[option]:
                self.b_battleOptions[option].config(image=self.img_selected_button[option])
            else:
                self.b_battleOptions[option].config(image=self.img_inactive_button[option])
        else:
            if self.currSelected == AUCTION_OPTIONS[option-4]:
                self.b_auctionOptions[option-4].config(image=self.img_selected_button[option])
            else:
                self.b_auctionOptions[option-4].config(image=self.img_inactive_button[option])

    def set_selected(self, mode):
        self.prevSelected = self.currSelected
        self.currSelected = mode

    def get_currSelected(self):
        return self.currSelected

    def get_prevSelected(self):
        return self.prevSelected

    def update_media(self):
        if self.currSelected != self.prevSelected:
            for i in range(4):
                if self.prevSelected == BATTLE_OPTIONS[i]:
                    self.b_battleOptions[i].config(image=self.img_inactive_button[i])
                    break
                if self.prevSelected == AUCTION_OPTIONS[i]:
                    self.b_auctionOptions[i].config(image=self.img_inactive_button[i+4])
                    break
        else:
            for i in range(4):
                if self.currSelected == BATTLE_OPTIONS[i]:
                    self.b_battleOptions[i].config(image=self.img_selected_button[i])
                    break
                if self.currSelected == AUCTION_OPTIONS[i]:
                    self.b_auctionOptions[i].config(image=self.img_selected_button[i+4])
                    break
