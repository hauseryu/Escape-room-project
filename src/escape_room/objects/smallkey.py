import os
import tkinter
import winsound

from escape_room import globals
from escape_room import graphics


class Key:
    def __init__(self, inventory):
        self.canvas = None
        self.inventory = inventory
        package_dir = os.path.dirname(os.path.dirname(__file__))
        self.image_path = os.path.join(package_dir, "assets", "images", "key_transparent.png")
        self.sound_path = os.path.join(package_dir, "assets", "sounds", "grab_key.wav")

    def draw(self, canvas):
        self.canvas = canvas
        self.img = tkinter.PhotoImage(file=self.image_path)
        if self.inventory.objectInInventory("key"):
            x1 = 28
            y1 = 80
        else:
            (x1, y1) = graphics.compute_2d_coordinates(
                6.5,
                0.78,
                3.0,
                globals.canvas_width,
                globals.canvas_height,
            )
        self.key_id = canvas.create_image(x1, y1, image=self.img, anchor="nw")
        self.canvas.tag_bind(self.key_id, "<Button-1>", self.on_key_click)

    def on_key_click(self, event):
        self.canvas.delete(self.key_id)
        try:
            winsound.PlaySound(
                self.sound_path,
                winsound.SND_FILENAME | winsound.SND_ASYNC,
            )
        except Exception as e:
            print(f"Sound konnte nicht abgespielt werden: {e}")
        self.inventory.addObject("key")
        self.draw(self.canvas)
