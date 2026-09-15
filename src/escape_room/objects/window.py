from PIL import Image, ImageTk, ImageOps, ImageDraw
import numpy as np
from src.escape_room.application.context_manager import ContextManager

class Window():
    def __init__(self, shift_coordinates=(0, 0, 0)):
        self.shift_coordinates = shift_coordinates
        self.sky_coordinates = [(0, 1.0, 2.5), (0, 1.0, 3.7), (0, 2.5, 3.7), (0, 2.5, 2.5)]
        self.window_coordinates = [
            # Himmel
            #["#6DB7E8", (0, 1.0, 2.5), (0, 1.0, 3.7), (0, 2.5, 3.7), (0, 2.5, 2.5)],

            # linker Rahmen
            ["#4A2A1A", (0, 1.0, 2.5), (0, 1.0, 2.62), (0, 2.5, 2.62), (0, 2.5, 2.5)],

            # rechter Rahmen
            ["#4A2A1A", (0, 1.0, 3.58), (0, 1.0, 3.7), (0, 2.5, 3.7), (0, 2.5, 3.58)],

            # unterer Rahmen
            ["#59331F", (0, 1.0, 2.5), (0, 1.12, 2.5), (0, 1.12, 3.7), (0, 1.0, 3.7)],

            # oberer Rahmen
            ["#59331F", (0, 2.38, 2.5), (0, 2.5, 2.5), (0, 2.5, 3.7), (0, 2.38, 3.7)],

            # linke vertikale Fenster-Sprosse
            ["#6B3E26", (0, 1.12, 2.95), (0, 1.12, 3.01), (0, 2.38, 3.01), (0, 2.38, 2.95)],

            # rechte vertikale Fenster-Sprosse
            ["#6B3E26", (0, 1.12, 3.19), (0, 1.12, 3.25), (0, 2.38, 3.25), (0, 2.38, 3.19)],

            # horizontale Fenster-Sprosse
            ["#6B3E26", (0, 1.68, 2.62), (0, 1.68, 3.58), (0, 1.75, 3.58), (0, 1.75, 2.62)],

            # untere Fensterbank
            ["#704229", (0, 0.90, 2.42), (0, 0.90, 3.78), (0, 1.0, 3.78), (0, 1.0, 2.42)]
        ]

    def draw_sky(self, canvas, window_corners):
        # Load the sky image
        sky_image_path = ContextManager.get_image_path().joinpath("blue_sky.jpg")

        sky_image = Image.open(sky_image_path).convert("RGB")
        sky, x, y = self.image_to_quad(sky_image, window_corners)

        # Maske erstellen
        mask = Image.new("L", sky.size, 0)

        draw = ImageDraw.Draw(mask)

        mask_corners = [
            (window_corners[0][0] - x, window_corners[0][1] - y),
            (window_corners[1][0] - x, window_corners[1][1] - y),
            (window_corners[2][0] - x, window_corners[2][1] - y),
            (window_corners[3][0] - x, window_corners[3][1] - y)
        ]

        draw.polygon(mask_corners, fill=255)

        # Transparentes Bild erzeugen
        sky_rgba = Image.new("RGBA", sky.size, (0, 0, 0, 0))

        sky_rgba.paste(
            sky,
            (0, 0),
            mask
        )

        # Tkinter
        self.sky_image = ImageTk.PhotoImage(sky_rgba)

        canvas.create_image(
            x,
            y,
            image=self.sky_image,
            anchor="nw"
        )

    def image_to_quad(self, image, corners):
        """
        corners:
            [(x1,y1), (x2,y2), (x3,y3), (x4,y4)]
            im Uhrzeigersinn:
            oben links, oben rechts, unten rechts, unten links
        """

        # Größe des Zielbildes bestimmen
        xs = [p[0] for p in corners]
        ys = [p[1] for p in corners]

        min_x = int(min(xs))
        max_x = int(max(xs))
        min_y = int(min(ys))
        max_y = int(max(ys))

        width = max_x - min_x
        height = max_y - min_y

        # Zielpunkte relativ zur Bounding-Box
        dst = np.array([
            [corners[0][0] - min_x, corners[0][1] - min_y],
            [corners[1][0] - min_x, corners[1][1] - min_y],
            [corners[2][0] - min_x, corners[2][1] - min_y],
            [corners[3][0] - min_x, corners[3][1] - min_y]
        ], dtype=np.float32)

        # Quellpunkte des Bildes
        src = np.array([
            [0, 0],
            [image.width, 0],
            [image.width, image.height],
            [0, image.height]
        ], dtype=np.float32)

        # Homographie berechnen
        A = []

        for (x, y), (u, v) in zip(src, dst):
            A.append([-x, -y, -1, 0, 0, 0, x*u, y*u, u])
            A.append([0, 0, 0, -x, -y, -1, x*v, y*v, v])

        A = np.array(A)

        _, _, V = np.linalg.svd(A)

        H = V[-1].reshape(3, 3)
        H /= H[2, 2]

        # Pillow benötigt die inverse Transformation
        H_inv = np.linalg.inv(H)

        coeffs = H_inv.flatten()[:8]

        # Bild transformieren
        transformed = image.transform(
            (width, height),
            Image.Transform.PERSPECTIVE,
            coeffs,
            resample=Image.Resampling.BICUBIC
        )

        return transformed, min_x, min_y
