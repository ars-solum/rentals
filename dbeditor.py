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

class NewSetPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.bg_imgs = [RGBAImage('menu', 'newbg.png'),
                        RGBAImage('menu', 'inner_bg.png'),]
        self.button_imgs = [RGBAImage('menu', 'back_button.png'),
                            RGBAImage('bar', 'aegislash.png'),]
        self.button_imgs_hover = [RGBAImage('menu', 'back_button2.png'),
                                  RGBAImage('bar', 'aegislash-hover.png'),]
        self.pkmn_imgs = [RGBAImage('menu', 'egg.png'),
                          RGBAImage('SwSh', 'aegislash.png'),]
        self.type_imgs = []
        self.item_imgs = [RGBAImage('bar', 'Life Orb.png'),]
        self.item_imgs_hover = [RGBAImage('bar', 'Life Orb-hover.png'),]
        self.ability_imgs = [RGBAImage('bar', 'Stance Change.png'),]
        self.ability_imgs_hover = [RGBAImage('bar', 'Stance Change-hover.png'),]
        self.attack_imgs = []


        self.canvas = tk.Canvas(self, height=651, width=651, highlightthickness=0)
        self.canvas.pack()

        self.background = self.canvas.create_image((0,0), image=self.bg_imgs[0], anchor='nw')
        self.pack_propagate(0)
        for i in range(40):
            self.canvas.rowconfigure(i, weight=100)
            self.canvas.columnconfigure(i, weight=100)

        self.back = self.canvas.create_image((80,40), image=self.button_imgs[0])
        self.canvas.tag_bind(self.back, '<Enter>', lambda event: self.on_hover(self.back, self.button_imgs_hover[0]))
        self.canvas.tag_bind(self.back, '<Leave>', lambda event: self.on_hover(self.back, self.button_imgs[0]))
        self.canvas.tag_bind(self.back, '<Button-1>', lambda event: self.controller.change_page('NewSetPage', 'MainPage'))

        self.canvas2 = tk.Canvas(self, height=1000, width=651, highlightthickness=0)
        self.inner_bg = self.canvas2.create_image((0,0), image=self.bg_imgs[1], anchor='nw')
        self.inner_canvas = self.canvas.create_window((0,223), window=self.canvas2, anchor='nw')

        self.pokemon_icon = self.canvas.create_image((100,120), image=self.pkmn_imgs[0])

        # pokemon entry
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

        # bottom canvas
        self.test = self.canvas2.create_image((320,60), image=self.button_imgs[1])
        self.canvas2.tag_bind(self.test, '<Enter>', lambda event: self.on_hover(self.test, self.button_imgs_hover[1]))
        self.canvas2.tag_bind(self.test, '<Leave>', lambda event: self.on_hover(self.test, self.button_imgs[1]))
        self.canvas2.tag_bind(self.test, '<Button-1>', lambda event: self.pick_pokemon('Aegislash'))
        self.item_test = self.canvas2.create_image((320,60), image=self.item_imgs[0])
        self.canvas2.tag_bind(self.item_test, '<Enter>', lambda event: self.on_hover(self.item_test, self.item_imgs_hover[0]))
        self.canvas2.tag_bind(self.item_test, '<Leave>', lambda event: self.on_hover(self.item_test, self.item_imgs[0]))
        self.canvas2.tag_bind(self.item_test, '<Button-1>', lambda event: self.pick_item('Life Orb'))
        self.canvas2.itemconfig(self.item_test, state='hidden')
        self.ability_test = self.canvas2.create_image((320,60), image=self.ability_imgs[0])
        self.canvas2.tag_bind(self.ability_test, '<Enter>', lambda event: self.on_hover(self.ability_test, self.ability_imgs_hover[0]))
        self.canvas2.tag_bind(self.ability_test, '<Leave>', lambda event: self.on_hover(self.ability_test, self.ability_imgs[0]))
        self.canvas2.tag_bind(self.ability_test, '<Button-1>', lambda event: self.pick_ability('Stance Change'))
        self.canvas2.itemconfig(self.ability_test, state='hidden')

    def get_pokemon_list(self):
        self.canvas2.itemconfig(self.test, state='normal')
        self.canvas2.itemconfig(self.item_test, state='hidden')
        self.canvas2.itemconfig(self.ability_test, state='hidden')
        self.entry.selection_range(0,tk.END)

    def pick_pokemon(self, name):
        self.canvas.itemconfig(self.item_text, state='normal')
        self.canvas.itemconfig(self.item_entry, state='normal')
        self.canvas.itemconfig(self.ability_text, state='normal')
        self.canvas.itemconfig(self.ability_entry, state='normal')
        self.canvas.itemconfig(self.pokemon_icon, image=self.pkmn_imgs[1])
        self.entry.delete(0,tk.END)
        self.entry.insert(0,name)
        self.entry2.delete(0,tk.END)
        self.entry2.insert(0,'')
        self.entry3.delete(0,tk.END)
        self.entry3.insert(0,'Stance Change')
        self.get_item_list()

    def get_item_list(self):
        self.entry2.selection_range(0,tk.END)
        self.canvas2.itemconfig(self.test, state='hidden')
        self.canvas2.itemconfig(self.item_test, state='normal')
        self.canvas2.itemconfig(self.ability_test, state='hidden')


    def pick_item(self, item_name):
        self.entry2.delete(0,tk.END)
        self.entry2.insert(0,item_name)
        self.get_ability_list()

    def get_ability_list(self):
        self.entry3.selection_range(0,tk.END)
        self.canvas2.itemconfig(self.test, state='hidden')
        self.canvas2.itemconfig(self.item_test, state='hidden')
        self.canvas2.itemconfig(self.ability_test, state='normal')

    def pick_ability(self, ability_name):
        self.entry3.delete(0,tk.END)
        self.entry3.insert(0,ability_name)
        self.get_move_list()

    def get_move_list(self):
        self.canvas2.itemconfig(self.ability_test, state='hidden')

    def test_print(self, name):
        print(name.get())

    def on_hover(self, button, image):
        self.canvas2.itemconfig(button, image=image)


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

    dbapp.resizable(False, False)
    dbapp.geometry("651x651")
    dbapp.title('Rentals DB Editor v%s' %VERSION)
    dbapp.mainloop()
