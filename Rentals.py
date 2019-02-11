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

ROOT = os.path.dirname(os.path.realpath(__file__))

SIDEBAR_OPTIONS = ["StandardDraft", "RandomBattle"]
AUCTION_OPTIONS = ["Trainers", "Auctions", "Leaderboards", "Prizes"]

class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # initialize main menu items
        self.f_sidebar = tk.Frame(self)
        self.f_sidebar.grid(row=0, column=0, rowspan=11, columnspan=2, sticky="nsew")
        self.sidebar = Sidebar(parent=self.f_sidebar, controller=self)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        self.f_container = tk.Frame(self)
        self.f_container.grid(row=0, column=1, rowspan=10, columnspan=6, sticky="nsew")

        self.containerFrames = {}

        # initialize each menu layer
        for i in range(len(SIDEBAR_OPTIONS)):
            page_name = SIDEBAR_OPTIONS[i]
            frame = Battle(parent=self.f_container, controller=self, mode=page_name)
            self.containerFrames[page_name] = frame
            frame.grid(row=0, column=0, rowspan=4, sticky="nsew")

        for F in (Trainers, Auctions, Leaderboards, Prizes):
            page_name = F.__name__
            frame = F(parent=self.f_container, controller=self)
            self.containerFrames[page_name] = frame
            frame.grid(row=0, column=0, rowspan=4, sticky="nsew")

        for i in range(11):
            self.grid_rowconfigure(i, weight=1)
        for i in range(8):
            self.grid_columnconfigure(i, weight=1)

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
