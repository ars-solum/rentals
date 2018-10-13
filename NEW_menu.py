try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

import os
import csv
import time
import random
from random import shuffle

TypeChart = {
    ("Bug", "Bug")      : 0,
    ("Bug", "Dark")     : 1,
    ("Bug", "Dragon")   : 0,
    ("Bug", "Electric") : 0,
    ("Bug", "Fairy")    : -1,
    ("Bug", "Fighting") : -1,
    ("Bug", "Fire")     : -1,
    ("Bug", "Flying")   : -1,
    ("Bug", "Ghost")    : -1,
    ("Bug", "Grass")    : 1,
    ("Bug", "Ground")   : 0,
    ("Bug", "Ice")      : 0,
    ("Bug", "Normal")   : 0,
    ("Bug", "Poison")   : -1,
    ("Bug", "Psychic")  : 1,
    ("Bug", "Rock")     : 0,
    ("Bug", "Steel")    : -1,
    ("Bug", "Water")    : 0,

    ("Dark", "Bug")      : 0,
    ("Dark", "Dark")     : -1,
    ("Dark", "Dragon")   : 0,
    ("Dark", "Electric") : 0,
    ("Dark", "Fairy")    : -1,
    ("Dark", "Fighting") : -1,
    ("Dark", "Fire")     : 0,
    ("Dark", "Flying")   : 0,
    ("Dark", "Ghost")    : 1,
    ("Dark", "Grass")    : 0,
    ("Dark", "Ground")   : 0,
    ("Dark", "Ice")      : 0,
    ("Dark", "Normal")   : 0,
    ("Dark", "Poison")   : 0,
    ("Dark", "Psychic")  : 1,
    ("Dark", "Rock")     : 0,
    ("Dark", "Steel")    : 0,
    ("Dark", "Water")    : 0,

    ("Dragon", "Bug")      : 0,
    ("Dragon", "Dark")     : 0,
    ("Dragon", "Dragon")   : 1,
    ("Dragon", "Electric") : 0,
    ("Dragon", "Fairy")    : -1,
    ("Dragon", "Fighting") : 0,
    ("Dragon", "Fire")     : 0,
    ("Dragon", "Flying")   : 0,
    ("Dragon", "Ghost")    : 0,
    ("Dragon", "Grass")    : 0,
    ("Dragon", "Ground")   : 0,
    ("Dragon", "Ice")      : 0,
    ("Dragon", "Normal")   : 0,
    ("Dragon", "Poison")   : 0,
    ("Dragon", "Psychic")  : 0,
    ("Dragon", "Rock")     : 0,
    ("Dragon", "Steel")    : -1,
    ("Dragon", "Water")    : 0,

    ("Electric", "Bug")      : 0,
    ("Electric", "Dark")     : 0,
    ("Electric", "Dragon")   : -1,
    ("Electric", "Electric") : -1,
    ("Electric", "Fairy")    : 0,
    ("Electric", "Fighting") : 0,
    ("Electric", "Fire")     : 0,
    ("Electric", "Flying")   : 1,
    ("Electric", "Ghost")    : 0,
    ("Electric", "Grass")    : -1,
    ("Electric", "Ground")   : -1,
    ("Electric", "Ice")      : 0,
    ("Electric", "Normal")   : 0,
    ("Electric", "Poison")   : 0,
    ("Electric", "Psychic")  : 0,
    ("Electric", "Rock")     : 0,
    ("Electric", "Steel")    : 0,
    ("Electric", "Water")    : 1,

    ("Fairy", "Bug")      : 0,
    ("Fairy", "Dark")     : 1,
    ("Fairy", "Dragon")   : 1,
    ("Fairy", "Electric") : 0,
    ("Fairy", "Fairy")    : 0,
    ("Fairy", "Fighting") : 1,
    ("Fairy", "Fire")     : -1,
    ("Fairy", "Flying")   : 0,
    ("Fairy", "Ghost")    : 0,
    ("Fairy", "Grass")    : 0,
    ("Fairy", "Ground")   : 0,
    ("Fairy", "Ice")      : 0,
    ("Fairy", "Normal")   : 0,
    ("Fairy", "Poison")   : -1,
    ("Fairy", "Psychic")  : 0,
    ("Fairy", "Rock")     : 0,
    ("Fairy", "Steel")    : -1,
    ("Fairy", "Water")    : 0,

    ("Fighting", "Bug")      : -1,
    ("Fighting", "Dark")     : 1,
    ("Fighting", "Dragon")   : 0,
    ("Fighting", "Electric") : 0,
    ("Fighting", "Fairy")    : 1,
    ("Fighting", "Fighting") : 0,
    ("Fighting", "Fire")     : 0,
    ("Fighting", "Flying")   : -1,
    ("Fighting", "Ghost")    : -1,
    ("Fighting", "Grass")    : 0,
    ("Fighting", "Ground")   : 0,
    ("Fighting", "Ice")      : 1,
    ("Fighting", "Normal")   : 1,
    ("Fighting", "Poison")   : -1,
    ("Fighting", "Psychic")  : -1,
    ("Fighting", "Rock")     : 1,
    ("Fighting", "Steel")    : 1,
    ("Fighting", "Water")    : 0,

    ("Fire", "Bug")      : 1,
    ("Fire", "Dark")     : 0,
    ("Fire", "Dragon")   : -1,
    ("Fire", "Electric") : 0,
    ("Fire", "Fairy")    : 0,
    ("Fire", "Fighting") : 0,
    ("Fire", "Fire")     : -1,
    ("Fire", "Flying")   : 0,
    ("Fire", "Ghost")    : 0,
    ("Fire", "Grass")    : 1,
    ("Fire", "Ground")   : 0,
    ("Fire", "Ice")      : 1,
    ("Fire", "Normal")   : 0,
    ("Fire", "Poison")   : 0,
    ("Fire", "Psychic")  : 0,
    ("Fire", "Rock")     : -1,
    ("Fire", "Steel")    : 1,
    ("Fire", "Water")    : -1,

    ("Flying", "Bug")      : 1,
    ("Flying", "Dark")     : 0,
    ("Flying", "Dragon")   : 0,
    ("Flying", "Electric") : -1,
    ("Flying", "Fairy")    : 0,
    ("Flying", "Fighting") : 1,
    ("Flying", "Fire")     : 0,
    ("Flying", "Flying")   : 0,
    ("Flying", "Ghost")    : 0,
    ("Flying", "Grass")    : 1,
    ("Flying", "Ground")   : 0,
    ("Flying", "Ice")      : 0,
    ("Flying", "Normal")   : 0,
    ("Flying", "Poison")   : 0,
    ("Flying", "Psychic")  : 0,
    ("Flying", "Rock")     : -1,
    ("Flying", "Steel")    : -1,
    ("Flying", "Water")    : 0,

    ("Ghost", "Bug")      : 0,
    ("Ghost", "Dark")     : -1,
    ("Ghost", "Dragon")   : 0,
    ("Ghost", "Electric") : 0,
    ("Ghost", "Fairy")    : 0,
    ("Ghost", "Fighting") : 0,
    ("Ghost", "Fire")     : 0,
    ("Ghost", "Flying")   : 0,
    ("Ghost", "Ghost")    : 1,
    ("Ghost", "Grass")    : 0,
    ("Ghost", "Ground")   : 0,
    ("Ghost", "Ice")      : 0,
    ("Ghost", "Normal")   : -1,
    ("Ghost", "Poison")   : 0,
    ("Ghost", "Psychic")  : 1,
    ("Ghost", "Rock")     : 0,
    ("Ghost", "Steel")    : 0,
    ("Ghost", "Water")    : 0,

    ("Grass", "Bug")      : -1,
    ("Grass", "Dark")     : 0,
    ("Grass", "Dragon")   : -1,
    ("Grass", "Electric") : 0,
    ("Grass", "Fairy")    : 0,
    ("Grass", "Fighting") : 0,
    ("Grass", "Fire")     : -1,
    ("Grass", "Flying")   : -1,
    ("Grass", "Ghost")    : 0,
    ("Grass", "Grass")    : -1,
    ("Grass", "Ground")   : 1,
    ("Grass", "Ice")      : 0,
    ("Grass", "Normal")   : 0,
    ("Grass", "Poison")   : -1,
    ("Grass", "Psychic")  : 0,
    ("Grass", "Rock")     : 1,
    ("Grass", "Steel")    : -1,
    ("Grass", "Water")    : 1,

    ("Ground", "Bug")      : -1,
    ("Ground", "Dark")     : 0,
    ("Ground", "Dragon")   : 0,
    ("Ground", "Electric") : 1,
    ("Ground", "Fairy")    : 0,
    ("Ground", "Fighting") : 0,
    ("Ground", "Fire")     : 1,
    ("Ground", "Flying")   : -1,
    ("Ground", "Ghost")    : 0,
    ("Ground", "Grass")    : -1,
    ("Ground", "Ground")   : 0,
    ("Ground", "Ice")      : 0,
    ("Ground", "Normal")   : 0,
    ("Ground", "Poison")   : 1,
    ("Ground", "Psychic")  : 0,
    ("Ground", "Rock")     : 1,
    ("Ground", "Steel")    : 1,
    ("Ground", "Water")    : 0,

    ("Ice", "Bug")      : 0,
    ("Ice", "Dark")     : 0,
    ("Ice", "Dragon")   : 1,
    ("Ice", "Electric") : 0,
    ("Ice", "Fairy")    : 0,
    ("Ice", "Fighting") : 0,
    ("Ice", "Fire")     : -1,
    ("Ice", "Flying")   : 1,
    ("Ice", "Ghost")    : 0,
    ("Ice", "Grass")    : 1,
    ("Ice", "Ground")   : 1,
    ("Ice", "Ice")      : -1,
    ("Ice", "Normal")   : 0,
    ("Ice", "Poison")   : 0,
    ("Ice", "Psychic")  : 0,
    ("Ice", "Rock")     : 0,
    ("Ice", "Steel")    : -1,
    ("Ice", "Water")    : -1,

    ("Normal", "Bug")      : 0,
    ("Normal", "Dark")     : 0,
    ("Normal", "Dragon")   : 0,
    ("Normal", "Electric") : 0,
    ("Normal", "Fairy")    : 0,
    ("Normal", "Fighting") : 0,
    ("Normal", "Fire")     : 0,
    ("Normal", "Flying")   : 0,
    ("Normal", "Ghost")    : -1,
    ("Normal", "Grass")    : 0,
    ("Normal", "Ground")   : 0,
    ("Normal", "Ice")      : 0,
    ("Normal", "Normal")   : 0,
    ("Normal", "Poison")   : 0,
    ("Normal", "Psychic")  : 0,
    ("Normal", "Rock")     : -1,
    ("Normal", "Steel")    : -1,
    ("Normal", "Water")    : 0,

    ("Poison", "Bug")      : 0,
    ("Poison", "Dark")     : 0,
    ("Poison", "Dragon")   : 0,
    ("Poison", "Electric") : 0,
    ("Poison", "Fairy")    : 1,
    ("Poison", "Fighting") : 0,
    ("Poison", "Fire")     : 0,
    ("Poison", "Flying")   : 0,
    ("Poison", "Ghost")    : -1,
    ("Poison", "Grass")    : 1,
    ("Poison", "Ground")   : -1,
    ("Poison", "Ice")      : 0,
    ("Poison", "Normal")   : 0,
    ("Poison", "Poison")   : -1,
    ("Poison", "Psychic")  : 0,
    ("Poison", "Rock")     : -1,
    ("Poison", "Steel")    : -1,
    ("Poison", "Water")    : 0,

    ("Psychic", "Bug")      : 0,
    ("Psychic", "Dark")     : -1,
    ("Psychic", "Dragon")   : 0,
    ("Psychic", "Electric") : 0,
    ("Psychic", "Fairy")    : 0,
    ("Psychic", "Fighting") : 1,
    ("Psychic", "Fire")     : 0,
    ("Psychic", "Flying")   : 0,
    ("Psychic", "Ghost")    : 0,
    ("Psychic", "Grass")    : 0,
    ("Psychic", "Ground")   : 0,
    ("Psychic", "Ice")      : 0,
    ("Psychic", "Normal")   : 0,
    ("Psychic", "Poison")   : 1,
    ("Psychic", "Psychic")  : -1,
    ("Psychic", "Rock")     : 0,
    ("Psychic", "Steel")    : -1,
    ("Psychic", "Water")    : 0,

    ("Rock", "Bug")      : 1,
    ("Rock", "Dark")     : 0,
    ("Rock", "Dragon")   : 0,
    ("Rock", "Electric") : 0,
    ("Rock", "Fairy")    : 0,
    ("Rock", "Fighting") : -1,
    ("Rock", "Fire")     : 1,
    ("Rock", "Flying")   : 1,
    ("Rock", "Ghost")    : 0,
    ("Rock", "Grass")    : 0,
    ("Rock", "Ground")   : -1,
    ("Rock", "Ice")      : 1,
    ("Rock", "Normal")   : 0,
    ("Rock", "Poison")   : 0,
    ("Rock", "Psychic")  : 0,
    ("Rock", "Rock")     : 0,
    ("Rock", "Steel")    : -1,
    ("Rock", "Water")    : 0,

    ("Steel", "Bug")      : 0,
    ("Steel", "Dark")     : 0,
    ("Steel", "Dragon")   : 0,
    ("Steel", "Electric") : -1,
    ("Steel", "Fairy")    : 1,
    ("Steel", "Fighting") : 0,
    ("Steel", "Fire")     : -1,
    ("Steel", "Flying")   : 0,
    ("Steel", "Ghost")    : 0,
    ("Steel", "Grass")    : 0,
    ("Steel", "Ground")   : 0,
    ("Steel", "Ice")      : 1,
    ("Steel", "Normal")   : 0,
    ("Steel", "Poison")   : 0,
    ("Steel", "Psychic")  : 0,
    ("Steel", "Rock")     : 1,
    ("Steel", "Steel")    : -1,
    ("Steel", "Water")    : -1,

    ("Water", "Bug")      : 0,
    ("Water", "Dark")     : 0,
    ("Water", "Dragon")   : -1,
    ("Water", "Electric") : 0,
    ("Water", "Fairy")    : 0,
    ("Water", "Fighting") : 0,
    ("Water", "Fire")     : 1,
    ("Water", "Flying")   : 0,
    ("Water", "Ghost")    : 0,
    ("Water", "Grass")    : -1,
    ("Water", "Ground")   : 1,
    ("Water", "Ice")      : 0,
    ("Water", "Normal")   : 0,
    ("Water", "Poison")   : 0,
    ("Water", "Psychic")  : 0,
    ("Water", "Rock")     : 1,
    ("Water", "Steel")    : 0,
    ("Water", "Water")    : -1
}

