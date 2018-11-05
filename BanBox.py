try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk
from PIL import Image, ImageTk
from RGBAImage import RGBAImage

from Pokemon import Pokemon, ALL_POKEMON, ABILITIES, TypeChart, type_logic

BATTLE_OPTIONS = ["StandardDraft", "RandomBattle", "NemesisDraft", "BanDraft"]
AUCTION_OPTIONS = ["Trainers", "Auctions", "Leaderboards", "Prizes"]
IMGTYPE = ["inactive", "active", "picked", "banned", "unknown"]

class BanBox(tk.Frame):
    def __init__(self, parent, controller, team):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.img_team = ImageTk.PhotoImage(RGBAImage('media\\Common\\t{0}bans.png'.format(team)))
        self.l_team = tk.Label(self, image=self.img_team)
        self.l_team.grid(row=0, column=0, columnspan=3)

        self.img_empty = ImageTk.PhotoImage(RGBAImage('media\\empty_pokemon.png'))

        self.l_pokemon = []
        for i in range(3):
            self.l_pokemon.append(tk.Label(self, image=self.controller.img_inactive_Blank))
            self.l_pokemon[i].grid(row=1, column=i, sticky="nsew")
