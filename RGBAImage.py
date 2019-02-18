from PIL import Image, ImageTk

def RGBAImage(path):
    return ImageTk.PhotoImage(Image.open(path).convert("RGBA"))

def RGBAImage2(path):
    return Image.open(path).convert("RGBA")
