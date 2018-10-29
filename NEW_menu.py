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
from TypeChart import TypeChart, type_logic

BATTLE_OPTIONS = ["StandardDraft", "RandomBattle", "NemesisDraft", "BanDraft"]
AUCTION_OPTIONS = ["Trainers", "Auctions", "Leaderboards", "Prizes"]
IMGTYPE = ["inactive", "active", "picked", "banned", "unknown"]
ALL_POKEMON = []
ABILITIES = {}

def RGBAImage(path):
    return Image.open(path).convert("RGBA")

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

class Sidebar(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # initialize private variables
        self.currSelected = None
        self.prevSelected = None

        self.img_battleModes = ImageTk.PhotoImage(RGBAImage('media\\Common\\label_battle.png'))
        self.img_auctionModes = ImageTk.PhotoImage(RGBAImage('media\\Common\\label_auction.png'))

        # set up the menu buttons and images
        self.f_menuOptions = []
        for i in range(2):
            self.f_menuOptions.append(tk.Frame(self))
            self.f_menuOptions[i].grid(row=i, column=0, sticky="nsew")

        self.l_battleModes = tk.Label(self.f_menuOptions[0], image=self.img_battleModes)
        self.l_battleModes.grid(row=0, column=0, pady=5)

        self.img_selected_button = []
        self.img_inactive_button = []
        self.b_battleOptions = []
        for i in range(4):
            self.img_selected_button.append(ImageTk.PhotoImage(RGBAImage('media\\Common\\button_selected_{0}.png'.format(BATTLE_OPTIONS[i]))))
            self.img_inactive_button.append(ImageTk.PhotoImage(RGBAImage('media\\Common\\button_inactive_{0}.png'.format(BATTLE_OPTIONS[i]))))

            if i == 0:
                self.b_battleOptions.append(tk.Button(self.f_menuOptions[0], image=self.img_selected_button[i], bd=0.1,
                                                        command=lambda i=i: controller.show_frame(BATTLE_OPTIONS[i])))
                self.currSelected = BATTLE_OPTIONS[i]
            else:
                self.b_battleOptions.append(tk.Button(self.f_menuOptions[0], image=self.img_inactive_button[i], bd=0.1,
                                                        command=lambda i=i: controller.show_frame(BATTLE_OPTIONS[i])))
            self.b_battleOptions[i].grid(row=i+1, column=0)
            self.b_battleOptions[i].bind("<Enter>", lambda event, i=i: self.on_enter(i))
            self.b_battleOptions[i].bind("<Leave>", lambda event, i=i: self.on_leave(i))

        self.l_auctionModes = tk.Label(self.f_menuOptions[1], image=self.img_auctionModes)
        self.l_auctionModes.grid(row=0, column=0, pady=(20, 5))

        self.b_auctionOptions = []
        for i in range(4):
            self.img_selected_button.append(ImageTk.PhotoImage(RGBAImage('media\\Common\\button_selected_{0}.png'.format(AUCTION_OPTIONS[i]))))
            self.img_inactive_button.append(ImageTk.PhotoImage(RGBAImage('media\\Common\\button_inactive_{0}.png'.format(AUCTION_OPTIONS[i]))))

            self.b_auctionOptions.append(tk.Button(self.f_menuOptions[1], image=self.img_inactive_button[i+4], bd=0.1,
                                                command=lambda i=i: controller.show_frame(AUCTION_OPTIONS[i])))
            self.b_auctionOptions[i].grid(row=i+1, column=0)
            self.b_auctionOptions[i].bind("<Enter>", lambda event, i=i: self.on_enter(i+4))
            self.b_auctionOptions[i].bind("<Leave>", lambda event, i=i: self.on_leave(i+4))

    def on_enter(self, option):
        if option < 4:
            if self.currSelected == BATTLE_OPTIONS[option]:
                pass
            else:
                self.b_battleOptions[option].config(image=self.img_selected_button[option])
        else:
            if self.currSelected == AUCTION_OPTIONS[option-4]:
                pass
            else:
                self.b_auctionOptions[option-4].config(image=self.img_selected_button[option])

    def on_leave(self, option):
        if option < 4:
            if self.currSelected == BATTLE_OPTIONS[option]:
                self.b_battleOptions[option].config(image=self.img_selected_button[option])
            else:
                self.b_battleOptions[option].config(image=self.img_inactive_button[option])
        else:
            if self.currSelected == AUCTION_OPTIONS[option-4]:
                self.b_auctionOptions[option-4].config(image=self.img_selected_button[option])
            else:
                self.b_auctionOptions[option-4].config(image=self.img_inactive_button[option])

    def set_selected(self, mode):
        self.prevSelected = self.currSelected
        self.currSelected = mode

    def get_currSelected(self):
        return self.currSelected

    def get_prevSelected(self):
        return self.prevSelected

    def update_media(self):
        if self.currSelected != self.prevSelected:
            for i in range(4):
                if self.prevSelected == BATTLE_OPTIONS[i]:
                    self.b_battleOptions[i].config(image=self.img_inactive_button[i])
                    break
                if self.prevSelected == AUCTION_OPTIONS[i]:
                    self.b_auctionOptions[i].config(image=self.img_inactive_button[i+4])
                    break
        else:
            for i in range(4):
                if self.currSelected == BATTLE_OPTIONS[i]:
                    self.b_battleOptions[i].config(image=self.img_selected_button[i])
                    break
                if self.currSelected == AUCTION_OPTIONS[i]:
                    self.b_auctionOptions[i].config(image=self.img_selected_button[i+4])
                    break

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

class SettingsBar(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.img_settingsTitle = ImageTk.PhotoImage(RGBAImage('media\\Common\\label_settings_{0}2.png'.format(self.controller.mode)))

        self.l_settingsTitle = tk.Label(self, image=self.img_settingsTitle)
        self.l_settingsTitle.grid(row=0, column=0, columnspan=3)

        self.l_generate = tk.Label(self, text="Pokémon Appearance")
        self.l_generate.grid(row=1, column=0, columnspan=2, sticky="w")
        #tritype
        self.optionsRandom = ["Random (default)", 0, "Balanced", 1, "Skewed", 2]
        self.randomness = tk.IntVar()
        self.b_randomness = []
        for i in range(3):
            self.b_randomness.append(tk.Radiobutton(self, text=self.optionsRandom[i*2], variable=self.randomness, value=self.optionsRandom[(i*2)+1]))
            self.b_randomness[i].grid(row=i+2, column=0, padx=20, columnspan=2, sticky="w")


        if "Random" not in self.controller.mode:
            self.l_turn = tk.Label(self, text="Turn Order")
            self.l_turn.grid(row=5, column=0, columnspan=2, sticky="w")
            self.optionsTurnOrder = ["Sequential (default)", 0, "First Pick", 1, "Random", 2]
            self.turnOrder = tk.IntVar()
            self.b_turns = []
            for i in range(3):
                self.b_turns.append(tk.Radiobutton(self, text=self.optionsTurnOrder[i*2], variable=self.turnOrder, value=self.optionsTurnOrder[(i*2)+1]))
                self.b_turns[i].grid(row=i+6, column=0, padx=20, columnspan=2, sticky="w")


        if "Ban" in self.controller.mode:
            self.l_bans = tk.Label(self, text="Number of Bans")
            self.l_bans.grid(row=9, column=0, columnspan=2, sticky="w")

            self.optionsBans = ["One (default)", 1, "Two", 2, "Three", 3]
            self.bans = tk.IntVar(value=1)
            self.b_bans = []
            for i in range(3):
                self.b_bans.append(tk.Radiobutton(self, text=self.optionsBans[i*2], variable=self.bans, value=self.optionsBans[(i*2)+1]))
                self.b_bans[i].grid(row=i+10, column=0, columnspan=2, padx=20, sticky="w")


        self.l_exclude = tk.Label(self, text="Exclusions")
        self.l_exclude.grid(row=13, column=0, columnspan=1, sticky="w")
        #self.b_moreExcludes = tk.Button(self, text=">", command=lambda: self.moreExcludes(1))
        #self.b_moreExcludes.grid(row=13, column=1, columnspan=1, sticky="w")
        self.optionsExcludeTiers = ["Ubers", "OU", "UU", "RU", "NU", "PU", "NFE"]
        self.optionsExcludeRegions = ["Kanto", "Johto", "Hoenn", "Sinnoh", "Unova", "Kalos", "Alola"]
        self.tierExcludes = [tk.StringVar() for i in range(7)]
        self.regionExcludes = [tk.StringVar() for i in range(7)]
        self.typeExcludes = [tk.StringVar() for i in range(7)]
        self.b_tierExcludes = []
        self.b_regionExcludes = []
        self.b_typeExcludes = []
        for i in range(7):
            self.b_tierExcludes.append(tk.Checkbutton(self, text=self.optionsExcludeTiers[i], variable=self.tierExcludes[i], onvalue=self.optionsExcludeTiers[i], offvalue=""))
            if i%2 == 0:
                self.b_tierExcludes[i].grid(row=i+14, column=0, padx=(20, 0), sticky="w")
            else:
                self.b_tierExcludes[i].grid(row=i+13, column=1, sticky="w")

        if "Random" not in self.controller.mode:
            self.l_other = tk.Label(self, text="Other Options")
            self.l_other.grid(row=21, column=0, columnspan=2, sticky="w")
            self.b_assist = tk.Checkbutton(self, text="Show Basic Tips", variable=self.controller.assist)
            self.b_assist.grid(row=22, column=0, columnspan=2, padx=(20, 0), sticky="w")
            self.b_vscpu = tk.Checkbutton(self, text="Play Against CPU", variable=self.controller.vscpu, command=lambda: self.controller.playCPU())
            self.b_vscpu.grid(row=23, column=0, columnspan=2, padx=(20, 0), sticky="w")
            self.b_blind = tk.Checkbutton(self, text="Blind Mode", variable=self.controller.blind, command=lambda: self.controller.blindMode())
            self.b_blind.grid(row=24, column=0, columnspan=2, padx=(20, 0), sticky="w")


        self.goButton = tk.Button(self, text="Go", command=lambda: self.controller.activate())
        self.goButton.grid(row=25, column=0, padx=5, pady=5)

    def moreExcludes(self, page):
        for i in range(7):
            self.b_tierExcludes[i].grid_forget()

class Battle(tk.Frame):
    def __init__(self, parent, controller, mode):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.mode = mode

        # initialize variables and images
        self.alpha = 0
        self.turn = 0
        self.activated = False
        self.pokemonNotPicked = [True for i in range(18)]

        self.assist = tk.BooleanVar()
        self.assist.set(False)
        self.vscpu = tk.BooleanVar()
        self.vscpu.set(False)
        self.blind = tk.BooleanVar()
        self.blind.set(False)

        self.img_border = RGBAImage('media\\border_%s.png' % self.mode)
        self.img_inactive_Blank_base = RGBAImage('media\\button_inactive_Blank.png')
        self.img_active_Blank_base = RGBAImage('media\\button_active_Blank.png')
        self.img_inactive_Blank_base.paste(self.img_border, (0, 0), self.img_border)
        self.img_active_Blank_base.paste(self.img_border, (0, 0), self.img_border)
        self.img_inactive_Blank = ImageTk.PhotoImage(self.img_inactive_Blank_base)
        self.img_active_Blank = ImageTk.PhotoImage(self.img_active_Blank_base)

        # initialize pool of pokemon buttons
        if "Random" not in self.mode:
            self.b_icons = []
            self.img_pokemon = [[] for i in range(18)]
            for i in range(3):
                for j in range(6):
                    x = (i*6)+j
                    self.b_icons.append(tk.Button(self, image=self.img_inactive_Blank, bd=0.1, command=None))
                    self.b_icons[x].grid(row=i, column=j, padx=5, pady=5)
                    self.b_icons[x].bind("<Enter>", lambda event, x=x: self.on_enter(x))
                    self.b_icons[x].bind("<Leave>", lambda event, x=x: self.on_leave(x))

        # initialize team boxes
        self.f_teams = []
        if "Ban" in self.mode:
            self.f_bans = []
        for i in range(2):
            if "Ban" in self.mode:
                self.f_bans.append(BanBox(parent=self, controller=self, team=i+1))
                self.f_bans[i].grid(row=3, column=i*3, columnspan=3, sticky="nsew")
                self.f_teams.append(TeamBox(parent=self, controller=self, team=i+1))
                self.f_teams[i].grid(row=4, column=i*3, columnspan=3, sticky="nsew")
            else:
                self.f_teams.append(TeamBox(parent=self, controller=self, team=i+1))
                self.f_teams[i].grid(row=3, column=i*3, columnspan=3, sticky="nsew")

        # initialize helpful tips box
        if "Random" not in self.mode:
            self.helpbox = HelpBox(parent=self, controller=self)
            if "Ban" in self.mode:
                self.helpbox.grid(row=5, column=0, columnspan=6, pady=10)
            else:
                self.helpbox.grid(row=4, column=0, columnspan=6, pady=10)

        # initialize settings side bar
        self.settings = SettingsBar(parent=self, controller=self)
        self.settings.grid(row=0, column=7, rowspan=8, sticky="n")

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

    def activate(self):
        # reset settings
        self.activated = True
        self.turn = 0
        self.pokemonList = []
        counter = 0
        excludeTiers = []
        for i in range(len(self.settings.tierExcludes)):
            if self.settings.tierExcludes[i].get() != "":
                excludeTiers.append(self.settings.tierExcludes[i].get())

        # pick new pokemon
        while counter < 18:
            newPokemon = random.choice(ALL_POKEMON)
            if not self.pokemonList:
                self.pokemonList.append(newPokemon)
                counter += 1
            else:
                # check if pokemon already picked
                add = True
                names = []
                for i in range(len(self.pokemonList)):
                    names.append(self.pokemonList[i].name)
                if newPokemon.name in names:
                    add = False
                if newPokemon.tier in excludeTiers:
                    add = False
                if add:
                    self.pokemonList.append(newPokemon)
                    counter += 1

        # get pokemon icons
        self.img_pokemonBase = [[] for i in range(18)]
        self.img_pokemonIcons = [[] for i in range(18)]
        for i in range(18):
            for j in range(5):
                self.img_pokemonBase[i].append(RGBAImage('media\\{0}_{1}.png'.format(self.pokemonList[i].name, IMGTYPE[j])))
                self.img_pokemonBase[i][j].paste(self.img_border, (0, 0), self.img_border)
                self.img_pokemonIcons[i].append(ImageTk.PhotoImage(self.img_pokemonBase[i][j]))
            # reset all button functionality
            self.pokemonNotPicked[i] = True
            if self.blind.get():
                self.b_icons[i].config(image=self.img_pokemonIcons[i][4], command=lambda i=i: self.pickPokemon(i))
            else:
                self.b_icons[i].config(image=self.img_pokemonIcons[i][0], command=lambda i=i: self.pickPokemon(i))

        # clear teams
        for i in range(2):
            self.f_teams[i].reset_team()

        # get list of counters for each pokemon
        self.helpbox.counter_pokemon = [[] for j in range(18)]
        for j in range(18):
            for k in range(18):
                if j != k:
                    if type_logic(self.pokemonList[k], self.pokemonList[j]):
                        self.helpbox.counter_pokemon[j].append(self.pokemonList[k].name)
        for counters in self.helpbox.counter_pokemon:
            shuffle(counters)

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
    with open('main_database.csv', 'r') as fileName:
        reader = csv.reader(fileName)
        next(reader, None)
        for row in reader:
            if row[1] == "Furret":
                break
            else:
                ALL_POKEMON.append(Pokemon(row))
    with open('Abilities.csv', 'r') as fileName:
        reader = csv.reader(fileName)
        for row in reader:
            ABILITIES[row[0]] = [row[x] for x in range(1,4) if row[x] != '']
    app.mainloop()
