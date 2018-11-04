from PIL import Image, ImageTk

def RGBAImage(path):
    return Image.open(path).convert("RGBA")