B_WIDTH = 15
BATTLE_OPTIONS = ["Standard Draft", "Random Battle", "Nemesis Draft", "First Pick Draft"]
AUCTION_OPTIONS = ["Trainers", "Auctions", "Leaderboards", "Prizes"]

POKEMON = []
IMGTYPE = ["inactive", "active", "picked", "banned", "unknown"]
def type_logic(attackingPokemon, defendingPokemon):
    matchup = 0
    if ("Delta Stream" in attackingPokemon.ability):
        return True
    if ("Multitype" in attackingPokemon.ability or
        "Multitype" in defendingPokemon.ability or
        "RKS System" in attackingPokemon.ability or
        "RKS System" in defendingPokemon.ability):
        return False
    for x in attackingPokemon.type:
        if x:
            for y in defendingPokemon.type:
                if y:
                    if (("Levitate" in defendingPokemon.ability  and "Ground" in x) or
                        ("Flash Fire" in defendingPokemon.ability  and "Fire" in x) or
                        ("Water Bubble" in defendingPokemon.ability  and "Fire" in x) or
                        ("Water Absorb" in defendingPokemon.ability  and "Water" in x) or
                        ("Storm Drain" in defendingPokemon.ability  and "Water" in x) or
                        ("Dry Skin" in defendingPokemon.ability  and "Water" in x) or
                        ("Lightningrod" in defendingPokemon.ability  and "Electric" in x) or
                        ("Volt Absorb" in defendingPokemon.ability  and "Electric" in x) or
                        ("Motor Drive" in defendingPokemon.ability  and "Electric" in x) or
                        ("Sap Sipper" in defendingPokemon.ability  and "Grass" in x) or
                        ("Desolate Land" in defendingPokemon.ability  and "Water" in x) or
                        ("Primordial Sea" in defendingPokemon.ability  and "Fire" in x) or
                        ("Prankster" in attackingPokemon.ability  and "Dark" in y)):
                        matchup -= 1
                    elif (("Fluffy" in defendingPokemon.ability and "Fire" in x) or
                          ("Dry Skin" in defendingPokemon.ability and "Fire" in x) or
                          ("Steelworker" in attackingPokemon.ability and "Rock" in y) or
                          ("Steelworker" in attackingPokemon.ability and "Fairy" in y) or
                          ("Steelworker" in attackingPokemon.ability and "Ice" in y)):
                        matchup += 1
                    elif (("Scrappy" in attackingPokemon.ability and "Ghost" in y) or
                          ("Tinted Lens" in attackingPokemon.ability and
                            ("Fairy" in y) or ("Fighting" in y) or ("Fire" in y) or
                            ("Flying" in y) or ("Ghost" in y) or ("Poison" in y) or
                            ("Steel" in y))):
                        matchup += 0
                    else:
                        matchup += TypeChart[(x, y)]
    if matchup > 0:
        return True
    else:
        return False

