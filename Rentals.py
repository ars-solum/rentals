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

from Pokemon import *
from Sidebar import Sidebar

from Battle import Battle

BATTLE_OPTIONS = ["StandardDraft", "RandomBattle", "NemesisDraft", "BanDraft"]
AUCTION_OPTIONS = ["Trainers", "Auctions", "Leaderboards", "Prizes"]

class MainApp(tk.Tk):
    # constructor function
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # initialize sidebar
        f_buttonsidebar = tk.Frame(self)
        f_buttonsidebar.grid(row=0, column=0, sticky="nsew")

        self.sidebar = Sidebar(parent=f_buttonsidebar, controller=self)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        # initialize main container for frames
        f_container = tk.Frame(self)
        f_container.grid(row=0, column=1, rowspan=5, sticky="nsew")
        f_container.grid_rowconfigure(0, weight=1)
        f_container.grid_columnconfigure(0, weight=1)

        self.containerFrames = {}

        # initialize each menu layer
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

    # menu changing function
    def show_frame(self, page_name):
        self.sidebar.set_selected(page_name)
        self.sidebar.update_media()
        frame = self.containerFrames[page_name]
        frame.tkraise()

class Trainers(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

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

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    #random.seed(time.strftime("%Y-%m-%d"))
    app = MainApp()
    app.mainloop()
