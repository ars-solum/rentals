try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk
from PIL import Image, ImageTk

import os
import csv
import time
import random
from random import shuffle

from RGBAImage import RGBAImage
from TypeChart import TypeChart, type_logic
from Pokemon import Pokemon, ALL_POKEMON, ABILITIES
from Sidebar import Sidebar

from Battle import Battle

BATTLE_OPTIONS = ["StandardDraft", "RandomBattle", "NemesisDraft", "BanDraft"]
AUCTION_OPTIONS = ["Trainers", "Auctions", "Leaderboards", "Prizes"]
IMGTYPE = ["inactive", "active", "picked", "banned", "unknown"]

class MainApp(tk.Tk):
    ############################################
    ##### constructor/initializer function #####
    ############################################
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # initialize private variables
        f_buttonsidebar = tk.Frame(self)
        f_buttonsidebar.grid(row=0, column=0, sticky="nsew")

        self.sidebar = Sidebar(parent=f_buttonsidebar, controller=self)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        f_container = tk.Frame(self)
        f_container.grid(row=0, column=1, rowspan=5, sticky="nsew")
        f_container.grid_rowconfigure(0, weight=1)
        f_container.grid_columnconfigure(0, weight=1)

        self.containerFrames = {}

        ######################################
        ##### initialize each menu layer #####
        ######################################
        for i in range(4):
            page_name = BATTLE_OPTIONS[i]
            frame = Battle(parent=f_container, controller=self, mode=page_name)
            self.containerFrames[page_name] = frame
            frame.grid(row=0, column=1, rowspan=4, sticky="nsew")

        for F in (Trainers, Auctions, Leaderboards, Prizes):
            page_name = F.__name__
            frame = F(parent=f_container, controller=self)
            self.containerFrames[page_name] = frame
            frame.grid(row=0, column=1, rowspan=4, sticky="nsew")

        self.show_frame("StandardDraft")
        self.sidebar.set_selected("StandardDraft")

    ########################################
    ##### menu layer changing function #####
    ########################################
    def show_frame(self, page_name):
        self.sidebar.set_selected(page_name)
        self.sidebar.update_media()
        frame = self.containerFrames[page_name]
        frame.tkraise()

class Trainers(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.alpha = 0.0
        self.img_pokemon = []
        self.img_pokemon.append(RGBAImage("media\\Squirtle_inactive.png"))
        self.img_pokemon.append(RGBAImage("media\\Squirtle_active.png"))
        self.img_pokemon.append(RGBAImage("media\\Squirtle_banned.png"))
        self.img_pokemon.append(RGBAImage("media\\Squirtle_unknown.png"))
        self.img_pokemon.append(RGBAImage("media\\Squirtle_picked.png"))
        self.img_border = RGBAImage("media\\border_StandardDraft.png")
        for i in range(5):
            self.img_pokemon[i].paste(self.img_border, (0, 0), self.img_border)

        self.img_pokemonFull = []
        for i in range(5):
            self.img_pokemonFull.append(ImageTk.PhotoImage(self.img_pokemon[i]))

        self.labels = []
        for i in range(5):
            self.labels.append(tk.Label(self, image=self.img_pokemonFull[i]))
            self.labels[i].grid(row=0, column=i, sticky="nsew")

        self.label1 = tk.Button(self, image=self.img_pokemonFull[0], bd=0.1, command=lambda:self.pick())
        self.label1.grid(row=0, column=6, sticky="nsew")

    def pick(self):
        if self.alpha > 1.0:
            return
        self.new_img = ImageTk.PhotoImage(Image.blend(self.img_pokemon[0], self.img_pokemon[2], self.alpha))
        self.alpha = self.alpha + 0.1
        self.label1.config(image=self.new_img)
        self.after(10, self.pick)

class Auctions(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

class Leaderboards(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

class Prizes(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

class TEST:
    def __init__(self, canvas, x1, y1, x2, y2, player):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.player = player
        self.img_trainer = []
        self.img_turn = []
        self.img_trainer.append(ImageTk.PhotoImage(RGBAImage('media\\Common\\trainer{0}.png'.format(self.player))))
        self.img_trainer.append(ImageTk.PhotoImage(RGBAImage('media\\Common\\trainer{0}fast.png'.format(self.player))))
        self.img_turn.append(ImageTk.PhotoImage(RGBAImage('media\\Common\\turn{0}.png'.format(self.player))))
        self.img_turn.append(ImageTk.PhotoImage(RGBAImage('media\\Common\\turn{0}fast.png'.format(self.player))))

    def move_turns(self, direction):
        if direction == "Left":
            pass

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    #random.seed(time.strftime("%Y-%m-%d"))
    app = MainApp()
    app.mainloop()
