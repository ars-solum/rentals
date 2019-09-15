import tkinter as tk
from Pokemon import *

class DraftGenerateSettings(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        setup_pkmn_settings(self, 'Draft')

    def parent_page(self):
        return self.controller.pages['Draft']
