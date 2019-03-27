# import tkinter
#
# class FancyListbox(tkinter.Listbox):
#
#     def __init__(self, parent, *args, **kwargs):
#         tkinter.Listbox.__init__(self, parent, *args, **kwargs)
#
#         self.popup_menu = tkinter.Menu(self, tearoff=0)
#         self.popup_menu.add_command(label="Delete",
#                                     command=self.delete_selected)
#         self.popup_menu.add_command(label="Select All",
#                                     command=self.select_all)
#
#         self.bind("<Button-3>", self.popup) # Button-2 on Aqua
#
#     def popup(self, event):
#         try:
#             self.popup_menu.tk_popup(event.x_root, event.y_root, 0)
#         finally:
#             self.popup_menu.grab_release()
#
#     def delete_selected(self):
#         for i in self.curselection()[::-1]:
#             self.delete(i)
#
#     def select_all(self):
#         self.selection_set(0, 'end')
#
#
# root = tkinter.Tk()
# flb = FancyListbox(root, selectmode='multiple')
# for n in range(10):
#     flb.insert('end', n)
# flb.pack()
# root.mainloop()

import os
from Pokemon import *

ROOT = os.path.dirname(os.path.realpath(__file__))
MEDIA = os.path.join(ROOT, 'media')
PKMN_DIR = os.path.join(MEDIA, 'pokemon')

EXT = ['_active.png', '_banned.png', '_inactive.png', '_picked.png', '_unknown.png']
names = [i.name for i in ALL_POKEMON_S]
ALL_NAMES = sorted(list(set(names)))
ALL_FILES = []
for i in ALL_NAMES:
    for j in range(5):
        ALL_FILES.append(i + EXT[j])

for file in os.listdir(PKMN_DIR):
    if file in ALL_FILES:
        pass
    else:
        print(file)
