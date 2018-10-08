try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

import os
import csv
import time
import random
from random import shuffle

DBLEN = 2797
FONT = ("Verdana", 12)
B_WIDTH = 15
BATTLE_OPTIONS = ["Standard Draft", "Random Battle", "Nemesis Draft", "First Pick Draft"]
AUCTION_OPTIONS = ["Trainers", "Auctions", "Leaderboards", "Prizes"]

class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

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

        for F in (StandardDraft, RandomBattle, NemesisDraft, FirstPickDraft,
                    Trainers, Auctions, Leaderboards, Prizes):
            page_name = F.__name__
            frame = F(parent=f_container, controller=self)
            self.containerFrames[page_name] = frame
            frame.grid(row=0, column=1, rowspan=4, sticky="nsew")

        self.show_frame("StandardDraft")
        self.sidebar.set_selected(BATTLE_OPTIONS[0].replace(" ", ""))

    def show_frame(self, page_name):
        self.sidebar.set_selected(page_name)
        self.sidebar.update_imgs()
        frame = self.containerFrames[page_name]
        frame.tkraise()

class Sidebar(tk.Frame):
    ##################################
    ##### setup the sidebar menu #####
    ##################################
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # initialize "private" variables
        self.currSelected = None
        self.prevSelected = None
        self.f_menuOptions = []
        self.b_battleOptions = []
        self.b_auctionOptions = []
        self.img_selected_button = []
        self.img_active_button = []
        self.img_inactive_button = []
        self.img_battleModes = tk.PhotoImage(file='imgs\\battle_formats.gif')

        for i in range(2):
            self.f_menuOptions.append(tk.Frame(self))
            self.f_menuOptions[i].grid(row=i, column=0, sticky="nsew")

        self.l_battleModes = tk.Label(self.f_menuOptions[0], image=self.img_battleModes)
        self.l_auctionModes = tk.Label(self.f_menuOptions[1], text="Auction Options", width=B_WIDTH, font=FONT)

        self.l_battleModes.image = self.img_battleModes
        self.l_battleModes.grid(row=0, column=0)

        for i in range(4):
            self.img_selected_button.append(tk.PhotoImage(file='imgs\\button_selected_{0}.gif'.format(BATTLE_OPTIONS[i].replace(" ", ""))))
            self.img_active_button.append(tk.PhotoImage(file='imgs\\button_active_{0}.gif'.format(BATTLE_OPTIONS[i].replace(" ", ""))))
            self.img_inactive_button.append(tk.PhotoImage(file='imgs\\button_inactive_{0}.gif'.format(BATTLE_OPTIONS[i].replace(" ", ""))))

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

    def update_imgs(self):
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
    def __init__(self, parent, controller, team):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.team = team

        img_team = tk.PhotoImage(file='imgs\\T{0}T_logo_inactive.gif'.format(team))
        l_team = tk.Label(self, image=img_team)
        l_team.grid(row=0, column=0, columnspan=3)
        l_team.image = img_team

        self.img_inactive_Blank = tk.PhotoImage(file='imgs\\button_inactive_Blank.gif')

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
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.img_pokemon_selected = tk.PhotoImage(file='imgs\\empty_pokemon.gif')

        self.container = []
        for i in range(3):
            self.container.append(tk.Frame(self))
            self.container[i].grid(row=0, column=i, padx=5)

        self.l_pokemon_name = tk.Label(self.container[0], text="")
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
            self.img_pokemon = tk.PhotoImage(file='imgs\\Bulbasaur_inactive.gif')

            self.l_pokemon_name.config(text="Bulbasaur")
            self.l_pokemon_selected.config(image=self.img_pokemon)
            self.l_pokemon_selected.image = self.img_pokemon
            self.l_possibleAbility.config(text="Possible Abilities:")
            self.l_possibleAbilities.config(text="Overgrow\nChlorophyll\nTEST")
            self.l_counterpick.config(text="Struggles Against:")
            for j in range(3):
                self.l_counters[j].config(image=self.img_pokemon)
                self.l_counters[j].image = self.img_pokemon

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

        self.img_settingsTitle = tk.PhotoImage(file='imgs\\label_settings_{0}.gif'.format(controller.__class__.__name__))

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
        self.pokemonNotPicked = True
        self.assist = tk.BooleanVar()
        self.assist.set(False)

        self.img_inactive_Blank = tk.PhotoImage(file='imgs\\button_inactive_Blank.gif')
        self.img_active_Blank = tk.PhotoImage(file='imgs\\button_active_Blank.gif')

        self.testicon = []
        self.testicon.append(tk.PhotoImage(file='imgs\\Bulbasaur_inactive.gif'))
        self.testicon.append(tk.PhotoImage(file='imgs\\Bulbasaur_active.gif'))
        self.testicon.append(tk.PhotoImage(file='imgs\\Bulbasaur_picked.gif'))

        self.b_testIcon = []
        for i in range(3):
            for j in range(6):
                x = (i*6)+j
                self.b_testIcon.append(tk.Button(self, image=self.img_inactive_Blank, bd=0.1, command=None))
                self.b_testIcon[x].grid(row=i, column=j, padx=5, pady=5)
                self.b_testIcon[x].image = self.img_inactive_Blank
                self.b_testIcon[x].bind("<Enter>", lambda event, x=x: self.on_enter(x))
                self.b_testIcon[x].bind("<Leave>", lambda event, x=x: self.on_leave(x))

        self.f_teams = []
        for i in range(2):
            frame = TeamBox(parent=self, controller=self, team=i+1)
            self.f_teams.append(frame)
            frame.grid(row=3, column=i*3, columnspan=3, pady=(30,0), sticky="nsew")

        self.helpbox = HelpBox(parent=self, controller=self)
        self.helpbox.grid(row=4, column=0, columnspan=6, pady=10)

        self.settings = SettingsBar(parent=self, controller=self)
        self.settings.grid(row=0, column=7, rowspan=8, sticky="n")


    def activate(self):
        self.activated = True
        self.pokemonNotPicked = True
        for i in range(2):
            self.b_testIcon[i].config(image=self.testicon[i], command=lambda: self.test(i))
            self.b_testIcon[i].image = self.testicon[i]

    def test(self, i):
        if self.pokemonNotPicked:
            self.b_testIcon[0].config(image=self.testicon[2])
            self.b_testIcon[0].image = self.testicon[2]
            self.pokemonNotPicked = False

    def on_enter(self, i):
        if self.activated:
            if i == 0:
                if self.pokemonNotPicked:
                    self.b_testIcon[0].config(image=self.testicon[1])
                    self.b_testIcon[0].image = self.testicon[1]

                self.helpbox.update_info(i)
            else:
                self.b_testIcon[i].config(image=self.img_active_Blank)
                self.b_testIcon[i].image = self.img_active_Blank
        else:
            self.b_testIcon[i].config(image=self.img_active_Blank)
            self.b_testIcon[i].image = self.img_active_Blank

    def on_leave(self, i):
        if self.activated:
            if i == 0:
                if self.pokemonNotPicked:
                    self.b_testIcon[0].config(image=self.testicon[0])
                    self.b_testIcon[0].image = self.testicon[0]
                self.helpbox.hide_info()
            else:
                self.b_testIcon[i].config(image=self.img_inactive_Blank)
                self.b_testIcon[i].image = self.img_inactive_Blank
        else:
            self.b_testIcon[i].config(image=self.img_inactive_Blank)
            self.b_testIcon[i].image = self.img_inactive_Blank

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
    app.mainloop()