class Pokemon:
    def __init__(self, row):
        self.id = row[0]
        self.name = row[1]
        self.dex = row[2]
        self.type = [row[3], row[4]]
        self.tier = row[5]
        self.item = row[6]
        self.ability = row[7]
        self.evSpread = row[8]
        self.nature = row[9]
        self.ivSpread = row[10]
        self.moves = [row[11], row[12], row[13], row[14]]
        self.image = [[] for j in range(4)]

        for j in range(4):
            if j == 1:
                self.image[j].append(tk.PhotoImage(file='media\\{0}\\{1}_{2}.gif'.format(BATTLE_OPTIONS[j].replace(" ", ""), self.name, IMGTYPE[0])))
            else:
                for i in range(5):
                    self.image.append(tk.PhotoImage(file='media\\{0}\\{1}_{2}.gif'.format(BATTLE_OPTIONS[j].replace(" ", ""), self.name, IMGTYPE[i])))


class MainApp(tk.Tk):
    ############################################
    ##### constructor/initializer function #####
    ############################################
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        ########################################
        ##### initialize private variables #####
        ########################################
        f_buttonsidebar = tk.Frame(self)
        f_buttonsidebar.grid(row=0, column=0, sticky="nsew")
        f_buttonsidebar.grid_rowconfigure(0, weight=1)
        f_buttonsidebar.grid_columnconfigure(0, weight=1)

        mainSidebar = Sidebar(parent=f_buttonsidebar, controller=self)
        self.sidebar = mainSidebar
        mainSidebar.grid(row=0, column=0, sticky="nsew")

        f_container = tk.Frame(self)
        f_container.grid(row=0, column=1, rowspan=4, sticky="nsew")
        f_container.grid_rowconfigure(0, weight=1)
        f_container.grid_columnconfigure(1, weight=1)

        self.containerFrames = {}

        ######################################
        ##### initialize each menu layer #####
        ######################################
        for F in (StandardDraft, RandomBattle, NemesisDraft, FirstPickDraft,
                    Trainers, Auctions, Leaderboards, Prizes):
            page_name = F.__name__
            frame = F(parent=f_container, controller=self)
            self.containerFrames[page_name] = frame
            frame.grid(row=0, column=1, rowspan=4, sticky="nsew")

        self.show_frame("StandardDraft")
        self.sidebar.set_selected(BATTLE_OPTIONS[0].replace(" ", ""))

    ########################################
    ##### menu layer changing function #####
    ########################################
    def show_frame(self, page_name):
        self.sidebar.set_selected(page_name)
        self.sidebar.update_media()
        frame = self.containerFrames[page_name]
        frame.tkraise()

