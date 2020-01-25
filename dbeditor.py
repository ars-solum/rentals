import os
import xlrd
import xlwt
import tkinter as tk
from PIL import Image, ImageTk
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer

VERSION = '0.1'
mixer.init()

def RGBAImage(path):
    return ImageTk.PhotoImage(Image.open(path).convert('RGBA'))

def donothing():
    pass

class NewSetPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.button_imgs = [RGBAImage(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'media', 'Common', 'new_button.png'))),
                            RGBAImage(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'media', 'Common', 'edit_button.png'))),
                            RGBAImage(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'media', 'Common', 'team_button.png'))),
                            RGBAImage(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'media', 'Common', 'quit_button.png')))]
        self.test_buttons = []

class EditSetPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.button_imgs = [RGBAImage(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'media', 'Common', 'new_button.png'))),
                            RGBAImage(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'media', 'Common', 'edit_button.png'))),
                            RGBAImage(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'media', 'Common', 'team_button.png'))),
                            RGBAImage(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'media', 'Common', 'quit_button.png')))]
        self.test_buttons = []

class TeamPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.button_imgs = [RGBAImage(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'media', 'Common', 'new_button.png'))),
                            RGBAImage(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'media', 'Common', 'edit_button.png'))),
                            RGBAImage(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'media', 'Common', 'team_button.png'))),
                            RGBAImage(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'media', 'Common', 'quit_button.png')))]
        self.test_buttons = []

class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.bg_imgs = [RGBAImage(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'media', 'Common', 'testbg2.png')))]
        self.button_imgs = [RGBAImage(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'media', 'Common', 'new_button.png'))),
                            RGBAImage(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'media', 'Common', 'edit_button.png'))),
                            RGBAImage(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'media', 'Common', 'team_button.png'))),
                            RGBAImage(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'media', 'Common', 'quit_button.png')))]
        self.test_buttons = []

        self.background = tk.Label(self, image=self.bg_imgs[0], bd=0)
        self.pack_propagate(0)
        self.background.pack(fill='both', expand=True)
        for i in range(40):
            self.background.rowconfigure(i, weight=100)
            self.background.columnconfigure(i, weight=100)

        for i in range(4):
            self.test_buttons.append(tk.Button(self.background, image=self.button_imgs[i], bd=0.1, highlightthickness=0))
            self.test_buttons[i].grid(row=i, column=0, padx=6, pady=2)

        self.test_buttons[0].config(command=lambda:self.controller.change_page('MainPage', 'NewSetPage'))
        self.test_buttons[1].config(command=lambda:self.controller.change_page('MainPage', 'EditSetPage'))
        self.test_buttons[2].config(command=lambda:self.controller.change_page('MainPage', 'TeamPage'))
        self.test_buttons[3].config(command=self.controller.quit)




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
