from Pokemon import *

class RandomGenerateSettings(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        setup_pkmn_settings(self, 'Random')

    def parent_page(self):
        return self.controller.pages['Random']