class Sidebar(tk.Frame):
    ############################################
    ##### constructor/initializer function #####
    ############################################
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        ########################################
        ##### initialize private variables #####
        ########################################
        self.currSelected = None
        self.prevSelected = None
        self.f_menuOptions = []
        self.b_battleOptions = []
        self.b_auctionOptions = []
        self.img_selected_button = []
        self.img_active_button = []
        self.img_inactive_button = []
        self.img_battleModes = tk.PhotoImage(file='media\\battle_formats.gif')

        ##############################################
        ##### set up the menu buttons and images #####
        ##############################################
        for i in range(2):
            self.f_menuOptions.append(tk.Frame(self))
            self.f_menuOptions[i].grid(row=i, column=0, sticky="nsew")

        self.l_battleModes = tk.Label(self.f_menuOptions[0], image=self.img_battleModes)
        self.l_auctionModes = tk.Label(self.f_menuOptions[1], text="Auction Options", width=B_WIDTH)

        self.l_battleModes.image = self.img_battleModes
        self.l_battleModes.grid(row=0, column=0)

        for i in range(4):
            self.img_selected_button.append(tk.PhotoImage(file='media\\button_selected_{0}.gif'.format(BATTLE_OPTIONS[i].replace(" ", ""))))
            self.img_active_button.append(tk.PhotoImage(file='media\\button_active_{0}.gif'.format(BATTLE_OPTIONS[i].replace(" ", ""))))
            self.img_inactive_button.append(tk.PhotoImage(file='media\\button_inactive_{0}.gif'.format(BATTLE_OPTIONS[i].replace(" ", ""))))

            if i == 0:
                self.b_battleOptions.append(tk.Button(self.f_menuOptions[0], image=self.img_selected_button[i], bd=0.1,
                                                        command=lambda i=i: controller.show_frame(BATTLE_OPTIONS[i].replace(" ", ""))))
                self.currSelected = BATTLE_OPTIONS[i].replace(" ", "")
            else:
                self.b_battleOptions.append(tk.Button(self.f_menuOptions[0], image=self.img_inactive_button[i], bd=0.1,
                                                        command=lambda i=i: controller.show_frame(BATTLE_OPTIONS[i].replace(" ", ""))))
            self.b_battleOptions[i].grid(row=i+1, column=0)
            self.b_battleOptions[i].image = self.img_active_button[i]
            self.b_battleOptions[i].bind("<Enter>", lambda event, i=i: self.on_enter(i))
            self.b_battleOptions[i].bind("<Leave>", lambda event, i=i: self.on_leave(i))

        self.l_auctionModes.grid(row=5, column=0, pady=10)

        for i in range(4):
            self.b_auctionOptions.append(tk.Button(self.f_menuOptions[1], text=AUCTION_OPTIONS[i], width=B_WIDTH,
                                                command=lambda i=i: controller.show_frame(AUCTION_OPTIONS[i].replace(" ", ""))))
            self.b_auctionOptions[i].grid(row=i+6, column=0)


    def on_enter(self, i):
        if self.currSelected == BATTLE_OPTIONS[i].replace(" ", ""):
            pass
        else:
            self.b_battleOptions[i].config(image=self.img_active_button[i])
            self.b_battleOptions[i].image = self.img_active_button[i]

    def on_leave(self, i):
        if self.currSelected == BATTLE_OPTIONS[i].replace(" ", ""):
            self.b_battleOptions[i].config(image=self.img_selected_button[i])
            self.b_battleOptions[i].image = self.img_selected_button[i]
        else:
            self.b_battleOptions[i].config(image=self.img_inactive_button[i])
            self.b_battleOptions[i].image = self.img_inactive_button[i]

    def set_selected(self, x):
        self.prevSelected = self.currSelected
        self.currSelected = x

    def get_currSelected(self):
        return self.currSelected

    def get_prevSelected(self):
        return self.prevSelected

    def update_media(self):
        if self.currSelected != self.prevSelected:
            for i in range(4):
                if self.prevSelected == BATTLE_OPTIONS[i].replace(" ", ""):
                    self.b_battleOptions[i].config(image=self.img_inactive_button[i])
                    self.b_battleOptions[i].image = self.img_inactive_button[i]
                    break
        else:
            for i in range(4):
                if self.currSelected == BATTLE_OPTIONS[i].replace(" ", ""):
                    self.b_battleOptions[i].config(image=self.img_selected_button[i])
                    self.b_battleOptions[i].image = self.img_selected_button[i]
                    break

