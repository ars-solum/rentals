import os
import tkinter as tk
from Pokemon2 import *
from PIL import Image, ImageTk
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
from pygame import mixer

VERSION = '0.9'
mixer.init(22100, -16, 2, 32)
sfx = {}
for file in os.listdir(os.fsencode(str(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'media', 'sound')))):
    if os.fsdecode(file).endswith('.wav'):
        sfx[os.fsdecode(file).replace('.wav', '')] = mixer.Sound(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'media', 'sound', os.fsdecode(file)))

EV_VALUES = [0, 252]

#os.path.join(os.path.dirname(os.path.realpath(__file__))

def RGBAImage(subdir, filename):
    try:
        return ImageTk.PhotoImage(Image.open(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'media', subdir, filename))).convert('RGBA'))
    except FileNotFoundError:
        print('Could not find file: ' + os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'media', subdir, filename)))
        return None

class NewSetPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.pack_propagate(0)
        self.images = {'bg'        : [RGBAImage('menu', 'newbg.png'), RGBAImage('menu', 'inner_bg.png')],
                       'buttons'   : {'back'   : [RGBAImage('menu', 'back_button.png'), RGBAImage('menu', 'back_button2.png')],
                                      'clear'  : [RGBAImage('menu', 'clear.png'), RGBAImage('menu', 'clear-hover.png')],
                                      'import' : [RGBAImage('menu', 'import.png'), RGBAImage('menu', 'import-hover.png')],
                                      'save'   : [RGBAImage('menu', 'save.png'), RGBAImage('menu', 'save-hover.png')],
                                      'stats'  : [RGBAImage('menu', 'stats.png'), RGBAImage('menu', 'stats2.png')]},
                       'pokemon'   : self._get_images('pokemon'),
                       'items'     : self._get_images('items'),
                       'abilities' : self._get_images('abilities'),
                       'attacks'   : self._get_images('attacks'),
                       'other'     : RGBAImage('menu', 'egg.png')}
        self.pkmn_canvas_height = len(self.images['pokemon'])*65+15
        self.item_canvas_height = len(self.images['items'])*65+15
        self.min_height = 431
        self._WIDTH = 651
        self.revealed = False
        self.canvas = tk.Canvas(self, height=self._WIDTH, width=self._WIDTH, highlightthickness=0)
        self.canvas.pack()
        self.background = self.canvas.create_image((0,0), image=self.images['bg'][0], anchor='nw')
        # make a nested canvas
        self.in_frame = tk.Frame(self, height=self.min_height, width=self._WIDTH, borderwidth=0, highlightthickness=0)
        self.in_frame.pack_propagate(0)
        self.frame = self.canvas.create_window((0,223), window=self.in_frame, anchor='nw')
        self.canvas2 = tk.Canvas(self.in_frame, height=self.pkmn_canvas_height, width=self._WIDTH, highlightthickness=0, scrollregion=(0, 0, self._WIDTH, self.pkmn_canvas_height))
        self.inner_bg = self.canvas2.create_image((0,0), image=self.images['bg'][1], anchor='nw')
        self.scrollbar = tk.Scrollbar(self.in_frame, orient='vertical', command=self._custom_yview)
        self.scrollbar.pack(side='right', fill='y')
        self.canvas2.config(yscrollcommand=self.scrollbar.set)
        self.canvas2.pack(side='left', expand=True, fill='both')
        self.canvas2.bind('<Enter>', self._on_mousewheel)
        self.canvas2.bind('<Leave>', self._off_mousewheel)
        # the top of the bottom canvas
        self.origX = self.canvas2.xview()[0]
        self.origY = self.canvas2.yview()[0]

        # back button
        self.back_button = self.canvas.create_image((50,40), image=self.images['buttons']['back'][0])
        self.canvas.tag_bind(self.back_button, '<Enter>', lambda event: self._on_hover(self.canvas, self.back_button, self.images['buttons']['back'][1], sound=True))
        self.canvas.tag_bind(self.back_button, '<Leave>', lambda event: self._on_hover(self.canvas, self.back_button, self.images['buttons']['back'][0]))
        self.canvas.tag_bind(self.back_button, '<Button-1>', lambda event: self.controller._change_page('NewSetPage', 'MainPage'))

        # import/export button
        self.import_button = self.canvas.create_image((150,40), image=self.images['buttons']['import'][0])
        self.canvas.tag_bind(self.import_button, '<Enter>', lambda event: self._on_hover(self.canvas, self.import_button, self.images['buttons']['import'][1], sound=True))
        self.canvas.tag_bind(self.import_button, '<Leave>', lambda event: self._on_hover(self.canvas, self.import_button, self.images['buttons']['import'][0]))
        self.canvas.tag_bind(self.import_button, '<Button-1>', lambda event: self._get_import_screen())

        # clear button
        self.clear_button = self.canvas.create_image((225,40), image=self.images['buttons']['clear'][0])
        self.canvas.tag_bind(self.clear_button, '<Enter>', lambda event: self._on_hover(self.canvas, self.clear_button, self.images['buttons']['clear'][1], sound=True))
        self.canvas.tag_bind(self.clear_button, '<Leave>', lambda event: self._on_hover(self.canvas, self.clear_button, self.images['buttons']['clear'][0]))
        self.canvas.tag_bind(self.clear_button, '<Button-1>', lambda event: self.clear_page())
        self.canvas.itemconfig(self.clear_button, state='hidden')

        # save button
        self.save_button = self.canvas.create_image((300,40), image=self.images['buttons']['save'][0])
        self.canvas.tag_bind(self.save_button, '<Enter>', lambda event: self._on_hover(self.canvas, self.save_button, self.images['buttons']['save'][1], sound=True))
        self.canvas.tag_bind(self.save_button, '<Leave>', lambda event: self._on_hover(self.canvas, self.save_button, self.images['buttons']['save'][0]))
        self.canvas.tag_bind(self.save_button, '<Button-1>', lambda event: self._save_set())
        self.canvas.itemconfig(self.save_button, state='hidden')

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
        self.entry2.bind('<Button-1>', lambda event: self._get_item_list(check=True))
        self.entry2.bind('<Return>', lambda event: self._check_item())
        self.entry2.bind('<Tab>', lambda event: self._check_item())
        self.item_entry = self.canvas.create_window((200,200), window=self.entry2)
        self.canvas.itemconfig(self.item_entry, state='hidden')

        # ability entry
        self.ability = tk.StringVar()
        self.ability_text = self.canvas.create_text((275,180), text='Ability')
        self.canvas.itemconfig(self.ability_text, state='hidden')
        self.entry3 = tk.Entry(self.canvas, textvariable=self.ability, width=15)
        self.entry3.bind('<Button-1>', lambda event: self._get_ability_list())
        self.entry3.bind('<Return>', lambda event: self._check_ability())
        self.entry3.bind('<Tab>', lambda event: self._check_ability())
        self.ability_entry = self.canvas.create_window((300,200), window=self.entry3)
        self.canvas.itemconfig(self.ability_entry, state='hidden')

        # TODO FIXME: Add dynamax checkbox for non-Gmax Pokemon.

        # move entry
        self.moves = [tk.StringVar() for i in range(4)]
        self.moves_text = self.canvas.create_text((378,105), text='Moves')
        self.canvas.itemconfig(self.moves_text, state='hidden')
        self.entry4 = []
        self.moves_entry = []
        for i in range(4):
            self.entry4.append(tk.Entry(self.canvas, textvariable=self.moves[i], width=20))
            self.entry4[i].bind('<Button-1>', lambda event: self._get_move_list())
            # TODO FIXME: bind return & tab
            self.moves_entry.append(self.canvas.create_window((420,125+25*i), window=self.entry4[i]))
            self.canvas.itemconfig(self.moves_entry[i], state='hidden')

        # stats button
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
        self.pkmn_trace = self.pkmn.trace('w', lambda name, index, mode, pkmn=self.pkmn: self._filter(pkmn, 'pokemon', self.images['pokemon']))
        self.item_buttons = {}
        for i, (item, img) in enumerate(self.images['items'].items()):
            self.item_buttons[item] = self.canvas2.create_image((315,40+65*i), image=img[0])
            self.canvas2.tag_bind(self.item_buttons[item], '<Enter>', lambda event, item=item, img=img: self._on_hover(self.canvas2, self.item_buttons[item], img[1], sound=True))
            self.canvas2.tag_bind(self.item_buttons[item], '<Leave>', lambda event, item=item, img=img: self._on_hover(self.canvas2, self.item_buttons[item], img[0]))
            self.canvas2.tag_bind(self.item_buttons[item], '<Button-1>', lambda event, item=item: self._pick_item(item))
            self.canvas2.itemconfig(self.item_buttons[item], state='hidden')
        self.item_trace = self.item.trace('w', lambda name, index, mode, item=self.item: self._filter(item, 'items', self.images['items']))
        self.ability_buttons = {}
        self.ability_trace = self.ability.trace('w', lambda name, index, mode, ability=self.ability: self._filter(ability, 'abilities', self.images['abilities']))
        self.move_buttons = {}
        self.move_trace = []
        for i in range(4):
            self.move_trace.append(self.moves[i].trace('w', lambda name, index, mode, moves=self.moves, i=i: self._filter(moves[i], 'attacks', self.images['attacks'])))

        # stat labels
        self.stat_labels = {
                            'base'      : self.canvas2.create_text((130,25), text='Base'),
                            'evs'       : self.canvas2.create_text((200,25), text='EVs'),
                            'ivs'       : self.canvas2.create_text((500,25), text='IVs'),
                            'hp_label'  : self.canvas2.create_text((70,50), text='HP'),
                            'atk_label' : self.canvas2.create_text((70,75), text='Attack'),
                            'def_label' : self.canvas2.create_text((70,100), text='Defense'),
                            'spa_label' : self.canvas2.create_text((70,125), text='Sp. Atk.'),
                            'spd_label' : self.canvas2.create_text((70,150), text='Sp. Def.'),
                            'spe_label' : self.canvas2.create_text((70,175), text='Speed'),
                            'rem_label' : self.canvas2.create_text((130,200), text='Remaining:'),
                            'nature'    : self.canvas2.create_text((70,225), text='Nature:'),
                            'hp_stat'   : self.canvas2.create_text((550,50), text='999'),
                            'atk_stat'   : self.canvas2.create_text((550,75), text='999'),
                            'def_stat'   : self.canvas2.create_text((550,100), text='999'),
                            'spa_stat'   : self.canvas2.create_text((550,125), text='999'),
                            'spd_stat'   : self.canvas2.create_text((550,150), text='999'),
                            'spe_stat'   : self.canvas2.create_text((550,175), text='999'),
                            'hp_base'   : self.canvas2.create_text((130,50), text='999'),
                            'atk_base'   : self.canvas2.create_text((130,75), text='999'),
                            'def_base'   : self.canvas2.create_text((130,100), text='999'),
                            'spa_base'   : self.canvas2.create_text((130,125), text='999'),
                            'spd_base'   : self.canvas2.create_text((130,150), text='999'),
                            'spe_base'   : self.canvas2.create_text((130,175), text='999'),
                            'rem_value'  : self.canvas2.create_text((200,200), text='508')
        }
        for item in self.stat_labels.values():
            self.canvas2.itemconfig(item, state='hidden')

        # nature
        self.positive_stat = []
        self.negative_stat = []
        self.nature = tk.StringVar()
        self.nature.set('Serious')
        self._natures = {'Adamant (+Atk, -SpA)' : 'Adamant',
                         'Bashful'              : 'Bashful',
                         'Bold (+Def, -Atk)'    : 'Bold',
                         'Brave (+Atk, -Spe)'   : 'Brave',
                         'Calm (+SpD, -Atk)'    : 'Calm',
                         'Careful (+SpD, -SpA)' : 'Careful',
                         'Docile'               : 'Docile',
                         'Gentle (+SpD, -Def)'  : 'Gentle',
                         'Hardy'                : 'Hardy',
                         'Hasty (+Spe, -Def)'   : 'Hasty',
                         'Impish (+Def, -SpA)'  : 'Impish',
                         'Jolly (+Spe, -SpA)'   : 'Jolly',
                         'Lax (+Def, -SpD)'     : 'Lax',
                         'Lonely (+Atk, -Def)'  : 'Lonely',
                         'Mild (+SpA, -Def)'    : 'Mild',
                         'Modest (+SpA, -Atk)'  : 'Modest',
                         'Naive (+Spe, -SpD)'   : 'Naive',
                         'Naughty (+Atk, -SpD)' : 'Naughty',
                         'Quiet (+SpA, -Spe)'   : 'Quiet',
                         'Quirky'               : 'Quirky',
                         'Rash (+SpA, -SpD)'    : 'Rash',
                         'Relaxed (+Def, -Spe)' : 'Relaxed',
                         'Sassy (+SpD, -Spe)'   : 'Sassy',
                         'Serious'              : 'Serious',
                         'Timid (+Spe, -Atk)'   : 'Timid'}
        self.display_nature = tk.StringVar()
        self.display_nature.set('Serious')
        self.nature_om = tk.OptionMenu(self.canvas2, self.display_nature, *self._natures.keys(), command=self._set_nature)
        self.nature_om.config(width=20)
        self.nature_widget = self.canvas2.create_window((175, 225), window=self.nature_om)
        self.canvas2.itemconfig(self.nature_widget, state='hidden')

        # ev stats
        self.ev_stats = [tk.StringVar() for i in range(6)]
        self.entry5 = []
        self.ev_stats_entry = []
        self.ev_trace = []
        for i, stat in enumerate(['hp_stat', 'atk_stat', 'def_stat', 'spa_stat', 'spd_stat', 'spe_stat']):
            self.entry5.append(tk.Entry(self.canvas2, textvariable=self.ev_stats[i], width=7))
            self.ev_stats_entry.append(self.canvas2.create_window((200, 50+25*i), window=self.entry5[i]))
            self.ev_trace.append(self.ev_stats[i].trace('w', lambda name, index, mode, i=i, stat=stat: self._update_all_stats(i, stat)))
            self.canvas2.itemconfig(self.ev_stats_entry[i], state='hidden')

        # ev scales
        self.scale = {}
        for i in ['hp', 'atk', 'def', 'spa', 'spd', 'spe']:
            self.scale[i] = tk.Scale(self.canvas2, from_=min(EV_VALUES), to=max(EV_VALUES),
                length=225, showvalue=False, sliderlength=20,
                troughcolor='#af5032', borderwidth=0, orient='horizontal')
        self.scale['hp'].config(command=self._update_hp_scale)
        self.scale['atk'].config(command=self._update_atk_scale)
        self.scale['def'].config(command=self._update_def_scale)
        self.scale['spa'].config(command=self._update_spa_scale)
        self.scale['spd'].config(command=self._update_spd_scale)
        self.scale['spe'].config(command=self._update_spe_scale)

        self.scale_widgets = []
        for i, stat in enumerate(self.scale.keys()):
            self.scale_widgets.append(self.canvas2.create_window((350,50+25*i), window=self.scale[stat]))
            self.canvas2.itemconfig(self.scale_widgets[i], state='hidden')

        # iv stats
        self.iv_stats = [tk.StringVar() for i in range(6)]
        self.entry6 = []
        self.iv_stats_entry = []
        self.iv_trace = []
        for i in range(6):
            self.entry6.append(tk.Entry(self.canvas2, textvariable=self.iv_stats[i], width=7))
            self.entry6[i].insert(0,'31')
            self.iv_stats_entry.append(self.canvas2.create_window((500, 50+25*i), window=self.entry6[i]))
            self.canvas2.itemconfig(self.iv_stats_entry[i], state='hidden')
        for i, stat in enumerate(['hp_stat', 'atk_stat', 'def_stat', 'spa_stat', 'spd_stat', 'spe_stat']):
            self.iv_trace.append(self.iv_stats[i].trace('w', lambda name, index, mode, i=i, stat=stat: self._update_all_stats(i, stat)))

        # import/export
        self.i_box = tk.Text(self.canvas2, height=20, width=75)
        self.import_box = self.canvas2.create_window((325,215), window=self.i_box)
        self.canvas2.itemconfig(self.import_box, state='hidden')
        self.i_back = tk.Button(self.canvas2, text='Back', width=10, command=lambda: self._get_pokemon_list(check=True))
        self.i_save = tk.Button(self.canvas2, text='Save', width=10, command=self._save_import)
        self.i_back_button = self.canvas2.create_window((100,25), window=self.i_back)
        self.i_save_button = self.canvas2.create_window((200,25), window=self.i_save)
        self.canvas2.itemconfig(self.i_back_button, state='hidden')
        self.canvas2.itemconfig(self.i_save_button, state='hidden')

    def _get_images(self, key):
        # return a dictionary of images based on the key/directory
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
                    # TODO FIXME: Add dynamax images
                    temp_dict[object_name] = [normal_img, hover_img, RGBAImage('pokemon', normal_filename.replace('-hover', ''))]
                else:
                    temp_dict[object_name] = [normal_img, hover_img]

        return temp_dict

    def _format_evs(self):
        # get the showdown formatted string for EVs
        ev_spread = [i.get().replace('+', '').replace('-', '') for i in self.ev_stats]
        evs = {'HP' : ev_spread[0] if ev_spread[0] else None,
               'Atk' : ev_spread[1] if ev_spread[1] else None,
               'Def' : ev_spread[2] if ev_spread[2] else None,
               'SpA' : ev_spread[3] if ev_spread[3] else None,
               'SpD' : ev_spread[4] if ev_spread[4] else None,
               'Spe' : ev_spread[5] if ev_spread[5] else None}
        return ' / '.join(['%s %s' %(value, key) for (key, value) in evs.items() if value])

    def _format_ivs(self):
        # get the showdown formatted string for IVs
        iv_spread = [i.get().replace('+', '').replace('-', '') for i in self.iv_stats]
        ivs = {'HP' : iv_spread[0] if iv_spread[0] != '31' else None,
               'Atk' : iv_spread[1] if iv_spread[1] != '31' else None,
               'Def' : iv_spread[2] if iv_spread[2] != '31' else None,
               'SpA' : iv_spread[3] if iv_spread[3] != '31' else None,
               'SpD' : iv_spread[4] if iv_spread[4] != '31' else None,
               'Spe' : iv_spread[5] if iv_spread[5] != '31' else None}
        return ' / '.join(['%s %s' %(value, key) for (key, value) in ivs.items() if value])

    def _save_import(self):
        def _string_isolate(string, bool):
            return ''.join(char for char in string if char.isdigit() == bool).replace(' ', '')

        # import/export the set
        if self.i_box.get('1.0', 'end-1c') == '':
            return

        # parse the input
        input = self.i_box.get('1.0', 'end-1c').splitlines()
        if len(input) > 9:
            input = input[:8]
        name = input[0].split('@')[0].strip()
        if not name.casefold() in self.images['pokemon'].keys():
            return
        item = '' if '@' not in input[0] else input[0].split('@')[1].strip()
        if not item.casefold() in self.images['items'].keys():
            return
        ability = input[1][9:].strip()
        if not ability.casefold() in self._get_abilities(name):
            return
        ev_index = -1
        iv_index = -1
        nat_index = -1
        move_index = []
        for i in range(len(input)):
            if 'EVs:' in input[i]:
                ev_index = i
            if 'IVs:' in input[i]:
                iv_index = i
            if 'Nature' in input[i]:
                nat_index = i
            if input[i].startswith('- '):
                move_index.append(i)
        ev_dict = {'HP': '0', 'Atk': '0', 'Def': '0', 'SpA': '0', 'SpD': '0', 'Spe': '0'}
        if ev_index != -1:
            ev_string = input[ev_index][4:]
            for e in ev_string.split('/'):
                ev_dict[_string_isolate(e.strip(), False)] = _string_isolate(e.strip(), True)
        iv_dict = {'HP': '31', 'Atk': '31', 'Def': '31', 'SpA': '31', 'SpD': '31', 'Spe': '31'}
        if iv_index != -1:
            iv_string = input[iv_index][4:]
            for i in iv_string.split('/'):
                iv_dict[_string_isolate(i.strip(), False)] = _string_isolate(i.strip(), True)
        if nat_index != -1:
            nature = input[nat_index].split()[0].strip()
        moves = []
        for i in move_index:
            moves.append(input[i][2:].strip())

        # assign values
        self.pkmn.set(name)
        self.item.set(item)
        self.ability.set(ability)
        for i in range(len(moves)):
            self.moves[i].set(moves[i])
        for i, (_, value) in enumerate(ev_dict.items()):
            self.ev_stats[i].set(value)
        for i, (_, value) in enumerate(iv_dict.items()):
            self.iv_stats[i].set(value)

        # revert to normal screen state
        self.canvas.itemconfig(self.item_text, state='normal')
        self.canvas.itemconfig(self.item_entry, state='normal')
        self.canvas.itemconfig(self.ability_text, state='normal')
        self.canvas.itemconfig(self.ability_entry, state='normal')
        self.canvas.itemconfig(self.pokemon_icon, image=self.images['pokemon'][name.casefold()][2])
        self.canvas.itemconfig(self.moves_text, state='normal')
        for i in range(4):
            self.canvas.itemconfig(self.moves_entry[i], state='normal')
        self.canvas.itemconfig(self.stats_text, state='normal')
        self.canvas.itemconfig(self.stats_button, state='normal')
        self.canvas.itemconfig(self.clear_button, state='normal')
        self.canvas.itemconfig(self.save_button, state='normal')
        if not self.revealed:
            self.revealed = True
        self._get_stats_screen()

    def _set_nature(self, nature):
        self.display_nature.set(nature)
        self.nature.set(self._natures[nature])

        # update the stat entry fields with + or - if needed
        if '+Atk' in nature:
            self.entry5[1].insert(tk.END, '+')
        elif '+Def' in nature:
            self.entry5[2].insert(tk.END, '+')
        elif '+SpA' in nature:
            self.entry5[3].insert(tk.END, '+')
        elif '+SpD' in nature:
            self.entry5[4].insert(tk.END, '+')
        elif '+Spe' in nature:
            self.entry5[5].insert(tk.END, '+')

        if '-Atk' in nature:
            self.entry5[1].insert(tk.END, '-')
        elif '-Def' in nature:
            self.entry5[2].insert(tk.END, '-')
        elif '-SpA' in nature:
            self.entry5[3].insert(tk.END, '-')
        elif '-SpD' in nature:
            self.entry5[4].insert(tk.END, '-')
        elif '-Spe' in nature:
            self.entry5[5].insert(tk.END, '-')

        if '+' not in nature and '-' not in nature:
            for i in range(1,6):
                entry_value = self.entry5[i].get()
                entry_value = entry_value.replace('+', '').replace('-', '')
                self.entry5[i].delete(0, tk.END)
                self.entry5[i].insert(0, entry_value)

    def _update_nature(self):
        # check & update which stat(s) have + and -
        pos_stat = None
        neg_stat = None
        stat = ['hp', 'attack', 'defense', 'spattack', 'spdefense', 'speed']
        for i in range(1, 6):
            if self.ev_stats[i].get().startswith('+') or self.ev_stats[i].get().endswith('+'):
                self.positive_stat.append(stat[i])
                pos_stat = stat_conversion[i]
                if len(self.positive_stat) > 2:
                    continue
                if len(self.positive_stat) == 2:
                    del self.positive_stat[0]
            if self.ev_stats[i].get().startswith('-') or self.ev_stats[i].get().endswith('-'):
                self.negative_stat.append(stat[i])
                neg_stat = stat_conversion[i]
                if len(self.negative_stat) > 2:
                    continue
                if len(self.negative_stat) == 2:
                    del self.negative_stat[0]

        # error checking and internal correcting
        if pos_stat == neg_stat:
            return
        if pos_stat == None:
            self.positive_stat = []
        if neg_stat == None:
            self.negative_stat = []

        # update the nature if everything is good
        if len(self.positive_stat) == 1 and len(self.negative_stat) == 1:
            for nat, stat_combo in nature_dex.items():
                if stat_combo == (pos_stat, neg_stat):
                    nature = nat
                    break
            self.nature.set(nature)
            for key, val in self._natures.items():
                if val == nature:
                    self.display_nature.set(key)
                    break

    def _update_all_stats(self, index, stat):
        # process internal values and update nature if + or - in entry field
        iv = self.iv_stats[index].get().replace('+', '').replace('-', '').replace(' ', '')
        ev = self.ev_stats[index].get().replace('+', '').replace('-', '').replace(' ', '')
        if ev == '':
            ev = '0'
        if iv == '':
            iv = '0'
        self._update_nature()

        # error check and correct the entries
        if int(iv) > 31:
            self.iv_stats[index].set('31')
        if int(iv) < 0:
            self.iv_stats[index].set('0')
        if int(ev) > 252:
            self.ev_stats[index].set('252')
        if int(ev) <= 0:
            self.ev_stats[index].set(self.ev_stats[index].get().replace(ev, '') + '')

        # update respestive stat labels and scale
        # TODO FIXME: When updating nature here, only one of the labels updates, not the 2 that change
        self.canvas2.itemconfig(self.stat_labels[stat], text=str(get_stat(self.pkmn.get(), stat.replace('_stat', ''), iv, ev, self.nature.get())) if self.pkmn.get() else '999')
        self.scale[stat.replace('_stat', '')].set(int(ev))

        # update remaining label
        # TODO FIXME: have an upper limit of 508 EVs.
        stat_list = [i.get().replace('+', '').replace('-', '').replace(' ', '') for i in self.ev_stats]
        stat_list = map(lambda x: '0' if x == '' else x, stat_list)
        stat_sum = sum(int(i) for i in stat_list)
        self.canvas2.itemconfig(self.stat_labels['rem_value'], text=str(508-stat_sum))

    def _update_stat_entry(self, scale_value, stat):
        # do not allow 0 on respective entry field
        if scale_value == 0:
            scale_value = ''
        if self.ev_stats[stat].get().startswith('+'):
            self.ev_stats[stat].set('+' + scale_value)
        elif self.ev_stats[stat].get().endswith('+'):
            self.ev_stats[stat].set(scale_value + '+')
        elif self.ev_stats[stat].get().startswith('-'):
            self.ev_stats[stat].set('-' + scale_value)
        elif self.ev_stats[stat].get().endswith('-'):
            self.ev_stats[stat].set(scale_value + '-')
        else:
            self.ev_stats[stat].set(scale_value)

    def _update_hp_scale(self, value):
        self.scale['hp'].set(value)
        self._update_stat_entry(str(self.scale['hp'].get()), 0)

    def _update_atk_scale(self, value):
        self.scale['atk'].set(value)
        self._update_stat_entry(str(self.scale['atk'].get()), 1)

    def _update_def_scale(self, value):
        self.scale['def'].set(value)
        self._update_stat_entry(str(self.scale['def'].get()), 2)

    def _update_spa_scale(self, value):
        self.scale['spa'].set(value)
        self._update_stat_entry(str(self.scale['spa'].get()), 3)

    def _update_spd_scale(self, value):
        self.scale['spd'].set(value)
        self._update_stat_entry(str(self.scale['spd'].get()), 4)

    def _update_spe_scale(self, value):
        self.scale['spe'].set(value)
        self._update_stat_entry(str(self.scale['spe'].get()), 5)

    def _refresh_canvas(self, height):
        # re-pack canvas and scrollbar
        if height <= self.min_height:
            self.scrollbar.pack_forget()
        else:
            self.scrollbar.pack(side='right', fill='y')
        self.canvas2.pack_forget()
        self.canvas2.config(height=height, scrollregion=(0, 0, self._WIDTH, height))
        self.canvas2.pack(side='left', expand=True, fill='both')
        # move bg to new coordinates for scrolling
        x = self.canvas2.canvasx(0)
        y = self.canvas2.canvasy(0)
        self.canvas2.coords(self.inner_bg, x, y)

    def _get_screen(self, pokemon=False, item=False, ability=False, moves=False, stats=False, import_=False):
        # show/hide parts of screen depending on the screen we want to show
        for _ in self.pokemon_buttons.values():
            self.canvas2.itemconfig(_, state='normal' if pokemon else 'hidden')
        for _ in self.item_buttons.values():
            self.canvas2.itemconfig(_, state='normal' if item else 'hidden')
        for _ in self.ability_buttons.values():
            self.canvas2.itemconfig(_, state='normal' if ability else 'hidden')
        for _ in self.move_buttons.values():
            self.canvas2.itemconfig(_, state='normal' if moves else 'hidden')
        for i in range(6):
            self.canvas2.itemconfig(self.ev_stats_entry[i], state='normal' if stats else 'hidden')
            self.canvas2.itemconfig(self.scale_widgets[i], state='normal' if stats else 'hidden')
            self.canvas2.itemconfig(self.iv_stats_entry[i], state='normal' if stats else 'hidden')
        for _ in self.stat_labels.values():
            self.canvas2.itemconfig(_, state='normal' if stats else 'hidden')
        self.canvas2.itemconfig(self.nature_widget, state='normal' if stats else 'hidden')
        self.canvas2.itemconfig(self.i_back_button, state='normal' if import_ else 'hidden')
        self.canvas2.itemconfig(self.i_save_button, state='normal' if import_ else 'hidden')
        self.canvas2.itemconfig(self.import_box, state='normal' if import_ else 'hidden')
        self.entry.config(state='disabled' if import_ else 'normal')
        self.entry2.config(state='disabled' if import_ else 'normal')
        self.entry3.config(state='disabled' if import_ else 'normal')
        for entry in self.entry4:
            entry.config(state='disabled' if import_ else 'normal')
        if import_:
            self.entry.unbind('<Button-1>')
            self.entry2.unbind('<Button-1>')
            self.entry3.unbind('<Button-1>')
            for entry in self.entry4:
                entry.unbind('<Button-1>')
            self.canvas.tag_unbind(self.stats_button, '<Button-1>')
        else:
            self.entry.bind('<Button-1>', lambda event: self._get_pokemon_list(check=True))
            self.entry2.bind('<Button-1>', lambda event: self._get_item_list(check=True))
            self.entry3.bind('<Button-1>', lambda event: self._get_ability_list())
            for entry in self.entry4:
                entry.bind('<Button-1>', lambda event: self._get_move_list())
            self.canvas.tag_bind(self.stats_button, '<Button-1>', lambda event: self._get_stats_screen())

    def _get_import_screen(self):
        self._get_screen(import_=True)
        self._refresh_canvas(self.min_height)

        # get existing set info and overwrite into entry field
        text = ''
        if self.pkmn.get():
            if self.item.get():
                text += self.pkmn.get() + ' @ ' + self.item.get() + '\n'
            else:
                text += self.pkmn.get() + '\n'
            text += 'Ability: ' + self.ability.get() + '\n'
            if self._format_evs():
                text += 'EVs: ' + self._format_evs() + '\n'
            text += self.nature.get() + ' Nature\n'
            if self._format_ivs():
                text += 'IVs: ' + self._format_ivs() + '\n'
            for i in self.moves:
                if i.get():
                    text += '- ' + i.get() + '\n'
        self.i_box.delete('1.0', tk.END)
        self.i_box.insert(tk.END, text)

    def _get_stats_screen(self):
        self._get_screen(stats=True)
        # fill in values for each stat
        self.canvas2.itemconfig(self.stat_labels['hp_base'], text=str(POKEMON_LIST[self.pkmn.get()].base_hp) if self.pkmn.get() else '999')
        self.canvas2.itemconfig(self.stat_labels['atk_base'], text=str(POKEMON_LIST[self.pkmn.get()].base_attack) if self.pkmn.get() else '999')
        self.canvas2.itemconfig(self.stat_labels['def_base'], text=str(POKEMON_LIST[self.pkmn.get()].base_defense) if self.pkmn.get() else '999')
        self.canvas2.itemconfig(self.stat_labels['spa_base'], text=str(POKEMON_LIST[self.pkmn.get()].base_spattack) if self.pkmn.get() else '999')
        self.canvas2.itemconfig(self.stat_labels['spd_base'], text=str(POKEMON_LIST[self.pkmn.get()].base_spdefense) if self.pkmn.get() else '999')
        self.canvas2.itemconfig(self.stat_labels['spe_base'], text=str(POKEMON_LIST[self.pkmn.get()].base_speed))
        self.canvas2.itemconfig(self.stat_labels['hp_stat'], text=str(get_stat(self.pkmn.get(), 'hp', self.iv_stats[0].get(), self.ev_stats[0].get().replace('+', '').replace('-', '').replace(' ', ''), self.nature.get())) if self.pkmn.get() else '999')
        self.canvas2.itemconfig(self.stat_labels['atk_stat'], text=str(get_stat(self.pkmn.get(), 'atk', self.iv_stats[1].get(), self.ev_stats[1].get().replace('+', '').replace('-', '').replace(' ', ''), self.nature.get())) if self.pkmn.get() else '999')
        self.canvas2.itemconfig(self.stat_labels['def_stat'], text=str(get_stat(self.pkmn.get(), 'def', self.iv_stats[2].get(), self.ev_stats[2].get().replace('+', '').replace('-', '').replace(' ', ''), self.nature.get())) if self.pkmn.get() else '999')
        self.canvas2.itemconfig(self.stat_labels['spa_stat'], text=str(get_stat(self.pkmn.get(), 'spa', self.iv_stats[3].get(), self.ev_stats[3].get().replace('+', '').replace('-', '').replace(' ', ''), self.nature.get())) if self.pkmn.get() else '999')
        self.canvas2.itemconfig(self.stat_labels['spd_stat'], text=str(get_stat(self.pkmn.get(), 'spd', self.iv_stats[4].get(), self.ev_stats[4].get().replace('+', '').replace('-', '').replace(' ', ''), self.nature.get())) if self.pkmn.get() else '999')
        self.canvas2.itemconfig(self.stat_labels['spe_stat'], text=str(get_stat(self.pkmn.get(), 'spe', self.iv_stats[5].get(), self.ev_stats[5].get().replace('+', '').replace('-', '').replace(' ', ''), self.nature.get())) if self.pkmn.get() else '999')
        self._refresh_canvas(self.min_height)

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
            return
        return [i.casefold() for i in POKEMON_LIST[pokemon_name].abilities]

    def _get_moves(self, pokemon_name):
        pokemon_name = pokemon_name.replace('-Gmax', '')
        if pokemon_name not in POKEMON_LIST.keys():
            return
        return [i.casefold() for i in POKEMON_LIST[pokemon_name].attacks]

    def _get_pokemon_list(self, check=False):
        self._get_screen(pokemon=True)
        if check:
            search_list = []
            for pkmn in self.images['pokemon'].keys():
                if pkmn.startswith(self.entry.get().casefold()):
                    search_list.append(pkmn)
            new_height = len(search_list)*65+15
            self._refresh_canvas(new_height if new_height > self.min_height else self.min_height)
        else:
            # TODO FIXME: if I click the entry field, do not filter and give me full list again.
            self._refresh_canvas(self.pkmn_canvas_height)

    def _pick_pokemon(self, pkmn_name):
        # show all the other entry fields
        if not self.revealed:
            self.canvas.itemconfig(self.item_text, state='normal')
            self.canvas.itemconfig(self.item_entry, state='normal')
            self.canvas.itemconfig(self.ability_text, state='normal')
            self.canvas.itemconfig(self.ability_entry, state='normal')
            self.canvas.itemconfig(self.moves_text, state='normal')
            for i in range(4):
                self.canvas.itemconfig(self.moves_entry[i], state='normal')
            self.canvas.itemconfig(self.stats_text, state='normal')
            self.canvas.itemconfig(self.stats_button, state='normal')
            self.canvas.itemconfig(self.clear_button, state='normal')
            self.canvas.itemconfig(self.save_button, state='normal')
            self.revealed = True
        self.canvas.itemconfig(self.pokemon_icon, image=self.images['pokemon'][pkmn_name.casefold()][2])

        # format and overwrite pokemon name onto correct entry field
        name = [word.capitalize() for word in pkmn_name.split()]
        pkmn_name = ' '.join(name)
        if pkmn_name not in ['Jangmo-o', 'Hakamo-o', 'Kommo-o'] and '-' in pkmn_name:
            name = [word.capitalize() for word in pkmn_name.split('-')]
            pkmn_name = '-'.join(name)
        self.entry.delete(0,tk.END)
        self.entry.insert(0,pkmn_name)
        self.entry2.delete(0,tk.END)
        if pkmn_name.startswith('Silvally-'):
            text = pkmn_name.split('-')[1] + ' Memory'
        elif pkmn_name == 'Zacian-Crowned':
            text = 'Rusted Sword'
        elif pkmn_name == 'Zamazenta-Crowned':
            text = 'Rusted Shield'
        else:
            text = ''
        self.entry2.insert(0,text)
        self.entry3.delete(0,tk.END)
        self.entry3.insert(0,'')

        # delete existing ability buttons and get this Pokemon's abilities
        for ability, button in self.ability_buttons.items():
            self.canvas2.delete(button)
        self.ability_buttons = {}
        abil_list = self._get_abilities(pkmn_name)

        # make new ability buttons
        for i, ability in enumerate(abil_list):
            try:
                self.ability_buttons[ability] = self.canvas2.create_image((315,40+65*i), image=self.images['abilities'][ability][0])
                self.canvas2.tag_bind(self.ability_buttons[ability], '<Enter>', lambda event, abil=ability, img=self.images['abilities'][ability]: self._on_hover(self.canvas2, self.ability_buttons[abil], img[1], sound=True))
                self.canvas2.tag_bind(self.ability_buttons[ability], '<Leave>', lambda event, abil=ability, img=self.images['abilities'][ability]: self._on_hover(self.canvas2, self.ability_buttons[abil], img[0]))
                self.canvas2.tag_bind(self.ability_buttons[ability], '<Button-1>', lambda event, abil=ability: self._pick_ability(abil.capitalize()))
            except:
                print('Missing Ability:', ability)

        # delete existing move buttons and get this Pokemon's moves
        for move, button in self.move_buttons.items():
            self.canvas2.delete(button)
        self.move_buttons = {}
        move_list = self._get_moves(pkmn_name)

        # make new move buttons
        for i, move in enumerate(move_list):
            try:
                self.move_buttons[move] = self.canvas2.create_image((315,40+65*i), image=self.images['attacks'][move][0])
                self.canvas2.tag_bind(self.move_buttons[move], '<Enter>', lambda event, move=move, img=self.images['attacks'][move]: self._on_hover(self.canvas2, self.move_buttons[move], img[1], sound=True))
                self.canvas2.tag_bind(self.move_buttons[move], '<Leave>', lambda event, move=move, img=self.images['attacks'][move]: self._on_hover(self.canvas2, self.move_buttons[move], img[0]))
                self.canvas2.tag_bind(self.move_buttons[move], '<Button-1>', lambda event, move=move: self._pick_move(move.capitalize()))
            except:
                print('Missing Attack:', move)

        # move to next part
        if pkmn_name.startswith('Silvally-') or pkmn_name.endswith('-Crowned'):
            self.entry3.focus_set()
            self._get_ability_list()
        else:
            self.entry2.focus_set()
            self._get_item_list()

    def _get_item_list(self, check=False):
        self._get_screen(item=True)
        if check:
            search_list = []
            for item in self.images['items'].keys():
                if item.startswith(self.entry2.get().casefold()):
                    search_list.append(item)
            new_height = len(search_list)*65+15
            self._refresh_canvas(new_height if new_height > self.min_height else self.min_height)
        else:
            # TODO FIXME: if I click the entry field, do not filter and give me full list again.
            self._refresh_canvas(self.item_canvas_height)

    def _pick_item(self, item_name):
        # format and overwrite item onto correct entry field
        name = [word.capitalize() for word in item_name.split()]
        item_name = ' '.join(name)
        self.entry2.delete(0,tk.END)
        self.entry2.insert(0,item_name)
        self.entry3.focus_set()
        self._get_ability_list()

    def _get_ability_list(self):
        self._get_screen(ability=True)
        self._refresh_canvas(self.min_height)

    def _pick_ability(self, ability_name):
        # format and overwrite ability onto correct entry field
        name = [word.capitalize() for word in ability_name.split()]
        ability_name = ' '.join(name)
        ability_name = ability_name.replace('Rks', 'RKS')
        self.entry3.delete(0,tk.END)
        self.entry3.insert(0,ability_name)
        self.entry4[0].focus_set()
        self._get_move_list()

    def _get_move_list(self):
        self._get_screen(moves=True)
        height = len(self._get_moves(self.entry.get()))*65+15
        self._refresh_canvas(height if height > self.min_height else self.min_height)

    def _pick_move(self, attack_name):
        # format and overwrite move onto correct entry field
        attack_name = ' '.join([word.capitalize() for word in attack_name.split()])
        if 'v-create' == attack_name.lower():
            attack_name = 'V-create'
        elif 'power-up punch' == attack_name.lower():
            attack_name = 'Power-Up Punch'
        elif '-' in attack_name:
            attack_name = '-'.join([word.capitalize() for word in attack_name.split('-')])
        else:
            pass
        slot = self.entry4.index(self.focus_get())
        self.moves[slot].trace_vdelete('w', self.move_trace[slot])
        del self.move_trace[slot]
        self.entry4[slot].delete(0,tk.END)
        self.entry4[slot].insert(0,attack_name)
        self.move_trace.insert(slot, self.moves[slot].trace('w', lambda name, index, mode, moves=self.moves, i=slot: self._filter(moves[i], 'attacks', self.images['attacks'])))

        # move to next field or stats
        if slot < 3:
            self.entry4[slot+1].focus_set()
        else:
            self._get_stats_screen()

    def _filter(self, name, buttons, images):
        # get list of matching elements
        search_list = []
        if buttons == 'pokemon' or buttons == 'items':
            for x in images.keys():
                if x.startswith(name.get().casefold()):
                    search_list.append(x)
        else:
            if buttons == 'abilities':
                if self._get_abilities(self.entry.get()):
                    for abil in self._get_abilities(self.entry.get()):
                        if abil.casefold().startswith(name.get().casefold()):
                            search_list.append(abil.casefold())
            if buttons == 'attacks':
                if self._get_moves(self.entry.get()):
                    for move in self._get_moves(self.entry.get()):
                        if move.casefold().startswith(name.get().casefold()):
                            search_list.append(move.casefold())
        if not search_list:
            return

        # clear canvas of all buttons
        if buttons == 'pokemon':
            for _, button in self.pokemon_buttons.items():
                self.canvas2.delete(button)
            self.pokemon_buttons = {}
        elif buttons == 'items':
            for _, button in self.item_buttons.items():
                self.canvas2.delete(button)
            self.item_buttons = {}
        elif buttons == 'abilities':
            for _, button in self.ability_buttons.items():
                self.canvas2.delete(button)
            self.ability_buttons = {}
        # TODO FIXME: add moves/attacks

        # resize canvas

        self._refresh_canvas(len(search_list)*65+15 if len(search_list)*65+15 > self.min_height else self.min_height)

        # repopulate canvas with new list
        for i, list_item in enumerate(search_list):
            if buttons == 'pokemon':
                try:
                    self.pokemon_buttons[list_item] = self.canvas2.create_image((315,40+65*i), image=images[list_item][0])
                    self.canvas2.tag_bind(self.pokemon_buttons[list_item], '<Enter>', lambda event, item=list_item, img=images[list_item]: self._on_hover(self.canvas2, self.pokemon_buttons[item], img[1], sound=True))
                    self.canvas2.tag_bind(self.pokemon_buttons[list_item], '<Leave>', lambda event, item=list_item, img=images[list_item]: self._on_hover(self.canvas2, self.pokemon_buttons[item], img[0]))
                    self.canvas2.tag_bind(self.pokemon_buttons[list_item], '<Button-1>', lambda event, item=list_item: self._pick_pokemon(item.capitalize()))
                except:
                    print('Missing Pokemon:', list_item)
            elif buttons == 'items':
                try:
                    self.item_buttons[list_item] = self.canvas2.create_image((315,40+65*i), image=images[list_item][0])
                    self.canvas2.tag_bind(self.item_buttons[list_item], '<Enter>', lambda event, item=list_item, img=images[list_item]: self._on_hover(self.canvas2, self.item_buttons[item], img[1], sound=True))
                    self.canvas2.tag_bind(self.item_buttons[list_item], '<Leave>', lambda event, item=list_item, img=images[list_item]: self._on_hover(self.canvas2, self.item_buttons[item], img[0]))
                    self.canvas2.tag_bind(self.item_buttons[list_item], '<Button-1>', lambda event, item=list_item: self._pick_item(item.capitalize()))
                except:
                    print('Missing Item:', list_item)
            elif buttons == 'abilities':
                try:
                    self.ability_buttons[list_item] = self.canvas2.create_image((315,40+65*i), image=images[list_item][0])
                    self.canvas2.tag_bind(self.ability_buttons[list_item], '<Enter>', lambda event, item=list_item, img=images[list_item]: self._on_hover(self.canvas2, self.ability_buttons[item], img[1], sound=True))
                    self.canvas2.tag_bind(self.ability_buttons[list_item], '<Leave>', lambda event, item=list_item, img=images[list_item]: self._on_hover(self.canvas2, self.ability_buttons[item], img[0]))
                    self.canvas2.tag_bind(self.ability_buttons[list_item], '<Button-1>', lambda event, item=list_item: self._pick_ability(item.capitalize()))
                except:
                    print('Missing Ability:', list_item)
            else:
                print('Error: i=', i, 'list_item=', list_item, 'buttons=', buttons)

    def _on_hover(self, canvas, button, image, sound=False):
        canvas.itemconfig(button, image=image)
        if sound:
            sfx['move'].play()

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

    def _get_checks(self):
        pass

    def _get_counters(self):
        pass

    def clear_page(self):
        # reset all fields
        self.pkmn.set('')
        self.item.set('')
        self.ability.set('')
        for i in self.moves:
            i.set('')
        for i in self.ev_stats:
            i.set('')
        for i in self.iv_stats:
            i.set('31')
        self.nature.set('Serious')
        self.canvas.itemconfig(self.item_text, state='hidden')
        self.canvas.itemconfig(self.item_entry, state='hidden')
        self.canvas.itemconfig(self.ability_text, state='hidden')
        self.canvas.itemconfig(self.ability_entry, state='hidden')
        self.canvas.itemconfig(self.pokemon_icon, image=self.images['other'])
        self.canvas.itemconfig(self.moves_text, state='hidden')
        for i in range(4):
            self.canvas.itemconfig(self.moves_entry[i], state='hidden')
        self.canvas.itemconfig(self.stats_text, state='hidden')
        self.canvas.itemconfig(self.stats_button, state='hidden')
        self.canvas.itemconfig(self.clear_button, state='hidden')
        self.canvas.itemconfig(self.save_button, state='hidden')
        self.revealed = False
        sfx['back_page'].play()
        self._get_pokemon_list()

    def _save_set(self):
        # check if certain fields are filled in
        if self.pkmn.get() not in POKEMON_LIST.keys() or self.ability.get() == '':
            return

        # update the database if the set is new
        set = PokemonSet(self.pkmn.get(), '100', self.item.get(), self.ability.get(), self._format_evs(), self.nature.get(), self._format_ivs(), [move.get() for move in self.moves if move.get()])
        if not exists(set):
            update_database(set)
            # TODO FIXME: have a visual indicator that the set was saved and prompt if user wants to continue editing or start over.
            sfx['save'].play()


class EditSetPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.pack_propagate(0)
        self.images = {'bg'        : [RGBAImage('menu', 'edit_bg.png'), RGBAImage('menu', 'edit_inner_bg.png')],
                       'buttons'   : {'back'  : [RGBAImage('menu', 'back_button.png'), RGBAImage('menu', 'back_button2.png')],
                                      'blank' : RGBAImage('menu', 'blank.png')},
                       'pokemon'   : self._get_sprites(),
                       'other'     : RGBAImage('menu', 'sorry.png')}
        self.min_height = 555
        self._WIDTH = 651
        self.TESTHEIGHT = 10000
        self.canvas = tk.Canvas(self, height=self._WIDTH, width=self._WIDTH, highlightthickness=0)
        self.canvas.pack()
        self.background = self.canvas.create_image((0,0), image=self.images['bg'][0], anchor='nw')
        # make a nested canvas
        self.in_frame = tk.Frame(self, height=self.min_height, width=self._WIDTH, borderwidth=0, highlightthickness=0)
        self.in_frame.pack_propagate(0)
        self.frame = self.canvas.create_window((0,96), window=self.in_frame, anchor='nw')
        self.canvas2 = tk.Canvas(self.in_frame, height=self.TESTHEIGHT, width=self._WIDTH, highlightthickness=0, scrollregion=(0, 0, self._WIDTH, self.TESTHEIGHT))
        self.inner_bg = self.canvas2.create_image((0,0), image=self.images['bg'][1], anchor='nw')
        self.scrollbar = tk.Scrollbar(self.in_frame, orient='vertical', command=self._custom_yview)
        self.scrollbar.pack(side='right', fill='y')
        self.canvas2.config(yscrollcommand=self.scrollbar.set)
        self.canvas2.pack(side='left', expand=True, fill='both')
        self.canvas2.bind('<Enter>', self._on_mousewheel)
        self.canvas2.bind('<Leave>', self._off_mousewheel)
        # the top of the bottom canvas
        self.origX = self.canvas2.xview()[0]
        self.origY = self.canvas2.yview()[0]

        # back button
        self.back_button = self.canvas.create_image((50,40), image=self.images['buttons']['back'][0])
        self.canvas.tag_bind(self.back_button, '<Enter>', lambda event: self._on_hover(self.canvas, self.back_button, self.images['buttons']['back'][1], sound=True))
        self.canvas.tag_bind(self.back_button, '<Leave>', lambda event: self._on_hover(self.canvas, self.back_button, self.images['buttons']['back'][0]))
        self.canvas.tag_bind(self.back_button, '<Button-1>', lambda event: self.controller._change_page('EditSetPage', 'MainPage'))

        # search bar
        self.pkmn = tk.StringVar()
        self.pokemon_text = self.canvas.create_text((230,60), text='Search:')
        self.entry = tk.Entry(self.canvas, textvariable=self.pkmn, width=25)
        self.entry.bind('<Button-1>', lambda event: self._get_screen(pokemon=True))
        self.pokemon_entry = self.canvas.create_window((340,60), window=self.entry)
        self.pkmn_trace = self.pkmn.trace('w', lambda name, index, mode, pkmn=self.pkmn: self._filter(pkmn, self.images['pokemon']))

        # bottom canvas
        self.pokemon_buttons = {}
        self.set_num_text = {}
        for i, pkmn in enumerate(self.images['pokemon'].keys()):
            self.pokemon_buttons[pkmn] = self.canvas2.create_image((120+200*(i%3)),120+200*int((i/3)), image=self.images['pokemon'][pkmn])
            self.canvas2.tag_bind(self.pokemon_buttons[pkmn], '<Button-1>', lambda event, pkmn=pkmn: self._pick_pokemon(pkmn))
            self.set_num_text[pkmn] = self.canvas2.create_text((120+200*(i%3)),70+200*int((i/3)), text='0 Sets') # TODO FIXME: change 0 to calculated amount

        self.set_buttons = {}

        # self.sorry = self.canvas.create_image((320,200), image=self.images['other'])

    def _get_sprites(self):
        temp_dict = {}
        for file in os.listdir(os.fsencode(str(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'media', 'sprites')))):
            if os.fsdecode(file).endswith('.png'):
                temp_dict[os.fsdecode(file).replace('e null', 'e: null').replace('mr ', 'mr. ').replace(' jr', ' jr.').replace('.png', '')] = ImageTk.PhotoImage(Image.open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'media', 'sprites', os.fsdecode(file))).convert('RGBA'))

        return temp_dict

    def _refresh_canvas(self, height):
        # re-pack canvas and scrollbar
        if height <= self.min_height:
            self.scrollbar.pack_forget()
        else:
            self.scrollbar.pack(side='right', fill='y')
        self.canvas2.pack_forget()
        self.canvas2.config(height=height, scrollregion=(0, 0, self._WIDTH, height))
        self.canvas2.pack(side='left', expand=True, fill='both')
        # move bg to new coordinates for scrolling
        x = self.canvas2.canvasx(0)
        y = self.canvas2.canvasy(0)
        self.canvas2.coords(self.inner_bg, x, y)

    def _filter(self, name, images):
        # get list of matching pokemon
        search_list = []
        for x in images.keys():
            if x.startswith(name.get().casefold()):
                search_list.append(x)
        if not search_list:
            return

        # clear canvas of all buttons and text
        for _, button in self.pokemon_buttons.items():
            self.canvas2.delete(button)
        self.pokemon_buttons = {}
        for _, text in self.set_num_text.items():
            self.canvas2.delete(text)
        self.set_num_text = {}

        # resize canvas
        # TODO FIXME: get real height values for images
        self._refresh_canvas(len(search_list)*65+15 if len(search_list)*65+15 > self.min_height else self.min_height)

        # repopulate canvas with new list
        for i, pkmn in enumerate(search_list):
            try:
                self.pokemon_buttons[pkmn] = self.canvas2.create_image((120+200*(i%3)),120+200*int((i/3)), image=images[pkmn])
                self.set_num_text[pkmn] = self.canvas2.create_text((120+200*(i%3)),70+200*int((i/3)), text='0 Sets') # TODO FIXME: change 0 to calculated amount
                self.canvas2.tag_bind(self.pokemon_buttons[pkmn], '<Button-1>', lambda event, pkmn=pkmn: self._pick_pokemon(pkmn.capitalize()))
            except:
                print('Missing Pokemon:', i, pkmn)

    def _pick_pokemon(self, pkmn_name):
        # format pokemon name
        name = [word.capitalize() for word in pkmn_name.split()]
        pkmn_name = ' '.join(name)
        if pkmn_name not in ['Jangmo-o', 'Hakamo-o', 'Kommo-o'] and '-' in pkmn_name:
            name = [word.capitalize() for word in pkmn_name.split('-')]
            pkmn_name = '-'.join(name)

        # delete existing set buttons get this Pokemon's sets
        for _, button in self.set_buttons.items():
            self.canvas2.delete(button)
        self.set_buttons = {}
        set_list = self._get_set_list(pkmn_name)

        # make new set buttons
        for i, pset in enumerate(set_list):
            self.set_buttons[pset] = self.canvas2.create_image((315,40+65*i), image=self.images['buttons']['blank'])
            # TODO FIXME: Add set details in text form
            self.canvas2.tag_bind(self.set_buttons[pset], '<Button-1>', lambda event, name=pset.name: self._edit_set(name))
            print('hi1%d' %i)

        self._get_screen(sets=True)
        self._refresh_canvas(self.min_height)

    def _get_screen(self, pokemon=False, sets=False):
        # show/hide parts of screen depending on the screen we want to show
        for _ in self.pokemon_buttons.values():
            self.canvas2.itemconfig(_, state='normal' if pokemon else 'hidden')
        for _ in self.set_num_text.values():
            self.canvas2.itemconfig(_, state='normal' if pokemon else 'hidden')
        for _ in self.set_buttons.values():
            self.canvas2.itemconfig(_, state='normal' if sets else 'hidden')


    def _get_set_list(self, pkmn_name):
        set_list = []
        for pset in sets:
            if pset.name == pkmn_name:
                set_list.append(pset)
        return set_list

    def _edit_set(self, pkmn_name):
        # TODO FIXME: Add the ability to change to NewSetPage and fill out w/ set info.
        pass

    def _on_hover(self, canvas, button, image, sound=False):
        canvas.itemconfig(button, image=image)
        if sound:
            sfx['move'].play()

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


class TeamBuilderPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.pack_propagate(0)
        self.images = {'bg'        : RGBAImage('menu', 'team_bg.png'),
                       'buttons'   : {'back'  : [RGBAImage('menu', 'back_button.png'), RGBAImage('menu', 'back_button2.png')]},
                       'other'     : RGBAImage('menu', 'sorry.png')}
        self._WIDTH = 651
        self.canvas = tk.Canvas(self, height=self._WIDTH, width=self._WIDTH, highlightthickness=0)
        self.canvas.pack()
        self.background = self.canvas.create_image((0,0), image=self.images['bg'], anchor='nw')

        # back button
        self.back_button = self.canvas.create_image((50,40), image=self.images['buttons']['back'][0])
        self.canvas.tag_bind(self.back_button, '<Enter>', lambda event: self._on_hover(self.canvas, self.back_button, self.images['buttons']['back'][1], sound=True))
        self.canvas.tag_bind(self.back_button, '<Leave>', lambda event: self._on_hover(self.canvas, self.back_button, self.images['buttons']['back'][0]))
        self.canvas.tag_bind(self.back_button, '<Button-1>', lambda event: self.controller._change_page('TeamBuilderPage', 'MainPage'))

        self.sorry = self.canvas.create_image((330,300), image=self.images['other'])

    def _on_hover(self, canvas, button, image, sound=False):
        canvas.itemconfig(button, image=image)
        if sound:
            sfx['move'].play()


