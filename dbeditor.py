import xlrd
import xlwt
import tkinter as tk
from PIL import Image, ImageTk
import os

VERSION = '0.1'

def RGBAImage(path):
    return ImageTk.PhotoImage(Image.open(path).convert('RGBA'))

def donothing():
    pass

class DBEditor (tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.menubar = tk.Menu(self)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="New", command=donothing)
        self.filemenu.add_command(label="Open", command=donothing)
        self.filemenu.add_command(label="Save", command=donothing)
        self.filemenu.add_command(label="Save as...", command=donothing)
        self.filemenu.add_command(label="Close", command=donothing)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.editmenu = tk.Menu(self.menubar, tearoff=0)
        self.editmenu.add_command(label="Undo", command=donothing)
        self.editmenu.add_separator()
        self.editmenu.add_command(label="Cut", command=donothing)
        self.editmenu.add_command(label="Copy", command=donothing)
        self.editmenu.add_command(label="Paste", command=donothing)
        self.editmenu.add_command(label="Delete", command=donothing)
        self.editmenu.add_command(label="Select All", command=donothing)
        self.menubar.add_cascade(label="Edit", menu=self.editmenu)
        self.config(menu=self.menubar)

        self.test_img = [RGBAImage(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'media', 'SwSh', 'charizard-gi.png'))),
                         RGBAImage(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'media', 'SwSh', 'lapras-gi.png'))),
                         RGBAImage(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'media', 'SwSh', 'hoothoot.png')))]
        self.test_buttons = []

        for i in range(3):
            self.test_buttons.append(tk.Button(self, image=self.test_img[i], bd=0.1))
            self.test_buttons[i].grid(row=0, column=i, padx=10, pady=10)

if __name__ == '__main__':
    dbapp = DBEditor()

    dbapp.resizable(False, False)

    dbapp.title('Rentals DB Editor v%s' %VERSION)
    dbapp.mainloop()
