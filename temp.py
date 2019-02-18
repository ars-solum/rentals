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


from Pokemon import *


DEBUG = True
def debug(message=None):
    if DEBUG:
        if message:
            print(message)
        else:
            print()

ROOT = os.path.dirname(os.path.realpath(__file__))

class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.side_frame = tk.Frame(self)
        self.side_frame.grid(row=0, column=0, sticky="nsew")

        self.main_frame = tk.Frame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew")

        self.sidebar = Sidebar(parent=self.side_frame, controller=self)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        self.pages = {}

        for Class in (Draft, Random, Banners):
            page_name = Class.__name__
            frame = Class(parent=self.main_frame, controller=self)
            self.pages[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame('Draft')

        self.side_frame.grid_rowconfigure(0, weight=1)
        self.side_frame.grid_columnconfigure(0, weight=1)

    def show_frame(self, page_name):
        frame = self.pages[page_name]
        frame.tkraise()

###############################################################################
class Sidebar(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.label_text = ['Battle', 'League']
        self.labels = []
        self.button_text = [['Draft', 'Random'], ['Banners']] # remove after getting images
        self.button_states = ['active', 'inactive']
        self.buttons = []

        self.section_frames = []
        self.tmp_counter = 0
        for i in range(len(self.label_text)):
            self.section_frames.append(tk.Frame(self))
            self.section_frames[i].grid(row=i, column=0, sticky="nsew")
            self.labels.append(tk.Label(self.section_frames[i], text=self.label_text[i], justify="center"))
            self.labels[i].grid(row=0, column=0, sticky="nsew")
            for j in range(len(self.button_text[i])):
                self.buttons.append(tk.Button(self.section_frames[i], text=self.button_text[i][j], command=lambda i=i, j=j: self.controller.show_frame(self.button_text[i][j])))
                self.buttons[self.tmp_counter].grid(row=j+1, column=0, sticky="nsew")
                self.tmp_counter += 1
###############################################################################

###############################################################################
class Draft(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.alpha = 0
        self.turn = 0
        self.game_activated = False
        self.pokemonNotPicked = [True for i in range(18)]

        ##### Pool Pokemon #####
        self.pool_buttons = []
        for i in range(3):
            for j in range(6):
                x = (i*6) + j
                self.pool_buttons.append(tk.Button(self, text="???", command=None))
                self.pool_buttons[x].grid(row=i, column=j, padx=5, pady=5)
        ##### Pool Pokemon #####

        ##### Ban Boxes #####
        self.bans = [[], []]
        self.ban_text = tk.Label(self, text="BANS")
        self.ban_text.grid(row=4, column=2, columnspan=2, sticky="nsew")
        self.ban_buttons = [[], []]
        for i in range(2):
            for j in range(2):
                self.ban_buttons[i].append(tk.Button(self, text="???", command=None))
                self.ban_buttons[i][j].grid(row=4, column=i*4+j, padx=5, pady=5, sticky="nsew")
        ##### Ban Boxes #####

        ##### Team Boxes #####
        self.team_text = []
        self.team_list = [[None for i in range(6)] for j in range(2)]
        self.team_buttons = [[], []]
        for team in range(2):
            self.team_text.append(tk.Label(self, text="TEAM %s" % str(team+1)))
            self.team_text[team].grid(row=5, column=team*4, columnspan=2, sticky="nsew")
            for row in range(3):
                for column in range(2):
                    x = (row * 2) + column
                    self.team_buttons[team].append(tk.Button(self, text="???", command=None))
                    self.team_buttons[team][x].grid(row=row+6, column=(team*4)+column, padx=5, pady=5, sticky="nsew")
        ##### Team Boxes #####

        ##### Settings #####
        self.settingsV1 = tk.Button(self, text="Draft Settings", command=None)
        self.settingsV1.grid(row=6, column=2, columnspan=2, padx=5, pady=5, sticky="nsew")
        self.settingsV2 = tk.Button(self, text="Pokemon Settings", command=None)
        self.settingsV2.grid(row=7, column=2, columnspan=2, padx=5, pady=5, sticky="nsew")


###############################################################################



###############################################################################
class Random(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
###############################################################################

###############################################################################
class Banners(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
###############################################################################

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
