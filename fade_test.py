try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk
from PIL import Image, ImageTk
import os

def RGBAImage(path):
    return Image.open(path).convert("RGBA")

class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        app = App(parent=self, controller=self)
        app.grid(row=0, column=0, pady=5, padx=5)

class App(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.alpha = 0.0

        # combine the base image and the border frame using paste
        self.img_pieces = []
        for i in range(2, 5):
            self.img_pieces.append(RGBAImage("media\\piltest%d.png" %(i)))
        self.img_border = RGBAImage("media\\piltest1.png")
        for i in range(3):
            self.img_pieces[i].paste(self.img_border, (0, 0), self.img_border)

        # use ImageTk to create PhotoImage for Tkinter
        self.images = []
        for i in range(3):
            self.images.append(ImageTk.PhotoImage(self.img_pieces[i]))

        # establish example images
        self.examples = []
        for i in range(3):
            self.examples.append(tk.Label(self, image=self.images[i]))
            self.examples[i].image = self.images[i]
            self.examples[i].grid(row=0, column=i, sticky="nsew")

        # create "fading" images example
        self.button = tk.Button(self, image=self.images[0], command=lambda: self.fade())
        self.button.image = self.images[0]
        self.button.grid(row=0, column=3, sticky="nsew")

    def fade(self):
        # stop fading once alpha == 1 (a.k.a. second image)
        if self.alpha > 1.0:
            print("Button now does fade2")
            self.alpha = 0.0
            self.button.config(command=lambda: self.fade2())
        else:
            # create the interpolated image using the current alpha value
            self.new_img = ImageTk.PhotoImage(Image.blend(self.img_pieces[0], self.img_pieces[2], self.alpha))
            self.alpha = self.alpha + 0.1
            print("alpha : %f" % self.alpha)
            # update the image displayed continuously to create the "fade" effect
            self.button.config(image=self.new_img)
            self.after(10, self.fade)

    def fade2(self):
        # stop fading once alpha == 1 (a.k.a. second image)
        if self.alpha > 1.0:
            print("Button now does fade1")
            self.alpha = 0.0
            self.button.config(command=lambda: self.fade())
        else:
            # create the interpolated image using the current alpha value
            self.new_img = ImageTk.PhotoImage(Image.blend(self.img_pieces[2], self.img_pieces[0], self.alpha))
            self.alpha = self.alpha + 0.1
            print("alpha : %d" % self.alpha)
            # update the image displayed continuously to create the "fade" effect
            self.button.config(image=self.new_img)
            self.after(10, self.fade2)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    app = MainApp()
    app.mainloop()
