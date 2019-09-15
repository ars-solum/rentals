from Pokemon import *

class DraftSettings(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        setup_game_settings(self, 'Draft')

    def update_gen_settings(self):
        # update the player and tier buttons
        mode = self.parent_page().battle_mode.get()
        for button in self.controller.pages['DraftGenerateSettings'].tier_buttons:
            button.config(state='normal' if (mode != 'Doubles') else 'disabled')
        for button in self.controller.pages['DraftGenerateSettings'].tier2_buttons:
            button.config(state='normal' if (mode == 'Doubles') else 'disabled')
        for button in self.player_option:
            button.grid() if (mode == 'SRL') else button.grid_remove()

    def reset_game(self):
        # end the current game
        if self.parent_page().game_activated:
            popup_message(self.controller, 'ERROR', 'Changing this setting has caused the current game to end.', text2='\nPlease start a new game.')
            self.parent_page().game_activated = False

        # clear the ban list and buttons
        for team in range(2):
            for slot in range(len(self.parent_page().ban_buttons[team])):
                self.parent_page().ban_buttons[team][slot].config(image=self.controller.img_blank['inactive'],
                    state='normal' if (slot < self.parent_page().ban_number.get()) else 'disabled', command=lambda: None)
        self.parent_page().ban_list = [[None, None], [None, None]]
        self.parent_page().ban_phase_finished = False
        self.parent_page().ban_text.config(state='normal' if (self.parent_page().ban_number.get()) else 'disabled')

        # clear the pool list and buttons
        for i in range(18):
            self.parent_page().pool_buttons[i].config(image=self.controller.img_blank['inactive'], command=lambda: None)
        self.parent_page().pkmn_pool_list = []
        self.parent_page().pkmn_not_picked = [True for i in range(18)]

        # clear the team lists, buttons, and indicator
        for team in self.parent_page().team_buttons:
            for button in team:
                button.config(image=self.controller.img_blank['inactive'], command=lambda: None)
        self.parent_page().pkmn_team_list = [[None for i in range(6)] for j in range(2)]
        self.parent_page().indicator.grid_remove()

    def parent_page(self):
        return self.controller.pages['Draft']
