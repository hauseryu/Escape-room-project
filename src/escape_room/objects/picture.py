from PIL import Image, ImageTk

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

    def draw_image(self, canvas, tag):
        x1, y1, x2, y2 = canvas.bbox(tag)
        image_width = x2 - x1
        image_heigth = y2 - y1
        image = Image.open(self.image_path)
        image = image.resize((image_width, image_heigth), Image.Resampling.LANCZOS)
        self.foto_image = ImageTk.PhotoImage(image, master=canvas)
        canvas.create_image(x1, y1, anchor="nw", image=self.foto_image)
        