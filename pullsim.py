import tkinter as tk
import random
import os
import csv
from PIL import Image, ImageTk
from RGBAImage import RGBAImage

pkmn_list = [[] for i in range(1)]

class Pokemon:
    def __init__(self, row):
        self.name = str(row[0])
        self.type = [str(row[1]), str(row[2])]
        self.tier = str(row[3])
        self.rarity = str(row[4])

banners = ['gof1.csv']

banName = ['Guardians of the Forest 1']

for i in range(1):
    with open(banners[i], 'r') as file:
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

class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.bannerNum = 0
        self.numPullsUntil = [3]

        buttons = []
        for i in range(3):
            if i < 2:
                buttons.append(tk.Button(self, text="Pull %d Pokemon" % ((i+1)*3), command=lambda i=i: self.choose((i+1)*3)))
            else:
                buttons.append(tk.Button(self, text="Pull %d Pokemon" % ((i+1)*4), command=lambda i=i: self.choose((i+1)*4)))
            buttons[i].grid(row=0, column=i)

        self.names = ['Zygarde']

        self.label = tk.Label(self, text="Get %s within %d more 12-pulls!" %(self.names[self.bannerNum], self.numPullsUntil[self.bannerNum]), font=('Verdana', 16))
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

        self.pullscreen = tk.Frame(self)
        self.pullscreen.grid(row=0, column=3, rowspan=4, columnspan=3)


        self.icons = []
        for i in range(12):
            self.icons.append(tk.Label(self.pullscreen, image=))


    def choose(self, numToChoose):
        pull = []
        for i in range(numToChoose):
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
                if numToChoose == 12 and i == 11:
                    for j in range(1):
                        if self.numPullsUntil[j] == 1 and pick.name != self.names[j] and self.bannerNum == j:
                            for k in range(len(pkmn_list[self.bannerNum])):
                                if self.names[j] == pkmn_list[self.bannerNum][k].name:
                                     ind = k
                            pick = pkmn_list[self.bannerNum][ind]
                            pull.append(pick)
                        else:
                            if pick.rarity != rarityChoose:
                                pick = None
                            else:
                                pull.append(pick)
                else:
                    if pick.rarity != rarityChoose:
                        pick = None
                    else:
                        pull.append(pick)

        random.shuffle(pull)
        print("-------------------------------------------------------")
        for i in range(len(pull)):
            print("(%2d)\t%17s\t[%s]" %(i+1, pull[i].name, pull[i].rarity))
        print("-------------------------------------------------------\n")

        if numToChoose == 12:
            for i in range(1):
                if i == self.bannerNum:
                    for pokemon in pull:
                        if pokemon.name == self.names[i]:
                            self.numPullsUntil[i] = 3
                            noMercy = False
                            break
                        else:
                            noMercy = True
                    if noMercy:
                        self.numPullsUntil[i] -= 1
                    self.label.config(text="Get %s within %d more 12-pulls!" % (self.names[i], self.numPullsUntil[i]))

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
        self.label.config(text="Get %s within %d more 12-pulls!" % (self.names[self.bannerNum], self.numPullsUntil[self.bannerNum]))


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
