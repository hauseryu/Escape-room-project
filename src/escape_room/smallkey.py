import tkinter
import os
import graphics
import globals
import winsound  # Integriertes Windows-Modul für Sound

class Key():
    def __init__(self,inventory):
        self.canvas = None
        self.inventory = inventory

    def draw(self,canvas):
        self.canvas = canvas
        # find folder of current python file
        current_dir = os.path.dirname(__file__)
        # connect path to file name
        image_path = os.path.join(current_dir, "key_transparent.png")
        self.img = tkinter.PhotoImage(file=image_path)
        if self.inventory.objectInInventory("key"):
            x1 = 50
            y1 = 100
        else:
            (x1, y1) = graphics.compute_2d_coordinates(6.5, 0.78, 3.0,
                                                    globals.canvas_width, globals.canvas_height)
        # draw key
        self.key_id = canvas.create_image(x1,y1,image=self.img,anchor="nw")
        # bind event to the image
        self.canvas.tag_bind(self.key_id, "<Button-1>", self.on_key_click)

    def on_key_click(self, event):
        self.canvas.delete(self.key_id)
        # play collect sound (i.e. user took the key)
        current_dir = os.path.dirname(__file__)
        sound_path = os.path.join(current_dir, "grab_key.wav")        
        try:
            winsound.PlaySound(
                sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC
            )
        except Exception as e:
            print(f"Sound konnte nicht abgespielt werden: {e}")
        self.inventory.addObject("key")
        self.draw(self.canvas)
