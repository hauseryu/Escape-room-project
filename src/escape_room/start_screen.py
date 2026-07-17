import os
import tkinter

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
            self.image = tkinter.PhotoImage(file=self.image_path)
            self.display_image = self.image.zoom(2, 2)
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
        self.canvas.create_text(
            804,
            284,
            text="ESCAPE ROOM",
            fill="#05070b",
            font=("Georgia", 68, "bold"),
        )
        self.canvas.create_text(
            800,
            280,
            text="ESCAPE ROOM",
            fill="#f1ead7",
            font=("Georgia", 68, "bold"),
        )

    def _draw_start_button(self):
        self.canvas.create_rectangle(
            590,
            795,
            1010,
            890,
            fill="#171a20",
            outline="#d6c28a",
            width=4,
            tags=("start_button",),
        )
        self.canvas.create_text(
            800,
            842,
            text="START GAME",
            fill="#090a0d",
            font=("Arial", 31, "bold"),
            tags=("start_button",),
        )
        self.canvas.create_text(
            800,
            838,
            text="START GAME",
            fill="#f3e8c4",
            font=("Arial", 31, "bold"),
            tags=("start_button",),
        )