class TeamBox(tk.Frame):
    def __init__(self, parent, controller, team, mode):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.team = team

        img_team = tk.PhotoImage(file='media\\T{0}T_logo_inactive.gif'.format(team))
        l_team = tk.Label(self, image=img_team)
        l_team.grid(row=0, column=0, columnspan=3)
        l_team.image = img_team

        self.img_inactive_Blank = tk.PhotoImage(file='media\\{0}\\button_inactive_Blank.gif'.format(mode))

        self.l_pokemon = []
        for i in range(3):
            for j in range(2):
                x = (i*2)+j
                self.l_pokemon.append(tk.Label(self, image=self.img_inactive_Blank))
                if j == 0:
                    self.l_pokemon[x].grid(row=i+1, column=j, sticky="e")
                else:
                    self.l_pokemon[x].grid(row=i+1, column=j, sticky="e")
                self.l_pokemon[x].image = self.img_inactive_Blank
    def update_pokemon(self, x):
        pass

class HelpBox(tk.Frame):
    def __init__(self, parent, controller, mode):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.img_blank = tk.PhotoImage(file='media\\{0}\\button_inactive_Blank.gif'.format(mode))
        self.img_pokemon_selected = tk.PhotoImage(file='media\\empty_pokemon.gif')

        self.img_pokemon = []
        self.img_pokemon.append(tk.PhotoImage(file='media\\{0}\\Bulbasaur_inactive.gif'.format(mode)))
        self.img_pokemon.append(tk.PhotoImage(file='media\\{0}\\Charmander_inactive.gif'.format(mode)))

        self.container = []
        for i in range(3):
            self.container.append(tk.Frame(self))
            self.container[i].grid(row=0, column=i, padx=5)

        self.l_pokemon_name = tk.Label(self.container[0], text="", width=10)
        self.l_pokemon_selected = tk.Label(self.container[0], image=self.img_pokemon_selected)
        self.l_pokemon_selected.image = self.img_pokemon_selected
        self.l_pokemon_name.grid(row=0, column=0, sticky="nsew")
        self.l_pokemon_selected.grid(row=1, column=0, sticky="nsew")

        self.l_possibleAbility = tk.Label(self.container[1], text="")
        self.l_possibleAbilities = tk.Label(self.container[1], text="", width=B_WIDTH)
        self.l_possibleAbility.grid(row=0, column=0, sticky="n")
        self.l_possibleAbilities.grid(row=1, column=0, sticky="n")

        self.l_counterpick = tk.Label(self.container[2], text="")
        self.l_counterpick.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.l_counters = []
        for i in range(3):
            self.l_counters.append(tk.Label(self.container[2], image=self.img_pokemon_selected))
            self.l_counters[i].grid(row=1, column=i, padx=5, sticky="nsew")
            self.l_counters[i].image = self.img_pokemon_selected

    def update_info(self, i):
        if self.controller.assist.get():
            if i == 0:
                self.l_pokemon_name.config(text="Bulbasaur")
                self.l_possibleAbilities.config(text="Overgrow\nChlorophyll\n")
                self.l_counters[0].config(image=self.img_pokemon[1])
                self.l_counters[0].image = self.img_pokemon[1]
                for j in range(1, 3):
                    self.l_counters[j].config(image=self.img_blank)
                    self.l_counters[j].image = self.img_blank
            if i == 1:
                self.l_pokemon_name.config(text="Charmander")
                self.l_possibleAbilities.config(text="Blaze\nSolar Power\n")
                for j in range(3):
                    self.l_counters[j].config(image=self.img_blank)
                    self.l_counters[j].image = self.img_blank
            self.l_possibleAbility.config(text="Possible Abilities:")
            self.l_counterpick.config(text="Struggles Against:")
            self.l_pokemon_selected.config(image=self.img_pokemon[i])
            self.l_pokemon_selected.image = self.img_pokemon[i]



    def hide_info(self):
        if self.controller.assist.get():
            self.l_pokemon_name.config(text="")
            self.l_pokemon_selected.config(image=self.img_pokemon_selected)
            self.l_pokemon_selected.image = self.img_pokemon_selected
            self.l_possibleAbility.config(text="")
            self.l_possibleAbilities.config(text="")
            self.l_counterpick.config(text="")
            for i in range(3):
                self.l_counters[i].config(image=self.img_pokemon_selected)
                self.l_counters[i].image = self.img_pokemon_selected

