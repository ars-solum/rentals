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

class HelpBox(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.img_empty = ImageTk.PhotoImage(RGBAImage('media\\empty_pokemon.png'))

        self.container = []
        for i in range(3):
            self.container.append(tk.Frame(self))
            self.container[i].grid(row=0, column=i, padx=5)

        self.l_pokemon_name = tk.Label(self.container[0], text="", width=15)
        self.l_pokemon_selected = tk.Label(self.container[0], image=self.img_empty)
        self.l_pokemon_name.grid(row=0, column=0, sticky="nsew")
        self.l_pokemon_selected.grid(row=1, column=0, sticky="nsew")

        self.l_possibleAbility = tk.Label(self.container[1], text="")
        self.l_possibleAbilities = tk.Label(self.container[1], text="", width=15)
        self.l_possibleAbility.grid(row=0, column=0, sticky="n")
        self.l_possibleAbilities.grid(row=1, column=0, sticky="n")

        self.l_counterpick = tk.Label(self.container[2], text="")
        self.l_counterpick.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.l_counters = []
        for i in range(3):
            self.l_counters.append(tk.Label(self.container[2], image=self.img_empty))
            self.l_counters[i].grid(row=1, column=i, padx=5, sticky="nsew")
        self.counter_pokemon = [[] for j in range(18)]

    def update_pool_info(self, i):
        if self.controller.assist.get():
            self.l_pokemon_name.config(text=self.controller.pokemonList[i].name)
            abilities = ABILITIES[self.controller.pokemonList[i].name]
            while len(abilities) < 3:
                abilities.append("")
            t_abilities = ""
            for x in range(3):
                if x < 2:
                    t_abilities += abilities[x] + "\n"
                else:
                    t_abilities += abilities[x]
            self.l_possibleAbilities.config(text=t_abilities)
            for j in range(len(self.counter_pokemon[i])):
                if j > 2:
                    break
                for k in range(18):
                    if self.counter_pokemon[i][j] == self.controller.pokemonList[k].name:
                        x = k
                        break
                self.l_counters[j].config(image=self.controller.img_pokemonIcons[x][0])
            self.l_possibleAbility.config(text="Possible Abilities:")
            self.l_counterpick.config(text="Struggles Against:")
            self.l_pokemon_selected.config(image=self.controller.img_pokemonIcons[i][0])

    def update_team_info(self, team, i):
        if self.controller.assist.get():
            if self.controller.f_teams[team].team_list[i]:

                self.l_pokemon_name.config(text=self.controller.f_teams[team].team_list[i])

                abilities = ABILITIES[self.controller.f_teams[team].team_list[i]]
                while len(abilities) < 3:
                    abilities.append("")
                t_abilities = ""
                for x in range(3):
                    if x < 2:
                        t_abilities += abilities[x] + "\n"
                    else:
                        t_abilities += abilities[x]
                self.l_possibleAbilities.config(text=t_abilities)
                x = self.controller.f_teams[team].find_pokemon(i)
                for j in range(len(self.counter_pokemon[x])):
                    if j > 2:
                        break
                    for k in range(18):
                        if self.counter_pokemon[x][j] == self.controller.pokemonList[k].name:
                            y = k
                            break
                    self.l_counters[j].config(image=self.controller.img_pokemonIcons[y][0])

                self.l_possibleAbility.config(text="Possible Abilities:")
                self.l_counterpick.config(text="Struggles Against:")
                self.l_pokemon_selected.config(image=self.controller.img_pokemonIcons[x][0])


    def hide_info(self):
        if self.controller.assist.get():
            self.l_pokemon_name.config(text="")
            self.l_pokemon_selected.config(image=self.img_empty)
            self.l_possibleAbility.config(text="")
            self.l_possibleAbilities.config(text="")
            self.l_counterpick.config(text="")
            for i in range(3):
                self.l_counters[i].config(image=self.img_empty)
