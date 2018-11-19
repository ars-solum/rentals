try:
    import tkinter as tk
except:
    import Tkinter as tk
import random
import os
import csv
# from PIL import Image, ImageTk
# from RGBAImage import RGBAImage

pkmn_list = [[] for i in range(1)]

class Pokemon:
    def __init__(self, row):
        self.name = str(row[0])
        self.type = [str(row[1]), str(row[2])]
        self.tier = str(row[3])
        self.rarity = str(row[4])

banners = ['gof1.csv']

banName = ['Guardians of the Forest 1']

fileDir = os.path.dirname(os.path.realpath('__file__'))
for i in range(1):
    filename = os.path.join(fileDir, 'banners/' + banners[i])
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            pkmn_list[i].append(Pokemon(row))

numpokes = []
for i in range(1):
    numpokes.append(len(pkmn_list[i]))

num_common = [0 for i in range(1)]
num_rare = [0 for i in range(1)]
num_ultra = [0 for i in range(1)]
for i in range(1):
    for j in pkmn_list[i]:
        if j.rarity == "COMMON":
            num_common[i] += 1
        if j.rarity == "RARE":
            num_rare[i] += 1
        if j.rarity == "ULTRA-RARE":
            num_ultra[i] += 1

prob_common = []
prob_rare = []
prob_ultra = []

for i in range(1):
    prob_common.append(0.8500 / num_common[i] * 100)
    prob_rare.append(0.1100 / num_rare[i] * 100)
    prob_ultra.append(0.0400 / num_ultra[i] * 100)

class Player:
    def __init__(self, name, jewels=0, team=[], pulls=[3 for i in range(1)]):
        self.name = name
        self.team = team
        self.jewels = jewels
        for i in range(len(pulls)):
            pulls[i] = int(pulls[i])
        self.numPullsUntil = pulls

    def addJewels(self, jewels):
        self.jewels += jewels
    def removeJewels(self, jewels):
        self.jewels -= jewels
    def setJewels(self, jewels):
        self.jewels = jewels

playerNames = ['Daniel', 'Jake', 'Yasmin']
player_list = []
for player in playerNames:
    filename = os.path.join(fileDir, 'players/' + player + '.csv')
    try:
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            currJewels = int(next(reader)[0])
            currPulls = next(reader)
            currTeam = []
            for row in reader:
                newPokemon = Pokemon(row)
                currTeam.append(newPokemon)
            currPlayer = Player(player, currJewels, currTeam, currPulls)
        player_list.append(currPlayer)
    except:
        with open(filename, 'w') as file:
            #writer = csv.DictWriter(file, lineterminator='\n')
            #writer = csv.writer(file, delimiter=',')
            writer = csv.writer(file, delimiter=',', lineterminator='\n')
            writer.writerow(["3000"])
        player_list.append(Player(player, 3000))

def getPlayer(playername):
    for player in player_list:
        if player.name == playername:
            return player

