from Pokemon import *

class RandomSettings(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        setup_game_settings(self, 'Random')

    def update_gen_settings(self):
        page = self.controller.pages['RandomGenerateSettings']
        mode = self.parent_page().battle_mode.get()
        theme = self.parent_page().theme.get()
        for button in page.tier_buttons:
            button.config(state='normal' if (mode != 'Doubles') else 'disabled')
        for button in page.tier2_buttons:
            button.config(state='normal' if (mode == 'Doubles') else 'disabled')
        for button in self.player_option:
            button.grid() if (mode == 'SRL') else button.grid_remove()
        for button in self.type_option:
            button.grid() if (theme == 'Monotype') else button.grid_remove()
        for button in page.type_buttons:
            button.config(state='disabled' if (theme == 'Monotype') else 'normal')

    def parent_page(self):
        return self.controller.pages['Random']
