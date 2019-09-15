from Pokemon import *

class StoreSettings(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.banner_img = [RGBAImage(os.path.join(COMMON, 'week%s.png' % i)) for i in range(8)]
        self.cur_week = tk.IntVar()
        self.cur_week.set(int(get_banner_num()/2))
        # current banner
        self.banner = tk.Label(self, image=self.banner_img[self.cur_week.get()])
        self.banner.grid(row=0, column=0, columnspan=2, pady=5, sticky='nsew')

        # change weeks
        self.week_frame = tk.Frame(self)
        self.week_frame.grid(row=1, column=0, sticky='nsew')
        self.week_frame.grid_columnconfigure(0, weight=1)
        self.week_label = tk.Label(self.week_frame, text='Change the Current Week')
        self.week_label.grid(row=0, column=0, pady=5, sticky='nsew')
        self.week_buttons = []
        for i in range(8):
            self.week_buttons.append(tk.Radiobutton(
                self.week_frame,
                text='Week #%s' %str(i+1),
                variable=self.cur_week,
                value=i,
                command=self.change_banner_img))
            self.week_buttons[i].grid(row=i+1, column=0, pady=5)

        # change dates of weeks
        self.date_frame = tk.Frame(self)
        self.date_frame.grid(row=1, column=1, sticky='nsew')
        for i in range(4):
            self.date_frame.grid_columnconfigure(i, weight=1)
        self.date_label = tk.Label(self.date_frame, text='Modify Banner Schedule (Format: M/DD)')
        self.date_label.grid(row=0, column=0, pady=5, columnspan=4, sticky='nsew')
        self.start_label = [tk.Label(self.date_frame, text='Week %s Start Date:' %str(i+1)) for i in range(8)]
        self.end_label = [tk.Label(self.date_frame, text='End Date:') for i in range(8)]
        self.entry_box = [[tk.Entry(self.date_frame, width=10) for i in range(8)] for j in range(2)]
        for i in range(8):
            self.start_label[i].grid(row=i+1, column=0, padx=5, pady=7)
            self.end_label[i].grid(row=i+1, column=2, padx=5, pady=7)
        for i in range(2):
            for j in range(8):
                self.entry_box[i][j].grid(row=j+1, column=i*2+1, padx=5, pady=8)
        self.init_dates()

        # save buttons
        self.save_button = []
        self.save_button.append(tk.Button(self.week_frame, text="Change Week", command=self.save))
        self.save_button.append(tk.Button(self.date_frame, text="Save Schedule", state='disabled', width=20, command=self.save_schedule))
        self.save_button[0].grid(row=10, column=0, padx=5, pady=5, sticky='nsew')
        self.save_button[1].grid(row=10, column=0, columnspan=4, padx=5, pady=5)
        # back button
        self.back_button = tk.Button(self, image=self.controller.img_back['inactive'], bd=0.1, command=lambda: self.controller.change_page('Store'))
        self.back_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        self.back_button.bind('<Enter>', lambda event: self.controller.on_enter(self.back_button, self.controller.img_back['active']))
        self.back_button.bind('<Leave>', lambda event: self.controller.on_leave(self.back_button, self.controller.img_back['inactive']))

    def init_dates(self):
        self.entry_box[0][0].insert(0, '6/1')
        self.entry_box[1][0].insert(0, '6/8')
        self.entry_box[0][1].insert(0, '6/9')
        self.entry_box[1][1].insert(0, '6/15')
        self.entry_box[0][2].insert(0, '6/16')
        self.entry_box[1][2].insert(0, '6/22')
        self.entry_box[0][3].insert(0, '6/23')
        self.entry_box[1][3].insert(0, '6/29')
        self.entry_box[0][4].insert(0, '6/30')
        self.entry_box[1][4].insert(0, '7/6')
        self.entry_box[0][5].insert(0, '7/7')
        self.entry_box[1][5].insert(0, '7/13')
        self.entry_box[0][6].insert(0, '7/14')
        self.entry_box[1][6].insert(0, '7/20')
        self.entry_box[0][7].insert(0, '7/21')
        self.entry_box[1][7].insert(0, '7/27')
        for group in self.entry_box:
            for box in group:
                box.config(state='disabled')

    def save(self):
        self.change_week()

    def save_schedule(self):
        pass

    def change_banner_img(self):
        self.banner.config(image=self.banner_img[self.cur_week.get()])

    def change_week(self):
        self.controller.pages['Store'].banner_num = self.cur_week.get() * 2
        self.controller.pages['Store'].change_week()