class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.bannerNum = 0
        self.currentPlayer = tk.StringVar(self)
        self.currentPlayer.set(playerNames[0])
        self.names = ['Zygarde']

        buttons = []
        for i in range(3):
            if i < 2:
                buttons.append(tk.Button(self, text="Pull %d Pokemon" % ((i+1)*3), command=lambda i=i: self.choose((i+1)*300, (i+1)*3)))
            else:
                buttons.append(tk.Button(self, text="Pull %d Pokemon" % ((i+1)*4), command=lambda i=i: self.choose((i+1)*400, (i+1)*4)))
            buttons[i].grid(row=0, column=i)

        self.label = tk.Label(self, text="Get %s within %d more 12-pulls!" %(self.names[self.bannerNum], getPlayer(self.currentPlayer.get()).numPullsUntil[self.bannerNum]), font=('Verdana', 16))
        self.label.grid(row=15, column=0, columnspan=3, pady=5)


        self.frame = tk.LabelFrame(self, text="Banner Info")
        self.frame.grid(row=1, column=0, rowspan=13, columnspan=3)
        texttop = "%15s | %10s | %6s" %("Pokemon", "Rarity", "Pull Rate")
        self.infotop = []
        for i in range(3):
            self.infotop.append(tk.Label(self.frame, text="%s" % texttop))
            self.infotop[i].grid(row=0, column=i, sticky="e")
        self.info = []
        for i in range(numpokes[self.bannerNum]):
            if pkmn_list[self.bannerNum][i].rarity == "COMMON":
                prob = prob_common[self.bannerNum]
            elif pkmn_list[self.bannerNum][i].rarity == "RARE":
                prob = prob_rare[self.bannerNum]
            else:
                prob = prob_ultra[self.bannerNum]
            text = "%15s | %10s | %.3f %%" %(pkmn_list[self.bannerNum][i].name, pkmn_list[self.bannerNum][i].rarity, prob)
            self.info.append(tk.Label(self.frame, text=text))
            self.info[i].grid(row=(i%13)+1, column=int(i/13), sticky="e")

        self.addJewels = tk.Button(self, text="Add 1000 Jewels", command=lambda: self.addJs(1000))
        self.addJewels.grid(row=18, column=0)
        self.dropdown = tk.OptionMenu(self, self.currentPlayer, *playerNames, command=self.updatePlayerInfo)
        self.dropdown.grid(row=18, column=1)
        self.jewelAmount = tk.Label(self, text=str(getPlayer(self.currentPlayer.get()).jewels) + " Jewels", font=('Monospace', 10))
        self.jewelAmount.grid(row=18, column=2)
        self.inventory = tk.Button(self, text="View Inventory", command=self.viewInventory)
        self.inventory.grid(row=19, column=1)

        # self.pullscreen = tk.Frame(self)
        # self.pullscreen.grid(row=0, column=3, rowspan=4, columnspan=3)
        # self.icons = []
        # for i in range(12):
        #     self.icons.append(tk.Label(self.pullscreen, image=))

    def viewInventory(self):
        self.inventoryMenu = tk.Toplevel()
        self.inventoryMenu.labels = []
        exit = tk.Button(self.inventoryMenu, text="Exit", command=self.inventoryMenu.destroy)
        exit.grid(row=0, column=2)
        sortA = tk.Button(self.inventoryMenu, text="Sort Alphabetically", command=lambda: self.sortAlpha(getPlayer(self.currentPlayer.get())))
        sortA.grid(row=0, column=0)
        sortB = tk.Button(self.inventoryMenu, text="Sort by Rarity", command=lambda: self.sortRare(getPlayer(self.currentPlayer.get())))
        sortB.grid(row=0, column=1)
        k = 0
        j = 0
        while k < len(getPlayer(self.currentPlayer.get()).team):
            k += 3
            j += 1
        for i in range(len(getPlayer(self.currentPlayer.get()).team)):
            self.inventoryMenu.labels.append(tk.Label(self.inventoryMenu, text="%15s   %10s" %(getPlayer(self.currentPlayer.get()).team[i].name, getPlayer(self.currentPlayer.get()).team[i].rarity), font=('Monospace', 10)))
            self.inventoryMenu.labels[i].grid(row=i%j+2, column=int(i/j), sticky="e")
        self.after(1000, self.updateInventory)
    def updateInventory(self):
        try:
            k = 0
            j = 0
            while k < len(getPlayer(self.currentPlayer.get()).team):
                k += 3
                j += 1
            for i in range(len(getPlayer(self.currentPlayer.get()).team)):
                try:
                    self.inventoryMenu.labels[i].config(text="%15s   %10s" %(getPlayer(self.currentPlayer.get()).team[i].name, getPlayer(self.currentPlayer.get()).team[i].rarity))
                    self.inventoryMenu.labels[i].grid(row=i%j+2, column=int(i/j), sticky="e")
                except IndexError:
                    self.inventoryMenu.labels.append(tk.Label(self.inventoryMenu, text="%15s   %10s" %(getPlayer(self.currentPlayer.get()).team[i].name, getPlayer(self.currentPlayer.get()).team[i].rarity), font=('Monospace', 10)))
                    self.inventoryMenu.labels[i].grid(row=i%j+2, column=int(i/j), sticky="e")
            self.after(1000, self.updateInventory)
        except tk.TclError:
            return

    def sortAlpha(self, player):
        getPlayer(self.currentPlayer.get()).team.sort(key=lambda x: x.name)
        for i in range(len(getPlayer(self.currentPlayer.get()).team)):
            self.inventoryMenu.labels[i].config(text="%15s   %10s" %(getPlayer(self.currentPlayer.get()).team[i].name, getPlayer(self.currentPlayer.get()).team[i].rarity))
    def sortRare(self, player):
        getPlayer(self.currentPlayer.get()).team.sort(key=lambda x: x.rarity)
        for i in range(len(getPlayer(self.currentPlayer.get()).team)):
            self.inventoryMenu.labels[i].config(text="%15s   %10s" %(getPlayer(self.currentPlayer.get()).team[i].name, getPlayer(self.currentPlayer.get()).team[i].rarity))
    def addJs(self, amount):
        getPlayer(self.currentPlayer.get()).addJewels(amount)
        self.jewelAmount.config(text=str(getPlayer(self.currentPlayer.get()).jewels) + " Jewels")
    def choose(self, jewels, numToChoose):
        pull = []
        if getPlayer(self.currentPlayer.get()).jewels - jewels >= 0:
            getPlayer(self.currentPlayer.get()).removeJewels(jewels)
            self.jewelAmount.config(text=str(getPlayer(self.currentPlayer.get()).jewels) + " Jewels")
            for i in range(numToChoose):
                if self.bannerNum > 13:
                    if numToChoose == 12 and (0 <= i <= 3):
                        rarity = random.randint(61, 100)
                    elif numToChoose == 6 and (0 <= i <= 1):
                        rarity = random.randint(61, 100)
                    elif numToChoose == 3 and i == 0:
                        rarity = random.randint(61, 100)
                    else:
                        rarity = random.randint(1, 100)
                    if rarity <= 60:
                        rarityChoose = "COMMON"
                    elif rarity > 60 and rarity <= 95:
                        rarityChoose = "RARE"
                    else:
                        rarityChoose = "ULTRA-RARE"
                else:
                    if numToChoose == 12 and i == 0:
                        rarity = random.randint(86, 100)
                    else:
                        rarity = random.randint(1, 100)
                    if rarity <= 85:
                        rarityChoose = "COMMON"
                    elif rarity > 85 and rarity <= 96:
                        rarityChoose = "RARE"
                    else:
                        rarityChoose = "ULTRA-RARE"
                pick = None
                while not pick:
                    pick = random.choice(pkmn_list[self.bannerNum])
                    # mercy pull
                    if numToChoose == 12 and i == 11 and self.bannerNum < 14:
                        for j in range(1):
                            if getPlayer(self.currentPlayer.get()).numPullsUntil[self.bannerNum] > 1 and self.bannerNum == j:
                                if pick.rarity != rarityChoose:
                                    pick = None
                                else:
                                    pull.append(pick)
                                break
                            if getPlayer(self.currentPlayer.get()).numPullsUntil[self.bannerNum] == 1 and pick.name != self.names[j] and self.bannerNum == j:
                                for k in range(len(pkmn_list[self.bannerNum])):
                                    if self.names[j] == pkmn_list[self.bannerNum][k].name:
                                         ind = k
                                         break
                                pick = pkmn_list[self.bannerNum][ind]
                                pull.append(pick)
                                break
                    else:
                        if pick.rarity != rarityChoose:
                            pick = None
                        else:
                            pull.append(pick)

            random.shuffle(pull)
            print("Pulling on %s..." %(banName[self.bannerNum]))
            print("-------------------------------------------------------")
            for i in range(len(pull)):
                print("(%2d)\t%17s\t[%s]" %(i+1, pull[i].name, pull[i].rarity))
                getPlayer(self.currentPlayer.get()).team.append(pull[i])
            print("-------------------------------------------------------\n")

            if numToChoose == 12:
                for i in range(1):
                    if i == self.bannerNum:
                        for pokemon in pull:
                            if pokemon.name == self.names[i]:
                                getPlayer(self.currentPlayer.get()).numPullsUntil[self.bannerNum] = 3
                                noMercy = False
                                break
                            else:
                                noMercy = True
                        if noMercy:
                            getPlayer(self.currentPlayer.get()).numPullsUntil[self.bannerNum] -= 1
                        self.label.config(text="Get %s within %d more 12-pulls!" % (self.names[i], getPlayer(self.currentPlayer.get()).numPullsUntil[self.bannerNum]))

            filename = os.path.join(fileDir, 'players/' + self.currentPlayer.get() + '.csv')
            with open(filename, 'w') as file:
                writer = csv.writer(file, delimiter=',', lineterminator='\n')
                writer.writerow([str(getPlayer(self.currentPlayer.get()).jewels)])
                writer.writerow(getPlayer(self.currentPlayer.get()).numPullsUntil)
                for pkm in getPlayer(self.currentPlayer.get()).team:
                    pk_list = []
                    pk_list.append(pkm.name)
                    pk_list.append(pkm.type[0])
                    pk_list.append(pkm.type[1])
                    pk_list.append(pkm.tier)
                    pk_list.append(pkm.rarity)
                    writer.writerow(pk_list)
        else:
            print("Not enough Jewels. This Player cannot pull!")
    def nextBanner(self, banNum):
        self.bannerNum = banNum
        for i in range(numpokes[self.bannerNum]):
            if pkmn_list[self.bannerNum][i].rarity == "COMMON":
                prob = prob_common[self.bannerNum]
            elif pkmn_list[self.bannerNum][i].rarity == "RARE":
                prob = prob_rare[self.bannerNum]
            else:
                prob = prob_ultra[self.bannerNum]
            text = "%15s | %10s | %.3f %%" %(pkmn_list[self.bannerNum][i].name, pkmn_list[self.bannerNum][i].rarity, prob)
            self.info[i].config(text=text)
        self.label.config(text="Get %s within %d more 12-pulls!" % (self.names[self.bannerNum], getPlayer(self.currentPlayer.get()).numPullsUntil[self.bannerNum]))
    def updatePlayerInfo(self, info):
        if self.bannerNum < 14:
            self.label.config(text="Get %s within %d more 12-pulls!" % (self.names[self.bannerNum], getPlayer(info).numPullsUntil[self.bannerNum]))
            self.jewelAmount.config(text=str(getPlayer(info).jewels) + " Jewels")

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
