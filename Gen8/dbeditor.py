import os
import xlrd
import xlwt
import tkinter as tk
from Pokemon2 import POKEMON_LIST
from PIL import Image, ImageTk
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer

VERSION = '0.4'
mixer.init(22100, -16, 2, 32)
move_sfx = mixer.Sound(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'media', 'sound', 'move.wav'))
move2_sfx = mixer.Sound(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'media', 'sound', 'move2.wav'))
change_screen_sfx = mixer.Sound(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'media', 'sound', 'change_screen.wav'))

#os.path.join(os.path.dirname(os.path.realpath(__file__))

def RGBAImage(subdir, filename):
    try:
        return ImageTk.PhotoImage(Image.open(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'media', subdir, filename))).convert('RGBA'))
    except FileNotFoundError:
        print('Could not find file: ' + os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'media', subdir, filename)))
        return None

def get_newset_images(key):
    directory = os.fsencode(str(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'media', 'bar', key)))
    temp_dict = {}
    running_list = []
    for file in os.listdir(directory):
        if os.fsdecode(file) not in running_list and os.fsdecode(file).endswith('.png') and not os.fsdecode(file).endswith('-hover.png'):
            normal_filename = os.fsdecode(file)
            hover_filename = normal_filename.replace('.png', '-hover.png')
            running_list.append(normal_filename)
            running_list.append(hover_filename)
            normal_img = ImageTk.PhotoImage(Image.open(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'media', 'bar', key, normal_filename))).convert('RGBA'))
            hover_img = ImageTk.PhotoImage(Image.open(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'media', 'bar', key, hover_filename))).convert('RGBA'))
            object_name = normal_filename.replace('e null', 'e: null').replace('mr ', 'mr. ').replace(' jr', ' jr.').replace('.png', '').replace('-hover', '')
            if key == 'pokemon':
                temp_dict[object_name] = [normal_img, hover_img, RGBAImage('pokemon', normal_filename.replace('-hover', ''))]
            else:
                temp_dict[object_name] = [normal_img, hover_img]

    return temp_dict

class NewSetPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.pack_propagate(0)
        self.images = {
                       'bg'        : [RGBAImage('menu', 'newbg.png'), RGBAImage('menu', 'inner_bg.png')],
                       'buttons'   : {'back'  : [RGBAImage('menu', 'back_button.png'), RGBAImage('menu', 'back_button2.png')],
                                      'stats' : [RGBAImage('menu', 'stats.png'), RGBAImage('menu', 'stats2.png')]},
                       'pokemon'   : get_newset_images('pokemon'),
                       'items'     : get_newset_images('items'),
                       'abilities' : get_newset_images('abilities'),
                       'attacks'   : get_newset_images('attacks'),
                       'other'     : RGBAImage('menu', 'egg.png')
                      }
        self.pkmn_canvas_height = len(self.images['pokemon'])*65+15
        self.item_canvas_height = len(self.images['items'])*65+15
        self.default_canvas_height = 431

        self.canvas = tk.Canvas(self, height=651, width=651, highlightthickness=0)
        self.canvas.pack()
        self.background = self.canvas.create_image((0,0), image=self.images['bg'][0], anchor='nw')
        self.in_frame = tk.Frame(self, height=431, width=651, borderwidth=0, highlightthickness=0)
        self.in_frame.pack_propagate(0)
        self.frame = self.canvas.create_window((0,223), window=self.in_frame, anchor='nw')
        self.canvas2 = tk.Canvas(self.in_frame, height=self.pkmn_canvas_height, width=651, highlightthickness=0, scrollregion=(0, 0, 651, self.pkmn_canvas_height))
        self.inner_bg = self.canvas2.create_image((0,0), image=self.images['bg'][1], anchor='nw')
        self.scrollbar = tk.Scrollbar(self.in_frame, orient='vertical', command=self._custom_yview)
        self.scrollbar.pack(side='right', fill='y')
        self.canvas2.config(yscrollcommand=self.scrollbar.set)
        self.canvas2.pack(side='left', expand=True, fill='both')
        self.canvas2.bind('<Enter>', self._on_mousewheel)
        self.canvas2.bind('<Leave>', self._off_mousewheel)
        self.origX = self.canvas2.xview()[0]
        self.origY = self.canvas2.yview()[0]

        # back button
        self.back = self.canvas.create_image((50,40), image=self.images['buttons']['back'][0])
        self.canvas.tag_bind(self.back, '<Enter>', lambda event: self._on_hover(self.canvas, self.back, self.images['buttons']['back'][1], sound=True))
        self.canvas.tag_bind(self.back, '<Leave>', lambda event: self._on_hover(self.canvas, self.back, self.images['buttons']['back'][0]))
        self.canvas.tag_bind(self.back, '<Button-1>', lambda event: self.controller._change_page('NewSetPage', 'MainPage'))

        # pokemon entry
        self.pokemon_icon = self.canvas.create_image((100,120), image=self.images['other'])
        self.pkmn = tk.StringVar()
        self.pokemon_text = self.canvas.create_text((80,180), text='Pokémon')
        self.entry = tk.Entry(self.canvas, textvariable=self.pkmn, width=15)
        self.entry.bind('<Button-1>', lambda event: self._get_pokemon_list(check=True))
        self.entry.bind('<Return>', lambda event: self._check_pokemon())
        self.entry.bind('<Tab>', lambda event: self._check_pokemon())
        self.pokemon_entry = self.canvas.create_window((100,200), window=self.entry)

        # item entry
        self.item = tk.StringVar()
        self.item_text = self.canvas.create_text((170,180), text='Item')
        self.canvas.itemconfig(self.item_text, state='hidden')
        self.entry2 = tk.Entry(self.canvas, textvariable=self.item, width=15)
        self.entry2.bind('<Button-1>', lambda event: self._get_item_list())
        self.entry2.bind('<Tab>', lambda event: self._check_item())
        self.item_entry = self.canvas.create_window((200,200), window=self.entry2)
        self.canvas.itemconfig(self.item_entry, state='hidden')

        # ability entry
        self.ability = tk.StringVar()
        self.ability_text = self.canvas.create_text((275,180), text='Ability')
        self.canvas.itemconfig(self.ability_text, state='hidden')
        self.entry3 = tk.Entry(self.canvas, textvariable=self.ability, width=15)
        self.entry3.bind('<Button-1>', lambda event: self._get_ability_list())
        self.entry3.bind('<Tab>', lambda event: self._check_ability())
        self.ability_entry = self.canvas.create_window((300,200), window=self.entry3)
        self.canvas.itemconfig(self.ability_entry, state='hidden')

        # move entry
        self.moves = [tk.StringVar() for i in range(4)]
        self.moves_text = self.canvas.create_text((378,105), text='Moves')
        self.canvas.itemconfig(self.moves_text, state='hidden')
        self.entry4 = []
        self.moves_entry = []
        for i in range(4):
            self.entry4.append(tk.Entry(self.canvas, textvariable=self.moves[i], width=20))
            self.entry4[i].bind('<Button-1>', lambda event: self._get_move_list())
            self.moves_entry.append(self.canvas.create_window((420,125+25*i), window=self.entry4[i]))
            self.canvas.itemconfig(self.moves_entry[i], state='hidden')

        # stats section
        self.stats_text = self.canvas.create_text((510,105), text='Stats')
        self.canvas.itemconfig(self.stats_text, state='hidden')
        self.stats_button = self.canvas.create_image((560,165), image=self.images['buttons']['stats'][0])
        self.canvas.tag_bind(self.stats_button, '<Enter>', lambda event: self._on_hover(self.canvas, self.stats_button, self.images['buttons']['stats'][1], sound=True))
        self.canvas.tag_bind(self.stats_button, '<Leave>', lambda event: self._on_hover(self.canvas, self.stats_button, self.images['buttons']['stats'][0]))
        self.canvas.tag_bind(self.stats_button, '<Button-1>', lambda event: self._get_stats_screen())
        self.canvas.itemconfig(self.stats_button, state='hidden')

        # bottom canvas
        self.pokemon_buttons = {}
        for i, (pkmn, img) in enumerate(self.images['pokemon'].items()):
            self.pokemon_buttons[pkmn] = self.canvas2.create_image((315,40+65*i), image=img[0])
            self.canvas2.tag_bind(self.pokemon_buttons[pkmn], '<Enter>', lambda event, pkmn=pkmn, img=img: self._on_hover(self.canvas2, self.pokemon_buttons[pkmn], img[1], sound=True))
            self.canvas2.tag_bind(self.pokemon_buttons[pkmn], '<Leave>', lambda event, pkmn=pkmn, img=img: self._on_hover(self.canvas2, self.pokemon_buttons[pkmn], img[0]))
            self.canvas2.tag_bind(self.pokemon_buttons[pkmn], '<Button-1>', lambda event, pkmn=pkmn: self._pick_pokemon(pkmn.capitalize()))
        self.pkmn.trace('w', lambda name, index, mode, pkmn=self.pkmn: self._filter(pkmn, 'pokemon', self.images['pokemon']))
        self.item_buttons = {}
        for i, (item, img) in enumerate(self.images['items'].items()):
            self.item_buttons[item] = self.canvas2.create_image((315,40+65*i), image=img[0])
            self.canvas2.tag_bind(self.item_buttons[item], '<Enter>', lambda event, item=item, img=img: self._on_hover(self.canvas2, self.item_buttons[item], img[1], sound=True))
            self.canvas2.tag_bind(self.item_buttons[item], '<Leave>', lambda event, item=item, img=img: self._on_hover(self.canvas2, self.item_buttons[item], img[0]))
            self.canvas2.tag_bind(self.item_buttons[item], '<Button-1>', lambda event, item=item: self._pick_item(item))
            self.canvas2.itemconfig(self.item_buttons[item], state='hidden')
        self.item.trace('w', lambda name, index, mode, item=self.item: self._filter(item, 'items', self.images['items']))
        self.ability_buttons = {}
        self.ability.trace('w', lambda name, index, mode, ability=self.ability: self._filter(ability, 'abilities', self.images['abilities']))
        self.move_buttons = {}
        for i in range(4):
            self.moves[i].trace('w', lambda name, index, mode, moves=self.moves, i=i: self._filter(moves[i], 'attacks', self.images['attacks']))

        # ev stats
        self.ev_stats = [tk.StringVar() for i in range(6)]
        for i in range(6):
            self.ev_stats[i].trace('w', lambda name, index, mode, stats=self.ev_stats, i=i: self._filter(stats[i], 'ev_stats'))
        self.entry5 = []
        self.ev_stats_entry = []
        for i in range(6):
            self.entry5.append(tk.Entry(self.canvas2, textvariable=self.ev_stats[i], width=7))
            self.ev_stats_entry.append(self.canvas2.create_window((300, 50+25*i), window=self.entry5[i]))
            self.canvas2.itemconfig(self.ev_stats_entry[i], state='hidden')

        # iv stats
        self.iv_stats = [tk.IntVar() for i in range(6)]
        for i in range(6):
            self.ev_stats[i].trace('w', lambda name, index, mode, stats=self.ev_stats, i=i: self._filter(stats[i], 'iv_stats'))
        self.entry5 = []
        self.ev_stats_entry = []
        for i in range(6):
            self.entry5.append(tk.Entry(self.canvas2, textvariable=self.ev_stats[i], width=7))
            self.ev_stats_entry.append(self.canvas2.create_window((300, 50+25*i), window=self.entry5[i]))
            self.canvas2.itemconfig(self.ev_stats_entry[i], state='hidden')

