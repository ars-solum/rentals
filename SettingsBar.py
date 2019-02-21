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

# class SettingsBar(tk.Frame):
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         self.controller = controller
#
#         self.img_settingsTitle = ImageTk.PhotoImage(RGBAImage('media\\Common\\label_settings_{0}.png'.format(self.controller.mode)))
#
#         self.l_settingsTitle = tk.Label(self, image=self.img_settingsTitle)
#         self.l_settingsTitle.grid(row=0, column=0, columnspan=3)
#
#         self.l_generate = tk.Label(self, text="Pokémon Appearance")
#         self.l_generate.grid(row=1, column=0, columnspan=2, sticky="w")
#         #tritype
#         self.optionsRandom = ["Random (default)", 0, "Balanced", 1, "Skewed", 2]
#         self.randomness = tk.IntVar()
#         self.b_randomness = []
#         for i in range(3):
#             self.b_randomness.append(tk.Radiobutton(self, text=self.optionsRandom[i*2], variable=self.randomness, value=self.optionsRandom[(i*2)+1]))
#             self.b_randomness[i].grid(row=i+2, column=0, padx=20, columnspan=2, sticky="w")
#
#
#         if "Random" not in self.controller.mode:
#             self.l_turn = tk.Label(self, text="Turn Order")
#             self.l_turn.grid(row=5, column=0, columnspan=2, sticky="w")
#             self.optionsTurnOrder = ["Sequential (default)", 0, "First Pick", 1, "Random", 2]
#             self.turnOrder = tk.IntVar()
#             self.b_turns = []
#             for i in range(3):
#                 self.b_turns.append(tk.Radiobutton(self, text=self.optionsTurnOrder[i*2], variable=self.turnOrder, value=self.optionsTurnOrder[(i*2)+1]))
#                 self.b_turns[i].grid(row=i+6, column=0, padx=20, columnspan=2, sticky="w")
#
#
#         if "Ban" in self.controller.mode:
#             self.l_bans = tk.Label(self, text="Number of Bans")
#             self.l_bans.grid(row=9, column=0, columnspan=2, sticky="w")
#
#             self.optionsBans = ["One (default)", 1, "Two", 2, "Three", 3]
#             self.bans = tk.IntVar(value=1)
#             self.b_bans = []
#             for i in range(3):
#                 self.b_bans.append(tk.Radiobutton(self, text=self.optionsBans[i*2], variable=self.bans, value=self.optionsBans[(i*2)+1]))
#                 self.b_bans[i].grid(row=i+10, column=0, columnspan=2, padx=20, sticky="w")
#
#
#         self.l_exclude = tk.Label(self, text="Exclusions")
#         self.l_exclude.grid(row=13, column=0, columnspan=1, sticky="w")
#         #self.b_moreExcludes = tk.Button(self, text=">", command=lambda: self.moreExcludes(1))
#         #self.b_moreExcludes.grid(row=13, column=1, columnspan=1, sticky="w")
#         self.optionsExcludeTiers = ["UBERS", "OU", "UU", "RU", "NU", "PU", "NFE"]
#         self.optionsExcludeRegions = ["Kanto", "Johto", "Hoenn", "Sinnoh", "Unova", "Kalos", "Alola"]
#         self.tierExcludes = [tk.StringVar() for i in range(7)]
#         self.regionExcludes = [tk.StringVar() for i in range(7)]
#         self.typeExcludes = [tk.StringVar() for i in range(7)]
#         self.b_tierExcludes = []
#         self.b_regionExcludes = []
#         self.b_typeExcludes = []
#         for i in range(7):
#             self.b_tierExcludes.append(tk.Checkbutton(self, text=self.optionsExcludeTiers[i], variable=self.tierExcludes[i], onvalue=self.optionsExcludeTiers[i], offvalue=""))
#             if i%2 == 0:
#                 self.b_tierExcludes[i].grid(row=i+14, column=0, padx=(20, 0), sticky="w")
#             else:
#                 self.b_tierExcludes[i].grid(row=i+13, column=1, sticky="w")
#
#         if "Random" not in self.controller.mode:
#             self.l_other = tk.Label(self, text="Other Options")
#             self.l_other.grid(row=21, column=0, columnspan=2, sticky="w")
#             self.b_assist = tk.Checkbutton(self, text="Show Basic Tips", variable=self.controller.assist)
#             self.b_assist.grid(row=22, column=0, columnspan=2, padx=(20, 0), sticky="w")
#             self.b_vscpu = tk.Checkbutton(self, text="Play Against CPU", variable=self.controller.vscpu, command=lambda: self.controller.playCPU())
#             self.b_vscpu.grid(row=23, column=0, columnspan=2, padx=(20, 0), sticky="w")
#             self.b_blind = tk.Checkbutton(self, text="Blind Mode", variable=self.controller.blind, command=lambda: self.controller.blindMode())
#             self.b_blind.grid(row=24, column=0, columnspan=2, padx=(20, 0), sticky="w")
#             self.b_mega = tk.Checkbutton(self, text="Reveal Megas", variable=self.controller.show_megas, command=lambda: self.controller.showMegas())
#             self.b_mega.grid(row=25, column=0, columnspan=2, padx=(20, 0), sticky="w")
#
#
#         self.goButton = tk.Button(self, text="Go", command=lambda: self.controller.activate())
#         self.goButton.grid(row=26, column=0, padx=5, pady=5)
#
#     def moreExcludes(self, page):
#         for i in range(7):
#             self.b_tierExcludes[i].grid_forget()
