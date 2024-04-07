from threading import Thread
import pystray
from PIL import Image
import os

print(os.getcwd())

image = Image.open("static/icons/logo.png")

def close(event):
    os._exit(0)

def open():
    print("open")
    os.system("start http://127.0.0.1:8000/")

def init():
    menu = pystray.Menu(
        pystray.MenuItem("Open",open),
        pystray.MenuItem("Close",close),
        )
    icon = pystray.Icon("Chaballon", image, "Chaballon", menu=menu)
    
    Thread(target=icon.run).start()