###############################################################################
    def _get_stats_screen(self):
        for pkmn, button in self.pokemon_buttons.items():
            self.canvas2.itemconfig(button, state='hidden')
        for item, button in self.item_buttons.items():
            self.canvas2.itemconfig(button, state='hidden')
        for ability, button in self.ability_buttons.items():
            self.canvas2.itemconfig(button, state='hidden')
        for move, button in self.move_buttons.items():
            self.canvas2.itemconfig(button, state='hidden')
        for i in range(6):
            self.canvas2.itemconfig(self.ev_stats_entry[i], state='normal')
        self.scrollbar.pack_forget()
        self.canvas2.pack_forget()
        self.canvas2.config(height=self.pkmn_canvas_height, scrollregion=(0, 0, 651, 431))
        self.canvas2.pack(side='left', expand=True, fill='both')
        x = self.canvas2.canvasx(0)
        y = self.canvas2.canvasy(0)
        self.canvas2.coords(self.inner_bg, x, y)

    def _check_pokemon(self):
        for pkmn, i in self.pokemon_buttons.items():
            if pkmn.startswith(self.entry.get().casefold()):
                pokemon_name = pkmn
                break
        self._pick_pokemon(pokemon_name)

    def _check_item(self):
        for item, i in self.item_buttons.items():
            if item.startswith(self.entry2.get().casefold()):
                item_name = item
                break
        self._pick_item(item_name)

    def _check_ability(self):
        for abil, i in self.ability_buttons.items():
            if abil.startswith(self.entry3.get().casefold()):
                abil_name = abil
                break
        self._pick_ability(abil_name)

    def _get_abilities(self, pokemon_name):
        pokemon_name = pokemon_name.replace('-Gmax', '')
        if pokemon_name not in POKEMON_LIST.keys():
            print('Error, cant find Pokemon: %s' %pokemon_name)
        return POKEMON_LIST[pokemon_name].abilities

    def _get_moves(self, pokemon_name):
        pokemon_name = pokemon_name.replace('-Gmax', '')
        if pokemon_name not in POKEMON_LIST.keys():
            print('Error, cant find Pokemon: %s' %pokemon_name)
        return POKEMON_LIST[pokemon_name].attacks

    def _get_pokemon_list(self, check=False):
        for pkmn, button in self.pokemon_buttons.items():
            self.canvas2.itemconfig(button, state='normal')
        for item, button in self.item_buttons.items():
            self.canvas2.itemconfig(button, state='hidden')
        for ability, button in self.ability_buttons.items():
            self.canvas2.itemconfig(button, state='hidden')
        for move, button in self.move_buttons.items():
            self.canvas2.itemconfig(button, state='hidden')
        for i in range(6):
            self.canvas2.itemconfig(self.ev_stats_entry[i], state='hidden')
        if check:
            search_list = {}
            for list_item, i in self.images['pokemon'].items():
                if list_item.startswith(self.entry.get().casefold()):
                    search_list[list_item] = i
            new_height = len(search_list)*65+15
            if new_height > 431:
                self.scrollbar.pack(side='right', fill='y')
                self.canvas2.pack_forget()
                self.canvas2.config(height=new_height, scrollregion=(0, 0, 651, new_height))
                self.canvas2.pack(side='left', expand=True, fill='both')
            else:
                self.scrollbar.pack_forget()
                self.canvas2.pack_forget()
                self.canvas2.config(height=431, scrollregion=(0, 0, 651, 431))
                self.canvas2.pack(side='left', expand=True, fill='both')
        else:
            self.scrollbar.pack(side='right', fill='y')
            self.canvas2.pack_forget()
            self.canvas2.config(height=self.pkmn_canvas_height, scrollregion=(0, 0, 651, self.pkmn_canvas_height))
            self.canvas2.pack(side='left', expand=True, fill='both')
        self.canvas2.xview_moveto(self.origX)
        self.canvas2.yview_moveto(self.origY)
        x = self.canvas2.canvasx(0)
        y = self.canvas2.canvasy(0)
        self.canvas2.coords(self.inner_bg, x, y)

    def _pick_pokemon(self, pkmn_name):
        # reveal all the other entry fields
        self.canvas.itemconfig(self.item_text, state='normal')
        self.canvas.itemconfig(self.item_entry, state='normal')
        self.canvas.itemconfig(self.ability_text, state='normal')
        self.canvas.itemconfig(self.ability_entry, state='normal')
        self.canvas.itemconfig(self.pokemon_icon, image=self.images['pokemon'][pkmn_name.casefold()][2])
        self.canvas.itemconfig(self.moves_text, state='normal')
        for i in range(4):
            self.canvas.itemconfig(self.moves_entry[i], state='normal')
        self.canvas.itemconfig(self.stats_text, state='normal')
        self.canvas.itemconfig(self.stats_button, state='normal')

        # overwrite entry text
        name = [word.capitalize() for word in pkmn_name.split()]
        pkmn_name = ' '.join(name)
        name = [word.capitalize() for word in pkmn_name.split('-')]
        pkmn_name = '-'.join(name)
        self.entry.delete(0,tk.END)
        self.entry.insert(0,pkmn_name)
        self.entry2.delete(0,tk.END)
        self.entry2.insert(0,'')
        self.entry3.delete(0,tk.END)
        self.entry3.insert(0,'')
        self.entry2.focus_set()

        # clear ability buttons
        for ability, button in self.ability_buttons.items():
            self.canvas2.delete(button)
        self.ability_buttons = {}

        # get this pokemon's abilites
        abil_list = self._get_abilities(pkmn_name)
        abil_list = [i.casefold() for i in abil_list]

        # make new buttons
        for i, ability in enumerate(abil_list):
            try:
                self.ability_buttons[ability] = self.canvas2.create_image((315,40+65*i), image=self.images['abilities'][ability][0])
                self.canvas2.tag_bind(self.ability_buttons[ability], '<Enter>', lambda event, abil=ability, img=self.images['abilities'][ability]: self._on_hover(self.canvas2, self.ability_buttons[abil], img[1], sound=True))
                self.canvas2.tag_bind(self.ability_buttons[ability], '<Leave>', lambda event, abil=ability, img=self.images['abilities'][ability]: self._on_hover(self.canvas2, self.ability_buttons[abil], img[0]))
                self.canvas2.tag_bind(self.ability_buttons[ability], '<Button-1>', lambda event, abil=ability: self._pick_ability(abil.capitalize()))
            except:
                print('Missing Ability:', ability)

        # clear move buttons
        for move, button in self.move_buttons.items():
            self.canvas2.delete(button)
        self.move_buttons = {}

        # get this pokemon's moves
        move_list = self._get_moves(pkmn_name)
        move_list = [i.casefold() for i in move_list]

        # make new buttons
        for i, move in enumerate(move_list):
            try:
                self.move_buttons[move] = self.canvas2.create_image((315,40+65*i), image=self.images['attacks'][move][0])
                self.canvas2.tag_bind(self.move_buttons[move], '<Enter>', lambda event, move=move, img=self.images['attacks'][move]: self._on_hover(self.canvas2, self.move_buttons[move], img[1], sound=True))
                self.canvas2.tag_bind(self.move_buttons[move], '<Leave>', lambda event, move=move, img=self.images['attacks'][move]: self._on_hover(self.canvas2, self.move_buttons[move], img[0]))
                self.canvas2.tag_bind(self.move_buttons[move], '<Button-1>', lambda event, move=move: self._pick_move(move.capitalize()))
            except:
                print('Missing Attack:', move)

        # move onto items
        self._get_item_list()

    def _get_item_list(self):
        for pkmn, button in self.pokemon_buttons.items():
            self.canvas2.itemconfig(button, state='hidden')
        for item, button in self.item_buttons.items():
            self.canvas2.itemconfig(button, state='normal')
        for ability, button in self.ability_buttons.items():
            self.canvas2.itemconfig(button, state='hidden')
        for move, button in self.move_buttons.items():
            self.canvas2.itemconfig(button, state='hidden')
        for i in range(6):
            self.canvas2.itemconfig(self.ev_stats_entry[i], state='hidden')
        if self.item_canvas_height > self.default_canvas_height:
            self.scrollbar.pack(side='right', fill='y')
        else:
            self.scrollbar.pack_forget()
        self.canvas2.pack_forget()
        self.canvas2.config(height=self.item_canvas_height, scrollregion=(0, 0, 651, self.item_canvas_height))
        self.canvas2.pack(side='left', expand=True, fill='both')
        self.canvas2.xview_moveto(self.origX)
        self.canvas2.yview_moveto(self.origY)
        x = self.canvas2.canvasx(0)
        y = self.canvas2.canvasy(0)
        self.canvas2.coords(self.inner_bg, x, y)

    def _pick_item(self, item_name):
        name = [word.capitalize() for word in item_name.split()]
        item_name = ' '.join(name)
        self.entry2.delete(0,tk.END)
        self.entry2.insert(0,item_name)
        self.entry3.focus_set()
        self._get_ability_list()

    def _get_ability_list(self):
        for pkmn, button in self.pokemon_buttons.items():
            self.canvas2.itemconfig(button, state='hidden')
        for item, button in self.item_buttons.items():
            self.canvas2.itemconfig(button, state='hidden')
        for ability, button in self.ability_buttons.items():
            self.canvas2.itemconfig(button, state='normal')
        for move, button in self.move_buttons.items():
            self.canvas2.itemconfig(button, state='hidden')
        for i in range(6):
            self.canvas2.itemconfig(self.ev_stats_entry[i], state='hidden')
        self.canvas2.config(height=self.default_canvas_height, scrollregion=(0, 0, 651, self.default_canvas_height))
        self.scrollbar.pack_forget()
        x = self.canvas2.canvasx(0)
        y = self.canvas2.canvasy(0)
        self.canvas2.coords(self.inner_bg, x, y)

    def _pick_ability(self, ability_name):
        name = [word.capitalize() for word in ability_name.split()]
        ability_name = ' '.join(name)
        self.entry3.delete(0,tk.END)
        self.entry3.insert(0,ability_name)
        self.entry4[0].focus_set()
        self._get_move_list()

    def _get_move_list(self):
        for pkmn, button in self.pokemon_buttons.items():
            self.canvas2.itemconfig(button, state='hidden')
        for item, button in self.item_buttons.items():
            self.canvas2.itemconfig(button, state='hidden')
        for ability, button in self.ability_buttons.items():
            self.canvas2.itemconfig(button, state='hidden')
        for move, button in self.move_buttons.items():
            self.canvas2.itemconfig(button, state='normal')
        for i in range(6):
            self.canvas2.itemconfig(self.ev_stats_entry[i], state='hidden')
        self.scrollbar.pack(side='right', fill='y')
        self.canvas2.pack_forget()
        self.canvas2.config(height=self.default_canvas_height, scrollregion=(0, 0, 651, self.default_canvas_height))
        self.canvas2.pack(side='left', expand=True, fill='both')
        self.canvas2.xview_moveto(self.origX)
        self.canvas2.yview_moveto(self.origY)
        x = self.canvas2.canvasx(0)
        y = self.canvas2.canvasy(0)
        self.canvas2.coords(self.inner_bg, x, y)

    def _pick_move(self, attack_name):
        # overwrite move onto correct entry field
        name = [word.capitalize() for word in attack_name.split()]
        attack_name = ' '.join(name)
        name = [word.capitalize() for word in attack_name.split('-')]
        attack_name = '-'.join(name)
        if self.focus_get() == self.entry4[0]:
            slot = 0
        elif self.focus_get() == self.entry4[1]:
            slot = 1
        elif self.focus_get() == self.entry4[2]:
            slot = 2
        elif self.focus_get() == self.entry4[3]:
            slot = 3
        else:
            print('Error')
        self.entry4[slot].delete(0,tk.END)
        self.entry4[slot].insert(0,attack_name)

        # move to next field or stats
        if slot < 3:
            self.entry4[slot+1].focus_set()
        else:
            self._get_stats_screen()

    def _filter(self, name, buttons, field):
        # get list of matching elements
        search_list = {}
        if buttons == 'pokemon' or buttons == 'items':
            for list_item, i in field.items():
                if list_item.startswith(name.get().casefold()):
                    search_list[list_item] = i
        else:
            if buttons == 'abilities':
                for abil in self._get_abilities(self.entry.get()):
                    if abil.casefold().startswith(name.get().casefold()):
                        search_list[abil.casefold()] = 0
            if buttons == 'attacks':
                for move in self._get_moves(self.entry.get()):
                    if move.casefold().startswith(name.get().casefold()):
                        search_list[move.casefold()] = 0
        if not search_list:
            return

        # clear canvas of all buttons
        if buttons == 'pokemon':
            for list_item, button in self.pokemon_buttons.items():
                self.canvas2.delete(button)
            self.pokemon_buttons = {}
        elif buttons == 'items':
            for list_item, button in self.item_buttons.items():
                self.canvas2.delete(button)
            self.item_buttons = {}
        elif buttons == 'abilities':
            for list_item, button in self.ability_buttons.items():
                self.canvas2.delete(button)
            self.ability_buttons = {}

        # resize canvas
        self.new_canvas_height = len(search_list)*65+15 if len(search_list)*65+15 > 431 else 431
        self.canvas2.config(height=self.new_canvas_height, scrollregion=(0, 0, 651, self.new_canvas_height))
        if self.new_canvas_height <= self.default_canvas_height:
            self.scrollbar.pack_forget()
        else:
            self.scrollbar.pack(side='right', fill='y')
            self.canvas2.pack_forget()
            self.canvas2.config(height=self.new_canvas_height, scrollregion=(0, 0, 651, self.new_canvas_height))
            self.canvas2.pack(side='left', expand=True, fill='both')

        # repopulate canvas with new list
        for i, (list_item, _) in enumerate(search_list.items()):
            if buttons == 'pokemon':
                try:
                    self.pokemon_buttons[list_item] = self.canvas2.create_image((315,40+65*i), image=field[list_item][0])
                    self.canvas2.tag_bind(self.pokemon_buttons[list_item], '<Enter>', lambda event, item=list_item, img=field[list_item]: self._on_hover(self.canvas2, self.pokemon_buttons[item], img[1], sound=True))
                    self.canvas2.tag_bind(self.pokemon_buttons[list_item], '<Leave>', lambda event, item=list_item, img=field[list_item]: self._on_hover(self.canvas2, self.pokemon_buttons[item], img[0]))
                    self.canvas2.tag_bind(self.pokemon_buttons[list_item], '<Button-1>', lambda event, item=list_item: self._pick_pokemon(item.capitalize()))
                except:
                    print('Missing Pokemon:', list_item)
            elif buttons == 'items':
                try:
                    self.item_buttons[list_item] = self.canvas2.create_image((315,40+65*i), image=field[list_item][0])
                    self.canvas2.tag_bind(self.item_buttons[list_item], '<Enter>', lambda event, item=list_item, img=field[list_item]: self._on_hover(self.canvas2, self.item_buttons[item], img[1], sound=True))
                    self.canvas2.tag_bind(self.item_buttons[list_item], '<Leave>', lambda event, item=list_item, img=field[list_item]: self._on_hover(self.canvas2, self.item_buttons[item], img[0]))
                    self.canvas2.tag_bind(self.item_buttons[list_item], '<Button-1>', lambda event, item=list_item: self._pick_item(item.capitalize()))
                except:
                    print('Missing Item:', list_item)
            elif buttons == 'abilities':
                try:
                    self.ability_buttons[list_item] = self.canvas2.create_image((315,40+65*i), image=field[list_item][0])
                    self.canvas2.tag_bind(self.ability_buttons[list_item], '<Enter>', lambda event, item=list_item, img=field[list_item]: self._on_hover(self.canvas2, self.ability_buttons[item], img[1], sound=True))
                    self.canvas2.tag_bind(self.ability_buttons[list_item], '<Leave>', lambda event, item=list_item, img=field[list_item]: self._on_hover(self.canvas2, self.ability_buttons[item], img[0]))
                    self.canvas2.tag_bind(self.ability_buttons[list_item], '<Button-1>', lambda event, item=list_item: self._pick_ability(item.capitalize()))
                except:
                    print('Missing Ability:', list_item)
            else:
                print('What is this? ', buttons)

    def _on_hover(self, canvas, button, image, sound=False):
        canvas.itemconfig(button, image=image)
        if sound:
            move_sfx.play()

    def _custom_yview(self, *args, **kwargs):
        self.canvas2.yview(*args, **kwargs)
        x = self.canvas2.canvasx(0)
        y = self.canvas2.canvasy(0)
        self.canvas2.coords(self.inner_bg, x, y)

    def _on_mousewheel(self, event):
        self.canvas2.bind_all('<MouseWheel>', self._scroll)

    def _off_mousewheel(self, event):
        self.canvas2.unbind_all('<MouseWheel>')

    def _scroll(self, event):
        self.canvas2.yview_scroll(int(-1*(event.delta/120)), 'units')
        x = self.canvas2.canvasx(0)
        y = self.canvas2.canvasy(0)
        self.canvas2.coords(self.inner_bg, x, y)


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
            self.canvas.tag_bind(self.buttons[i], '<Enter>', lambda event, i=i: self._on_hover(self.buttons[i], self.button_imgs_hover[i]))
            self.canvas.tag_bind(self.buttons[i], '<Leave>', lambda event, i=i: self._on_hover(self.buttons[i], self.button_imgs[i]))
        self.canvas.tag_bind(self.buttons[0], '<Button-1>', lambda event: self.controller._change_page('MainPage', 'NewSetPage'))
        self.canvas.tag_bind(self.buttons[1], '<Button-1>', lambda event: self.controller._change_page('MainPage', 'EditSetPage'))
        self.canvas.tag_bind(self.buttons[2], '<Button-1>', lambda event: self.controller._change_page('MainPage', 'TeamPage'))
        self.canvas.tag_bind(self.buttons[3], '<Button-1>', lambda event: self.controller.quit)

    def _on_hover(self, button, image, sound=False):
        self.canvas.itemconfig(button, image=image)
        if sound:
            move2_sfx.play()


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

    def _change_page(self, old_page_name, page_name):
        change_screen_sfx.play()
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
