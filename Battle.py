try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

import os
import random
from random import shuffle
from PIL import Image, ImageTk
from RGBAImage import RGBAImage, RGBAImage2

from BanBox import BanBox
from TeamBox import TeamBox
from HelpBox import HelpBox
from SettingsBar import SettingsBar

from Pokemon import Pokemon, ALL_POKEMON, ABILITIES, TypeChart, type_logic

ROOT = os.path.dirname(os.path.realpath(__file__))

BATTLE_OPTIONS = ["StandardDraft", "RandomBattle", "NemesisDraft", "BanDraft"]
AUCTION_OPTIONS = ["Trainers", "Auctions", "Leaderboards", "Prizes"]
IMGTYPE = ["inactive", "active", "picked", "banned", "unknown"]

class Battle(tk.Frame):
    def __init__(self, parent, controller, mode):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.mode = mode

        # # initialize variables and images
        # self.alpha = 0
        # self.turn = 0
        # self.activated = False
        # self.pokemonNotPicked = [True for i in range(18)]

        self.assist = tk.BooleanVar()
        self.assist.set(False)
        self.vscpu = tk.BooleanVar()
        self.vscpu.set(False)
        self.blind = tk.BooleanVar()
        self.blind.set(False)
        self.show_megas = tk.BooleanVar()
        self.show_megas.set(False)

        self.img_border = RGBAImage2(os.path.join(ROOT, 'media', 'Common', 'border_%s.png' %(self.mode)))
        self.img_border_mega = RGBAImage2(os.path.join(ROOT, 'media', 'Common', 'border_Mega.png'))
        self.img_inactive_Blank_base = RGBAImage2(os.path.join(ROOT, 'media', 'Common', 'button_inactive_Blank.png'))
        self.img_active_Blank_base = RGBAImage2(os.path.join(ROOT, 'media', 'Common', 'button_active_Blank.png'))
        self.img_inactive_Blank_base.paste(self.img_border, (0, 0))
        self.img_active_Blank_base.paste(self.img_border, (0, 0), self.img_border)
        self.img_inactive_Blank = ImageTk.PhotoImage(self.img_inactive_Blank_base)
        self.img_active_Blank = ImageTk.PhotoImage(self.img_active_Blank_base)

        # # initialize pool of pokemon buttons
        # if "Random" not in self.mode:
        #     self.b_icons = []
        #     self.img_pokemon = [[] for i in range(18)]
        #     for i in range(3):
        #         for j in range(6):
        #             x = (i*6)+j
        #             self.b_icons.append(tk.Button(self, image=self.img_inactive_Blank, bd=0.1, command=None))
        #             self.b_icons[x].grid(row=i, column=j, padx=5, pady=5)
        #             self.b_icons[x].bind("<Enter>", lambda event, x=x: self.on_enter(x))
        #             self.b_icons[x].bind("<Leave>", lambda event, x=x: self.on_leave(x))
        #
        # # initialize team boxes
        # self.f_teams = []
        # if "Ban" in self.mode:
        #     self.f_bans = []
        # for i in range(2):
        #     if "Ban" in self.mode:
        #         self.f_bans.append(BanBox(parent=self, controller=self, team=i+1))
        #         self.f_bans[i].grid(row=3, column=i*3, columnspan=3, padx=5, sticky="nsew")
        #         self.f_teams.append(TeamBox(parent=self, controller=self, team=i+1))
        #         self.f_teams[i].grid(row=4, column=i*3, columnspan=3, padx=10, sticky="nsew")
        #     else:
        #         self.f_teams.append(TeamBox(parent=self, controller=self, team=i+1))
        #         self.f_teams[i].grid(row=3, column=i*3, columnspan=3, padx=10, pady=5, sticky="nsew")
        #
        # # initialize helpful tips box
        # if "Random" not in self.mode:
        #     self.helpbox = HelpBox(parent=self, controller=self)
        #     if "Ban" in self.mode:
        #         self.helpbox.grid(row=5, column=0, columnspan=6, pady=10)
        #     else:
        #         self.helpbox.grid(row=4, column=0, columnspan=6, pady=10)
        #
        # # initialize settings side bar
        # self.settings = SettingsBar(parent=self, controller=self)
        # self.settings.grid(row=0, column=7, rowspan=8, sticky="n")

    def playCPU(self):
        if self.vscpu.get():
            self.f_teams[1].l_team.config(image=self.f_teams[1].img_cpu_team[0])
        else:
            self.f_teams[1].l_team.config(image=self.f_teams[1].img_team[0])

    def blindMode(self):
        if self.activated:
            for i in range(18):
                if self.pokemonNotPicked[i]:
                    if self.blind.get():
                        self.b_icons[i].config(image=self.img_pokemonIcons[i][4])
                    else:
                        self.b_icons[i].config(image=self.img_pokemonIcons[i][0])
                else:
                    self.b_icons[i].config(image=self.img_pokemonIcons[i][2])

    def showMegas(self):
        if self.activated:
            for i in range(18):
                if self.pokemonList[i].item.endswith("ite") and self.pokemonList[i].item != "Eviolite":
                    for j in range(5):
                        if self.show_megas.get():
                            self.img_pokemonBase[i][j].paste(self.img_border_mega, (0, 0), self.img_border_mega)
                        else:
                            self.img_pokemonBase[i][j].paste(self.img_border, (0, 0), self.img_border)
                        self.img_pokemonIcons[i][j] = ImageTk.PhotoImage(self.img_pokemonBase[i][j])
                        if self.pokemonNotPicked[i]:
                            if self.blind.get():
                                self.b_icons[i].config(image=self.img_pokemonIcons[i][4])
                            else:
                                self.b_icons[i].config(image=self.img_pokemonIcons[i][0])
                        else:
                            self.b_icons[i].config(image=self.img_pokemonIcons[i][2])
                            for k in range(2):
                                for m in range(6):
                                    if self.f_teams[k].team_list[m] == self.pokemonList[i].name:
                                        self.f_teams[k].b_team_pokemon[m].config(image=self.img_pokemonIcons[i][0])
                                        break

    def activate(self):
        # # reset settings
        # self.activated = True
        # self.turn = 0
        # self.pokemonList = []
        # counter = 0
        # excludeTiers = []
        # for i in range(len(self.settings.tierExcludes)):
        #     if self.settings.tierExcludes[i].get() != "":
        #         excludeTiers.append(self.settings.tierExcludes[i].get())
        #
        # # pick new pokemon
        # while counter < 18:
        #     newPokemon = random.choice(ALL_POKEMON)
        #     if not self.pokemonList:
        #         self.pokemonList.append(newPokemon)
        #         counter += 1
        #     else:
        #         # check if pokemon should not be added
        #         add = True
        #         if newPokemon.name in (pkmn.name for pkmn in self.pokemonList):
        #             add = False
        #         if newPokemon.tier in excludeTiers:
        #             add = False
        #         if add:
        #             self.pokemonList.append(newPokemon)
        #             counter += 1
        # # reset all button functionality
        # self.pokemonNotPicked[i] = True
        # if self.blind.get():
        #     self.b_icons[i].config(image=self.img_pokemonIcons[i][4], command=lambda i=i: self.pickPokemon(i))
        # else:
        #     self.b_icons[i].config(image=self.img_pokemonIcons[i][0], command=lambda i=i: self.pickPokemon(i))

        # # clear teams
        # for i in range(2):
        #     self.f_teams[i].reset_team()
        #
        # # get list of counters for each pokemon
        # self.helpbox.counter_pokemon = [[] for j in range(18)]
        # for j in range(18):
        #     for k in range(18):
        #         if j != k:
        #             if type_logic(self.pokemonList[k], self.pokemonList[j]):
        #                 self.helpbox.counter_pokemon[j].append(self.pokemonList[k].name)
        # for counters in self.helpbox.counter_pokemon:
        #     shuffle(counters)

        # get pokemon icons
        self.img_pokemonBase = [[] for i in range(18)]
        self.img_pokemonIcons = [[] for i in range(18)]
        for i in range(18):
            for j in range(5):
                self.img_pokemonBase[i].append(RGBAImage('media\\{0}_{1}.png'.format(self.pokemonList[i].name, IMGTYPE[j])))
                if self.show_megas.get():
                    if self.pokemonList[i].item.endswith("ite") and self.pokemonList[i].item != "Eviolite":
                        self.img_pokemonBase[i][j].paste(self.img_border_mega, (0, 0), self.img_border_mega)
                    else:
                        self.img_pokemonBase[i][j].paste(self.img_border, (0, 0), self.img_border)
                else:
                    self.img_pokemonBase[i][j].paste(self.img_border, (0, 0), self.img_border)
                self.img_pokemonIcons[i].append(ImageTk.PhotoImage(self.img_pokemonBase[i][j]))

    def fade_in(self, i, button1, button2):
        if self.alpha > 1.0:
            # reset alpha value for next use and disable button
            self.alpha = 0
            self.b_icons[i].config(command=None)
        else:
            # create the interpolated images using the current alpha value
            if self.blind.get():
                self.new_img = ImageTk.PhotoImage(Image.blend(self.img_pokemonBase[i][4], self.img_pokemonBase[i][2], self.alpha))
            else:
                self.new_img = ImageTk.PhotoImage(Image.blend(self.img_pokemonBase[i][1], self.img_pokemonBase[i][2], self.alpha))
            if button2:
                self.new_img2 = ImageTk.PhotoImage(Image.blend(self.img_inactive_Blank_base, self.img_pokemonBase[i][0], self.alpha))
            self.alpha = self.alpha + 0.1
            # update the images displayed continuously to create fade in effect
            button1.config(image=self.new_img)
            button1.image = self.new_img
            if button2:
                button2.config(image=self.new_img2)
                button2.image = self.new_img2
            # loop until fade is complete
            self.after(10, self.fade_in, i, button1, button2)

    def pickPokemon(self, pool_slot_num):
        if self.pokemonNotPicked[pool_slot_num]:
            if self.turn <= 11:
                self.pokemonNotPicked[pool_slot_num] = False
                self.f_teams[self.turn%2].addToTeam(pool_slot_num, self.turn)
                self.fade_in(pool_slot_num, self.b_icons[pool_slot_num], self.f_teams[(self.turn)%2].b_team_pokemon[int(self.turn/2)])
                team_num = self.turn%2
                team_slot_num = int(self.turn/2)
                self.f_teams[team_num].b_team_pokemon[team_slot_num].config(command=lambda pool_slot_num=pool_slot_num, team_num=team_num, team_slot_num=team_slot_num: self.f_teams[team_num].removeFromTeam(team_slot_num, pool_slot_num))
                nextTurn = 0
                for i in range(12):
                    if self.f_teams[i%2].team_list[int(i/2)] == None:
                        break
                    else:
                        nextTurn += 1
                self.turn = nextTurn


    def on_enter(self, i):
        if self.activated:
            if self.pokemonNotPicked[i]:
                if not self.blind.get():
                    self.b_icons[i].config(image=self.img_pokemonIcons[i][1])
            self.helpbox.update_pool_info(i)
        else:
            self.b_icons[i].config(image=self.img_active_Blank)

    def on_leave(self, i):
        if self.activated:
            if self.pokemonNotPicked[i]:
                if not self.blind.get():
                    self.b_icons[i].config(image=self.img_pokemonIcons[i][0])
            self.helpbox.hide_info()
        else:
            self.b_icons[i].config(image=self.img_inactive_Blank)
