try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk
from PIL import Image, ImageTk
from RGBAImage import RGBAImage

from Pokemon import Pokemon, ALL_POKEMON, ABILITIES
from TypeChart import TypeChart, type_logic

BATTLE_OPTIONS = ["StandardDraft", "RandomBattle", "NemesisDraft", "BanDraft"]
AUCTION_OPTIONS = ["Trainers", "Auctions", "Leaderboards", "Prizes"]
IMGTYPE = ["inactive", "active", "picked", "banned", "unknown"]

class TeamBox(tk.Frame):
    def __init__(self, parent, controller, team):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.team = team

        self.img_team = []
        for i in range(2):
            self.img_team.append(ImageTk.PhotoImage(RGBAImage('media\\Common\\T{0}T_logo_{1}.png'.format(self.team, IMGTYPE[i]))))
        if self.team == 2:
            self.img_cpu_team = []
            for i in range(2):
                self.img_cpu_team.append(ImageTk.PhotoImage(RGBAImage('media\\Common\\T3T_logo_{0}.png'.format(IMGTYPE[i]))))
        self.l_team = tk.Label(self, image=self.img_team[0])
        self.l_team.grid(row=0, column=0, columnspan=3)

        self.b_team_pokemon = []
        for row in range(3):
            for column in range(2):
                x = (row*2)+column
                self.b_team_pokemon.append(tk.Button(self, image=self.controller.img_inactive_Blank, bd=0.1, command=None))
                self.b_team_pokemon[x].grid(row=row+1, column=column, sticky="e")
                self.b_team_pokemon[x].bind("<Enter>", lambda event, x=x: self.on_enter(x))
                self.b_team_pokemon[x].bind("<Leave>", lambda event, x=x: self.on_leave(x))

        self.team_list = [None for i in range(6)]

    def reset_team(self):
        for pkmn in range(6):
            self.team_list[pkmn] = None
            self.b_team_pokemon[pkmn].config(image=self.controller.img_inactive_Blank, command=None)

    def find_pokemon(self, team_slot_num):
        for i in range(18):
            if self.team_list[team_slot_num] == self.controller.pokemonList[i].name:
                x = i
                break
        return x

    def on_enter(self, team_slot_num):
        if self.team_list[team_slot_num]:
            x = self.find_pokemon(team_slot_num)
            self.b_team_pokemon[team_slot_num].config(image=self.controller.img_pokemonIcons[x][1])
        else:
            self.b_team_pokemon[team_slot_num].config(image=self.controller.img_active_Blank)
        if "Random" not in self.controller.mode:
            self.controller.helpbox.update_team_info(self.team-1, team_slot_num)

    def on_leave(self, team_slot_num):
        if not self.team_list[team_slot_num]:
            self.b_team_pokemon[team_slot_num].config(image=self.controller.img_inactive_Blank)
        else:
            x = self.find_pokemon(team_slot_num)
            self.b_team_pokemon[team_slot_num].config(image=self.controller.img_pokemonIcons[x][0])
        if "Random" not in self.controller.mode:
            self.controller.helpbox.hide_info()

    def addToTeam(self, pool_slot_num, turn):
        if self.team_list[int(turn/2)] == None:
            self.team_list[int(turn/2)] = self.controller.pokemonList[pool_slot_num].name
            self.b_team_pokemon[int(turn/2)].config(image=self.controller.img_pokemonIcons[pool_slot_num][0])
            print(self.team_list)

    def removeFromTeam(self, team_slot_num, pool_slot_num):
        print(self.team_list)

        if self.team_list[team_slot_num]:
            print("hi3")
            self.team_list[team_slot_num] = None
            self.b_team_pokemon[team_slot_num].config(image=self.controller.img_active_Blank, command=None)
