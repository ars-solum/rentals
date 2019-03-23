class Sidebar(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.currPageSelected = 'Draft'
        self.prevPageSelected = None

    def on_enter(self, option):
        if option < 4:
            if self.currPageSelected == BATTLE_OPTIONS[option]:
                pass
            else:
                self.b_battleOptions[option].config(image=self.img_selected_button[option])
        else:
            if self.currPageSelected == AUCTION_OPTIONS[option-4]:
                pass
            else:
                self.b_auctionOptions[option-4].config(image=self.img_selected_button[option])

    def on_leave(self, option):
        if option < 4:
            if self.currPageSelected == BATTLE_OPTIONS[option]:
                self.b_battleOptions[option].config(image=self.img_selected_button[option])
            else:
                self.b_battleOptions[option].config(image=self.img_inactive_button[option])
        else:
            if self.currPageSelected == AUCTION_OPTIONS[option-4]:
                self.b_auctionOptions[option-4].config(image=self.img_selected_button[option])
            else:
                self.b_auctionOptions[option-4].config(image=self.img_inactive_button[option])

    def set_selected(self, mode):
        self.prevPageSelected = self.currPageSelected
        self.currPageSelected = mode

    def get_currSelected(self):
        return self.currPageSelected

    def get_prevSelected(self):
        return self.prevPageSelected

    def update_media(self):
        if self.currPageSelected != self.prevPageSelected:
            for i in range(4):
                if self.prevPageSelected == BATTLE_OPTIONS[i]:
                    self.b_battleOptions[i].config(image=self.img_inactive_button[i])
                    break
                if self.prevPageSelected == AUCTION_OPTIONS[i]:
                    self.b_auctionOptions[i].config(image=self.img_inactive_button[i+4])
                    break
        else:
            for i in range(4):
                if self.currPageSelected == BATTLE_OPTIONS[i]:
                    self.b_battleOptions[i].config(image=self.img_selected_button[i])
                    break
                if self.currPageSelected == AUCTION_OPTIONS[i]:
                    self.b_auctionOptions[i].config(image=self.img_selected_button[i+4])
                    break
