# import tkinter
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
# from PIL import Image, ImageTk
# import os
#
# ROOT = os.path.dirname(os.path.realpath(__file__))
# MEDIA = os.path.join(ROOT, 'media')
# COMMON = os.path.join(MEDIA, 'Common')
#
# def RGBAImage(path):
#     return ImageTk.PhotoImage(Image.open(path).convert('RGBA'))
#
# root = tk.Tk()
# root.image = RGBAImage(os.path.join(COMMON, '798Kartana.png'))
# label = tk.Button(root, image=root.image, bg='white', activebackground='white')
# #root.overrideredirect(True)
# #root.geometry("+250+250")
# #root.lift()
# #root.wm_attributes("-topmost", True)
# #root.wm_attributes("-disabled", True)
# root.wm_attributes("-transparentcolor", "white")
# label.pack()
# label.mainloop()
