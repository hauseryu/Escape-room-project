import os
import tkinter
from PIL import Image, ImageTk

from escape_room import globals


class StartScreen:
    def __init__(self, canvas, start_callback):
        self.canvas = canvas
        self.start_callback = start_callback
        self.image_path = os.path.join(
            os.path.dirname(__file__),
            "assets",
            "images",
            "start_screen_moon.png",
        )
        self.image = None
        self.display_image = None

    def draw(self):
        self.canvas.delete("all")
        self.canvas.create_rectangle(
            0,
            0,
            globals.canvas_width,
            globals.canvas_height,
            fill="#07111f",
            outline="",
        )
        self._draw_bitmap()
        self._draw_title()
        self._draw_start_button()
        self.canvas.tag_bind("start_button", "<Button-1>", self.start_callback)

    def _draw_bitmap(self):
        try:
            imagePil = Image.open(self.image_path)
            imagePilResized = imagePil.resize((globals.canvas_width,globals.canvas_height),Image.LANCZOS)
            self.image = ImageTk.PhotoImage(imagePilResized)
            # self.image = tkinter.PhotoImage(file=self.image_path)
            # self.display_image = self.image.zoom(1, 1)
            self.display_image = self.image
            self.canvas.create_image(
                0,
                0,
                image=self.display_image,
                anchor="nw",
            )
        except (RuntimeError, tkinter.TclError):
            self.canvas.create_rectangle(
                180,
                140,
                1420,
                940,
                fill="#14213a",
                outline="#44516a",
                width=3,
            )

    def _draw_title(self):
        center_x = globals.canvas_width / 2
        self.canvas.create_text(
            center_x + 4,
            284,
            text="ESCAPE ROOM",
            fill="#05070b",
            font=("Georgia", 68, "bold"),
        )
        self.canvas.create_text(
            center_x,
            280,
            text="ESCAPE ROOM",
            fill="#f1ead7",
            font=("Georgia", 68, "bold"),
        )

    def _draw_start_button(self):
        center_x = globals.canvas_width / 2
        button_half_width = 210
        self.canvas.create_rectangle(
            center_x - button_half_width,
            795,
            center_x + button_half_width,
            890,
            fill="#171a20",
            outline="#d6c28a",
            width=4,
            tags=("start_button",),
        )
        self.canvas.create_text(
            center_x,
            842,
            text="START GAME",
            fill="#090a0d",
            font=("Arial", 31, "bold"),
            tags=("start_button",),
        )
        self.canvas.create_text(
            center_x,
            838,
            text="START GAME",
            fill="#f3e8c4",
            font=("Arial", 31, "bold"),
            tags=("start_button",),
        )