class SettingsBar(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.img_settingsTitle = tk.PhotoImage(file='media\\label_settings_{0}.gif'.format(controller.__class__.__name__))

        self.l_settingsTitle = tk.Label(self, image=self.img_settingsTitle)
        self.l_settingsTitle.grid(row=0, column=0, columnspan=2)
        self.l_settingsTitle.image = self.img_settingsTitle

        self.optionsRandom = ["Random", 0, "Semi-Random", 1]
        self.optionsExcludeTiers = ["Ubers", "OU", "UU", "RU", "NU", "PU"]

        self.randomness = tk.IntVar()
        self.excludes = [tk.StringVar() for i in range(6)]

        self.l_generate = tk.Label(self, text="Random Pokémon Generation")
        self.l_generate.grid(row=1, column=0, columnspan=2, sticky="w")

        self.b_randomness = []
        for i in range(2):
            self.b_randomness.append(tk.Radiobutton(self, text=self.optionsRandom[i*2], variable=self.randomness, value=self.optionsRandom[(i*2)+1]))
            self.b_randomness[i].grid(row=i+2, column=0, padx=20, columnspan=2, sticky="w")

        self.l_exclude = tk.Label(self, text="Exclude:")
        self.l_exclude.grid(row=4, column=0, columnspan=2, sticky="w")

        self.b_excludes = []
        for i in range(6):
            self.b_excludes.append(tk.Checkbutton(self, text=self.optionsExcludeTiers[i], variable=self.excludes[i], onvalue=self.optionsExcludeTiers[i], offvalue=""))
            if i%2 == 0:
                self.b_excludes[i].grid(row=i+5, column=0, padx=(20, 0), sticky="w")
            else:
                self.b_excludes[i].grid(row=i+4, column=1, sticky="w")

        self.l_other = tk.Label(self, text="Other Options")
        self.l_other.grid(row=11, column=0, columnspan=2, sticky="w")
        self.b_assist = tk.Checkbutton(self, text="Assist Trainer?", variable=self.controller.assist, onvalue=True, offvalue=False)
        self.b_assist.grid(row=12, column=0, columnspan=2, padx=(20, 0), sticky="w")

        self.goButton = tk.Button(self, text="Go", command=lambda: controller.activate())
        self.goButton.grid(row=13, column=0, padx=5, pady=5)

class StandardDraft(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.activated = False
        self.pokemonNotPicked = [True for i in range(18)]
        self.assist = tk.BooleanVar()
        self.assist.set(False)

        self.img_inactive_Blank = tk.PhotoImage(file='media\\{0}\\button_inactive_Blank.gif'.format(BATTLE_OPTIONS[0].replace(" ", "")))
        self.img_active_Blank = tk.PhotoImage(file='media\\{0}\\button_active_Blank.gif'.format(BATTLE_OPTIONS[0].replace(" ", "")))

        self.b_icons = []
        self.img_pokemon = [[] for i in range(18)]

        for i in range(3):
            for j in range(6):
                x = (i*6)+j
                self.b_icons.append(tk.Button(self, image=self.img_inactive_Blank, bd=0.1, command=None))
                self.b_icons[x].grid(row=i, column=j, padx=5, pady=5)
                self.b_icons[x].image = self.img_inactive_Blank
                self.b_icons[x].bind("<Enter>", lambda event, x=x: self.on_enter(x))
                self.b_icons[x].bind("<Leave>", lambda event, x=x: self.on_leave(x))

        self.f_teams = []
        for i in range(2):
            frame = TeamBox(parent=self, controller=self, team=i+1, mode="StandardDraft")
            self.f_teams.append(frame)
            frame.grid(row=3, column=i*3, columnspan=3, pady=(30,0), sticky="nsew")

        self.helpbox = HelpBox(parent=self, controller=self, mode="StandardDraft")
        self.helpbox.grid(row=4, column=0, columnspan=6, pady=10)

        self.settings = SettingsBar(parent=self, controller=self)
        self.settings.grid(row=0, column=7, rowspan=8, sticky="n")


    def activate(self):
        self.activated = True
        ########################
        ## generate code here ##
        ########################

        for i in range(18):
            self.pokemonNotPicked[i] = True

        self.b_icons[0].config(image=self.testicon[0], command=lambda: self.test(0))
        self.b_icons[0].image = self.testicon[0]
        self.b_icons[1].config(image=self.testicon[3], command=lambda: self.test(1))
        self.b_icons[1].image = self.testicon[3]

    def test(self, i):
        if self.pokemonNotPicked[i]:
            self.b_icons[i].config(image=self.testicon[i+2])
            self.b_icons[i].image = self.testicon[i+2]
            self.pokemonNotPicked[i] = False

    def on_enter(self, i):
        if self.activated:
            if i == 0:
                if self.pokemonNotPicked[i]:
                    self.b_icons[0].config(image=self.testicon[1])
                    self.b_icons[0].image = self.testicon[1]
                self.helpbox.update_info(i)
            elif i == 1:
                if self.pokemonNotPicked[i]:
                    self.b_icons[1].config(image=self.testicon[4])
                    self.b_icons[1].image = self.testicon[4]
                self.helpbox.update_info(i)
            else:
                self.b_icons[i].config(image=self.img_active_Blank)
                self.b_icons[i].image = self.img_active_Blank
        else:
            self.b_icons[i].config(image=self.img_active_Blank)
            self.b_icons[i].image = self.img_active_Blank

    def on_leave(self, i):
        if self.activated:
            if i == 0:
                if self.pokemonNotPicked[i]:
                    self.b_icons[0].config(image=self.testicon[0])
                    self.b_icons[0].image = self.testicon[0]
                self.helpbox.hide_info()
            elif i == 1:
                if self.pokemonNotPicked[i]:
                    self.b_icons[1].config(image=self.testicon[3])
                    self.b_icons[1].image = self.testicon[3]
                self.helpbox.hide_info()
            else:
                self.b_icons[i].config(image=self.img_inactive_Blank)
                self.b_icons[i].image = self.img_inactive_Blank
        else:
            self.b_icons[i].config(image=self.img_inactive_Blank)
            self.b_icons[i].image = self.img_inactive_Blank

class RandomBattle(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

class NemesisDraft(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

class FirstPickDraft(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

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

    random.seed(time.strftime("%Y-%m-%d"))

    app = MainApp()
    with open('main_database.csv', 'r') as fileName:
        reader = csv.reader(fileName)
        next(reader, None)
        for row in reader:
            POKEMON.append(Pokemon(row))
    app.mainloop()