class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.pack_propagate(0)
        # TODO FIXME: clean up images into dictionaries
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
            self.canvas.tag_bind(self.buttons[i], '<Enter>', lambda event, i=i: self._on_hover(self.canvas, self.buttons[i], self.button_imgs_hover[i]))
            self.canvas.tag_bind(self.buttons[i], '<Leave>', lambda event, i=i: self._on_hover(self.canvas, self.buttons[i], self.button_imgs[i]))
        self.canvas.tag_bind(self.buttons[0], '<Button-1>', lambda event: self.controller._change_page('MainPage', 'NewSetPage'))
        self.canvas.tag_bind(self.buttons[1], '<Button-1>', lambda event: self.controller._change_page('MainPage', 'EditSetPage'))
        self.canvas.tag_bind(self.buttons[2], '<Button-1>', lambda event: self.controller._change_page('MainPage', 'TeamBuilderPage'))
        self.canvas.tag_bind(self.buttons[3], '<Button-1>', lambda event: self.controller.quit())

    # TODO FIXME: When changing pages, the sound plays twice.
    def _on_hover(self, canvas, button, image, sound=False):
        canvas.itemconfig(button, image=image)
        if sound:
            sfx['move2'].play()


class Rentals (tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # make the base window
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill='both', expand=True)
        self.pages = {}

        # initialize each page
        for page in [MainPage, NewSetPage, EditSetPage, TeamBuilderPage,]:
            frame = page(parent=self.main_frame, controller=self)
            self.pages[page.__name__] = frame
            frame.pack(fill='both', expand=True)

        # hide each page for now
        for page in ['NewSetPage', 'EditSetPage', 'TeamBuilderPage',]:
            self.pages[page].pack_forget()

    def _change_page(self, old_page_name, page_name):
        if page_name == 'MainPage':
            sfx['load_main_menu'].play()
        else:
            sfx['change_screen'].play()
        frame = self.pages[old_page_name]
        frame.pack_forget()
        frame = self.pages[page_name]
        frame.pack(fill='both', expand=True)


if __name__ == '__main__':
    dbapp = Rentals()

    dbapp.resizable(False, False)
    dbapp.geometry("651x651")
    dbapp.title('Pokemon Rentals v%s' %VERSION)
    dbapp.mainloop()
