import os
import xlrd
import xlwt
import tkinter as tk
from PIL import Image, ImageTk
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer

VERSION = '0.1'
mixer.init()

def RGBAImage(subdir, filename):
    return ImageTk.PhotoImage(Image.open(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'media', subdir, filename))).convert('RGBA'))

def get_newset_images():
    pass

class NewSetPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.pack_propagate(0)
        self.images = {
                       'bg'        : [RGBAImage('menu', 'newbg.png'), RGBAImage('menu', 'inner_bg.png')],
                       'buttons'   : {'back'  : [RGBAImage('menu', 'back_button.png'), RGBAImage('menu', 'back_button2.png')],
                                      'stats' : [RGBAImage('menu', 'stats.png'), RGBAImage('menu', 'stats2.png')]},
                       'pokemon'   : {'aegislash' : [RGBAImage('bar', 'aegislash.png'), RGBAImage('bar', 'aegislash-hover.png'), RGBAImage('SwSh', 'aegislash.png')],
                                      'abomasnow' : [RGBAImage('bar', 'abomasnow.png'), RGBAImage('bar', 'abomasnow-hover.png'), RGBAImage('SwSh', 'abomasnow.png')],
                                      'alcremie'  : [RGBAImage('bar', 'alcremie.png'), RGBAImage('bar', 'alcremie-hover.png'), RGBAImage('SwSh', 'alcremie.png')],
                                      'accelgor'  : [RGBAImage('bar', 'accelgor.png'), RGBAImage('bar', 'accelgor-hover.png'), RGBAImage('SwSh', 'accelgor.png')],
                                      'appletun'  : [RGBAImage('bar', 'appletun.png'), RGBAImage('bar', 'appletun-hover.png'), RGBAImage('SwSh', 'appletun.png')]},
                       'items'     : {'Life Orb'     : [RGBAImage('bar', 'Life Orb.png'), RGBAImage('bar', 'Life Orb-hover.png')],
                                      'Choice Scarf' : [RGBAImage('bar', 'Choice Scarf.png'), RGBAImage('bar', 'Choice Scarf-hover.png')],
                                      'Choice Specs' : [RGBAImage('bar', 'Choice Specs.png'), RGBAImage('bar', 'Choice Specs-hover.png')],
                                      'Choice Band'  : [RGBAImage('bar', 'Choice Band.png'), RGBAImage('bar', 'Choice Band-hover.png')],
                                      'Assault Vest' : [RGBAImage('bar', 'Assault Vest.png'), RGBAImage('bar', 'Assault Vest-hover.png')]},
                       'abilities' : {'Stance Change' : [RGBAImage('bar', 'Stance Change.png'), RGBAImage('bar', 'Stance Change-hover.png')]},
                       'attacks'   : { },
                       'other'     : RGBAImage('menu', 'egg.png')
                      }


        self.canvas = tk.Canvas(self, height=651, width=651, highlightthickness=0)
        self.canvas.pack()
        self.background = self.canvas.create_image((0,0), image=self.images['bg'][0], anchor='nw')
        self.in_frame = tk.Frame(self, height=431, width=651, borderwidth=0, highlightthickness=0)
        self.in_frame.pack_propagate(0)
        self.frame = self.canvas.create_window((0,223), window=self.in_frame, anchor='nw')
        self.canvas2 = tk.Canvas(self.in_frame, height=1000, width=651, highlightthickness=0)
        self.inner_bg = self.canvas2.create_image((0,0), image=self.images['bg'][1], anchor='nw')
        self.scrollbar = tk.Scrollbar(self.in_frame, orient='vertical', command=self.custom_yview)
        self.scrollbar.pack(side='right', fill='y')
        self.canvas2.config(yscrollcommand=self.scrollbar.set)
        self.canvas2.pack()

        # back button
        self.back = self.canvas.create_image((80,40), image=self.images['buttons']['back'][0])
        self.canvas.tag_bind(self.back, '<Enter>', lambda event: self.on_hover(self.canvas, self.back, self.images['buttons']['back'][1]))
        self.canvas.tag_bind(self.back, '<Leave>', lambda event: self.on_hover(self.canvas, self.back, self.images['buttons']['back'][0]))
        self.canvas.tag_bind(self.back, '<Button-1>', lambda event: self.controller.change_page('NewSetPage', 'MainPage'))

        # pokemon entry
        self.pokemon_icon = self.canvas.create_image((100,120), image=self.images['other'])
        self.pkmn = tk.StringVar()
        self.pkmn.trace('w', lambda name, index, mode, pkmn=self.pkmn: self.test_print(pkmn))
        self.pokemon_text = self.canvas.create_text((80,180), text='Pokémon')
        self.entry = tk.Entry(self.canvas, textvariable=self.pkmn, width=15)
        self.entry.bind('<Button-1>', lambda event: self.get_pokemon_list())
        self.pokemon_entry = self.canvas.create_window((100,200), window=self.entry)

        # item entry
        self.item = tk.StringVar()
        self.item.trace('w', lambda name, index, mode, item=self.item: self.test_print(item))
        self.item_text = self.canvas.create_text((170,180), text='Item')
        self.canvas.itemconfig(self.item_text, state='hidden')
        self.entry2 = tk.Entry(self.canvas, textvariable=self.item, width=15)
        self.entry2.bind('<Button-1>', lambda event: self.get_item_list())
        self.item_entry = self.canvas.create_window((200,200), window=self.entry2)
        self.canvas.itemconfig(self.item_entry, state='hidden')

        # ability entry
        self.ability = tk.StringVar()
        self.ability.trace('w', lambda name, index, mode, ability=self.ability: self.test_print(ability))
        self.ability_text = self.canvas.create_text((275,180), text='Ability')
        self.canvas.itemconfig(self.ability_text, state='hidden')
        self.entry3 = tk.Entry(self.canvas, textvariable=self.ability, width=15)
        self.entry3.bind('<Button-1>', lambda event: self.get_ability_list())
        self.ability_entry = self.canvas.create_window((300,200), window=self.entry3)
        self.canvas.itemconfig(self.ability_entry, state='hidden')

        # move entry
        self.moves = [tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()]
        for i in range(4):
            self.moves[i].trace('w', lambda name, index, mode, moves=self.moves, i=i: self.test_print(moves[i]))
        self.moves_text = self.canvas.create_text((378,105), text='Moves')
        self.canvas.itemconfig(self.moves_text, state='hidden')
        self.entry4 = []
        for i in range(4):
            self.entry4.append(tk.Entry(self.canvas, textvariable=self.moves[i], width=20))
            self.entry4[i].bind('<Button-1>', lambda event: self.get_move_list())
        self.moves_entry1 = self.canvas.create_window((420,125), window=self.entry4[0])
        self.moves_entry2 = self.canvas.create_window((420,150), window=self.entry4[1])
        self.moves_entry3 = self.canvas.create_window((420,175), window=self.entry4[2])
        self.moves_entry4 = self.canvas.create_window((420,200), window=self.entry4[3])
        self.canvas.itemconfig(self.moves_entry1, state='hidden')
        self.canvas.itemconfig(self.moves_entry2, state='hidden')
        self.canvas.itemconfig(self.moves_entry3, state='hidden')
        self.canvas.itemconfig(self.moves_entry4, state='hidden')

        # stats section
        self.stats_text = self.canvas.create_text((510,105), text='Stats')
        self.canvas.itemconfig(self.stats_text, state='hidden')
        self.stats_button = self.canvas.create_image((560,165), image=self.images['buttons']['stats'][0])
        self.canvas.tag_bind(self.stats_button, '<Enter>', lambda event: self.on_hover(self.canvas, self.stats_button, self.images['buttons']['stats'][1]))
        self.canvas.tag_bind(self.stats_button, '<Leave>', lambda event: self.on_hover(self.canvas, self.stats_button, self.images['buttons']['stats'][0]))
        self.canvas.itemconfig(self.stats_button, state='hidden')

        # bottom canvas
        self.pokemon_buttons = {}
        for i, (pkmn, img) in enumerate(self.images['pokemon'].items()):
            self.pokemon_buttons[pkmn] = self.canvas2.create_image((315,40+65*i), image=img[0])
            self.canvas2.tag_bind(self.pokemon_buttons[pkmn], '<Enter>', lambda event, pkmn=pkmn, img=img: self.on_hover(self.canvas2, self.pokemon_buttons[pkmn], img[1]))
            self.canvas2.tag_bind(self.pokemon_buttons[pkmn], '<Leave>', lambda event, pkmn=pkmn, img=img: self.on_hover(self.canvas2, self.pokemon_buttons[pkmn], img[0]))
            self.canvas2.tag_bind(self.pokemon_buttons[pkmn], '<Button-1>', lambda event, pkmn=pkmn: self.pick_pokemon(pkmn.capitalize()))
        self.item_buttons = {}
        for i, (item, img) in enumerate(self.images['items'].items()):
            self.item_buttons[item] = self.canvas2.create_image((315,40+65*i), image=img[0])
            self.canvas2.tag_bind(self.item_buttons[item], '<Enter>', lambda event, item=item, img=img: self.on_hover(self.canvas2, self.item_buttons[item], img[1]))
            self.canvas2.tag_bind(self.item_buttons[item], '<Leave>', lambda event, item=item, img=img: self.on_hover(self.canvas2, self.item_buttons[item], img[0]))
            self.canvas2.tag_bind(self.item_buttons[item], '<Button-1>', lambda event, item=item: self.pick_item(item))
            self.canvas2.itemconfig(self.item_buttons[item], state='hidden')

        self.ability_buttons = {}
        for i, (ability, img) in enumerate(self.images['abilities'].items()):
            self.ability_buttons[ability] = self.canvas2.create_image((315,40+65*i), image=img[0])
            self.canvas2.tag_bind(self.ability_buttons[ability], '<Enter>', lambda event, ability=ability, img=img: self.on_hover(self.canvas2, self.ability_buttons[ability], img[1]))
            self.canvas2.tag_bind(self.ability_buttons[ability], '<Leave>', lambda event, ability=ability, img=img: self.on_hover(self.canvas2, self.ability_buttons[ability], img[0]))
            self.canvas2.tag_bind(self.ability_buttons[ability], '<Button-1>', lambda event, ability=ability: self.pick_ability(ability))
            self.canvas2.itemconfig(self.ability_buttons[ability], state='hidden')

    def get_pokemon_list(self):
        for pkmn, button in self.pokemon_buttons.items():
            self.canvas2.itemconfig(button, state='normal')
        for item, button in self.item_buttons.items():
            self.canvas2.itemconfig(button, state='hidden')
        for ability, button in self.ability_buttons.items():
            self.canvas2.itemconfig(button, state='hidden')

    def pick_pokemon(self, name):
        self.canvas.itemconfig(self.item_text, state='normal')
        self.canvas.itemconfig(self.item_entry, state='normal')
        self.canvas.itemconfig(self.ability_text, state='normal')
        self.canvas.itemconfig(self.ability_entry, state='normal')
        self.canvas.itemconfig(self.pokemon_icon, image=self.images['pokemon'][name.casefold()][2])
        self.canvas.itemconfig(self.moves_text, state='normal')
        self.canvas.itemconfig(self.moves_entry1, state='normal')
        self.canvas.itemconfig(self.moves_entry2, state='normal')
        self.canvas.itemconfig(self.moves_entry3, state='normal')
        self.canvas.itemconfig(self.moves_entry4, state='normal')
        self.canvas.itemconfig(self.stats_text, state='normal')
        self.canvas.itemconfig(self.stats_button, state='normal')
        self.entry.delete(0,tk.END)
        self.entry.insert(0,name)
        self.entry2.delete(0,tk.END)
        self.entry2.insert(0,'')
        self.entry3.delete(0,tk.END)
        self.entry3.insert(0,'')
        self.entry2.focus_set()
        self.get_item_list()

    def get_item_list(self):
        for pkmn, button in self.pokemon_buttons.items():
            self.canvas2.itemconfig(button, state='hidden')
        for item, button in self.item_buttons.items():
            self.canvas2.itemconfig(button, state='normal')
        for ability, button in self.ability_buttons.items():
            self.canvas2.itemconfig(button, state='hidden')


    def pick_item(self, item_name):
        self.entry2.delete(0,tk.END)
        self.entry2.insert(0,item_name)
        self.entry3.focus_set()
        self.get_ability_list()

    def get_ability_list(self):
        for pkmn, button in self.pokemon_buttons.items():
            self.canvas2.itemconfig(button, state='hidden')
        for item, button in self.item_buttons.items():
            self.canvas2.itemconfig(button, state='hidden')
        for ability, button in self.ability_buttons.items():
            self.canvas2.itemconfig(button, state='normal')

    def pick_ability(self, ability_name):
        self.entry3.delete(0,tk.END)
        self.entry3.insert(0,ability_name)
        self.entry4[0].focus_set()
        self.get_move_list()

    def get_move_list(self):
        for pkmn, button in self.pokemon_buttons.items():
            self.canvas2.itemconfig(button, state='hidden')
        for item, button in self.item_buttons.items():
            self.canvas2.itemconfig(button, state='hidden')
        for ability, button in self.ability_buttons.items():
            self.canvas2.itemconfig(button, state='hidden')

    def test_print(self, name):
        print(name.get())

    def on_hover(self, canvas, button, image):
        canvas.itemconfig(button, image=image)

    def custom_yview(self, *args, **kwargs):
        self.canvas2.yview(*args, **kwargs)
        x = self.canvas2.canvasx(0)
        y = self.canvas2.canvasy(0)
        self.canvas.coords(self.inner_bg, x, y)


class EditSetPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.bg_imgs = []
        self.button_imgs = []
        self.buttons = []


class TeamPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.bg_imgs = []
        self.button_imgs = []
        self.buttons = []

class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.bg_imgs = [RGBAImage('menu', 'testbg.png')]
        self.button_imgs = [RGBAImage('menu', 'new_button.png'),
                            RGBAImage('menu', 'edit_button.png'),
                            RGBAImage('menu', 'team_button.png'),
                            RGBAImage('menu', 'quit_button.png')]
        self.button_imgs_hover = [RGBAImage('menu', 'new_button2.png'),
                                  RGBAImage('menu', 'edit_button2.png'),
                                  RGBAImage('menu', 'team_button2.png'),
                                  RGBAImage('menu', 'quit_button2.png')]
        self.buttons = []

        self.canvas = tk.Canvas(self, height=651, width=651, highlightthickness=0)
        self.canvas.pack()

        self.background = self.canvas.create_image((0,0), image=self.bg_imgs[0], anchor='nw')
        self.pack_propagate(0)
        for i in range(40):
            self.canvas.rowconfigure(i, weight=1)
            self.canvas.columnconfigure(i, weight=1)

        for i in range(4):
            self.buttons.append(self.canvas.create_image((110,40+60*i), image=self.button_imgs[i]))
        for i in range(len(self.buttons)):
            self.canvas.tag_bind(self.buttons[i], '<Enter>', lambda event, i=i: self.on_hover(self.buttons[i], self.button_imgs_hover[i]))
            self.canvas.tag_bind(self.buttons[i], '<Leave>', lambda event, i=i: self.on_hover(self.buttons[i], self.button_imgs[i]))
        self.canvas.tag_bind(self.buttons[0], '<Button-1>', lambda event: self.controller.change_page('MainPage', 'NewSetPage'))
        self.canvas.tag_bind(self.buttons[1], '<Button-1>', lambda event: self.controller.change_page('MainPage', 'EditSetPage'))
        self.canvas.tag_bind(self.buttons[2], '<Button-1>', lambda event: self.controller.change_page('MainPage', 'TeamPage'))
        self.canvas.tag_bind(self.buttons[3], '<Button-1>', lambda event: self.controller.quit)

    def on_hover(self, button, image):
        self.canvas.itemconfig(button, image=image)


class DBEditor (tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill='both', expand=True)
        self.pages = {}

        for page in [MainPage, NewSetPage, EditSetPage, TeamPage,]:
            frame = page(parent=self.main_frame, controller=self)
            self.pages[page.__name__] = frame
            frame.pack(fill='both', expand=True)

        for page in ['NewSetPage', 'EditSetPage', 'TeamPage',]:
            self.pages[page].pack_forget()

    def change_page(self, old_page_name, page_name):
        frame = self.pages[old_page_name]
        frame.pack_forget()
        frame = self.pages[page_name]
        frame.pack(fill='both', expand=True)

if __name__ == '__main__':
    dbapp = DBEditor()

    #dbapp.resizable(False, False)
    dbapp.geometry("651x651")
    dbapp.title('Rentals DB Editor v%s' %VERSION)
    dbapp.mainloop()
