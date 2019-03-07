# import tkinter # Tkinter -> tkinter in Python 3
#
# class FancyListbox(tkinter.Listbox):
#
#     def __init__(self, parent, *args, **kwargs):
#         tkinter.Listbox.__init__(self, parent, *args, **kwargs)
#
#         self.popup_menu = tkinter.Menu(self, tearoff=0)
#         self.popup_menu.add_command(label="Delete",
#                                     command=self.delete_selected)
#         self.popup_menu.add_command(label="Select All",
#                                     command=self.select_all)
#
#         self.bind("<Button-3>", self.popup) # Button-2 on Aqua
#
#     def popup(self, event):
#         try:
#             self.popup_menu.tk_popup(event.x_root, event.y_root, 0)
#         finally:
#             self.popup_menu.grab_release()
#
#     def delete_selected(self):
#         for i in self.curselection()[::-1]:
#             self.delete(i)
#
#     def select_all(self):
#         self.selection_set(0, 'end')
#
#
# root = tkinter.Tk()
# flb = FancyListbox(root, selectmode='multiple')
# for n in range(10):
#     flb.insert('end', n)
# flb.pack()
# root.mainloop()

# import tkinter as tk
# from tkinter import ttk
#
# root = tk.Tk()
#
# mytext = tk.StringVar(value='test ' * 30)
#
# myframe = ttk.Frame(root)
# myentry = ttk.Entry(myframe, textvariable=mytext, state='readonly')
# myscroll = ttk.Scrollbar(myframe, orient='horizontal', command=myentry.xview)
# myentry.config(xscrollcommand=myscroll.set)
#
# myframe.grid()
# myentry.grid(row=1, sticky='ew')
# myscroll.grid(row=2, sticky='ew')
#
# root.mainloop()

i = 0
while True:
    if i == 10:
        print(i)
        break
    i += 1
