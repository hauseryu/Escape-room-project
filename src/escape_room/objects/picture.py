from PIL import Image, ImageTk
from tkinter import Toplevel, Label
from riddles.riddle_generator import generate_riddle

class Picture:
    """A picture frame on the back wall (``z = 4``).

    Pass a PNG or JPG path to ``image_path`` and call :meth:`draw` after the
    wall was drawn.  The image is perspective-transformed to match the frame.
    """

    def __init__(self, image_path=None):
        self.image_path = image_path

        self.coordinates_frame = [
            ["#4A2B18", (5.05, 2.35, 3.985), (6.45, 2.35, 3.985),
             (6.45, 0.85, 3.985), (5.05, 0.85, 3.985)],
            ["#C79045", (5.10, 2.30, 3.980), (6.40, 2.30, 3.980),
             (6.40, 0.90, 3.980), (5.10, 0.90, 3.980)],
        ]
        self.coordinates_image = [
            ["#24364B", (5.19, 2.21, 3.975), (6.31, 2.21, 3.975),
             (6.31, 0.99, 3.975), (5.19, 0.99, 3.975)],
        ]
        self.foto_image = None
        self.image_id = None
        self.riddle = generate_riddle()

    def draw_image(self, canvas, tag):
        x1, y1, x2, y2 = canvas.bbox(tag)
        image_width = x2 - x1
        image_heigth = y2 - y1
        image = Image.open(self.image_path)
        image = image.resize((image_width, image_heigth), Image.Resampling.LANCZOS)
        self.foto_image = ImageTk.PhotoImage(image, master=canvas)
        self.image_id = canvas.create_image(x1, y1, anchor="nw", image=self.foto_image)
        canvas.tag_bind(
            self.image_id,
            "<Button-1>",
            lambda e: self.show_riddle(canvas)
        )

    def show_riddle(self, canvas):
        w = canvas.winfo_width()
        h = canvas.winfo_height()

        # Hintergrund abdunkeln
        canvas.create_rectangle(
            0, 0, w, h,
            fill="black",
            stipple="gray50",
            tags="riddle"
        )

        # Pergament (ca. 60 % der Canvas)
        margin_x = w * 0.2
        margin_y = h * 0.15 + 50

        canvas.create_rectangle(
            margin_x,
            margin_y,
            w - margin_x,
            h - margin_y,
            fill="#d8c3a5",
            outline="#7a5230",
            width=4,
            tags="riddle"
        )

        canvas.create_text(
            w / 2,
            h / 2,
            text=self.riddle,
            width=(w - 2 * margin_x - 40),
            font=("Times New Roman", 30),
            justify="left",
            tags="riddle"
        )

        # Schließen-Button
        canvas.create_text(
            w - margin_x - 20,
            margin_y + 20,
            text="✕",
            font=("Arial", 20, "bold"),
            fill="darkred",
            tags="riddle riddle_close"
        )

        canvas.tag_bind(
            "riddle_close",
            "<Button-1>",
            lambda e: canvas.delete("riddle")
        )