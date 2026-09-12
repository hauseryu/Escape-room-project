import os
import tkinter
from PIL import Image, ImageTk
from pathlib import Path

from src.escape_room.application import globals
from src.escape_room.gui_utilities import icon_picker_popup
from src.escape_room.application.context_manager import ContextManager

class GameOverScreen:
    def __init__(self, canvas, start_callback, server):
        self.canvas = canvas
        self.start_callback = start_callback
        self.image_path = ContextManager.get_image_path()
        self.image_path_start_screen = self.image_path.joinpath("game_over_screen.jpg")
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
        self._draw_return_button()
        escape_app = ContextManager().get_escape_app()
        self.canvas.tag_bind("return_button", "<Button-1>", escape_app.return_to_start_screen)
        print(f"[DEBUG] children in StartScreen frame: {self.canvas.winfo_children()}")

    def _draw_bitmap(self):
        try:
            imagePil = Image.open(self.image_path_start_screen)
            imagePilResized = imagePil.resize((globals.canvas_width,globals.canvas_height),Image.LANCZOS)
            self.image = ImageTk.PhotoImage(imagePilResized)
            self.display_image = self.image
            self.canvas.create_image(
                0,
                0,
                image=self.display_image,
                anchor="nw",
            )
            
            if not hasattr(self.canvas, '_images'):
                self.canvas._images = []
            
            # Wir fügen das Foto der Liste hinzu, damit der Garbage Collector es NIEMALS löscht
            self.canvas._images.append(self.image)
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

    def _draw_return_button(self):
        center_x = globals.canvas_width / 2
        button_half_width = 350
        self.canvas.create_rectangle(
            center_x - button_half_width,
            980,
            center_x + button_half_width,
            1070,
            fill="#000000",
            outline="#ffffff",
            width=4,
            tags=("return_button",),
        )
        self.canvas.create_text(
            center_x + 3,
            1022 + 3,
            text="Return to Start Screen",
            fill="#db2929",
            font=("Courier New", 31, "bold"),
            tags=("return_button",),
        )
        self.canvas.create_text(
            center_x,
            1022,
            text="Return to Start Screen",
            fill="#ffffff",
            font=("Courier New", 31, "bold"),
            tags=("return_button",),
        )
