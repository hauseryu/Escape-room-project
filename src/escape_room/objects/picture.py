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
        

    # def draw(self, canvas):
    #     """Draw the frame and, when available, its PNG/JPG image on *canvas*."""
    #     self._draw_polygon(canvas, self.coordinates_frame[0])
    #     self._draw_polygon(canvas, self.coordinates_frame[1])

    #     if self.image_path and self.image_path.is_file():
    #         self._draw_image(canvas)
    #     else:
    #         # A coloured inset makes the picture visible before an image is set.
    #         self._draw_polygon(canvas, self.coordinates_image[0])

    # def _draw_polygon(self, canvas, polygon):
    #     points = self._project_points(polygon[1:])
    #     canvas.create_polygon(*self._flatten(points), fill=polygon[0], outline="black")

    # def _draw_image(self, canvas):
    #     destination = self._project_points(self.coordinates_image[0][1:])
    #     min_x = int(min(x for x, _ in destination))
    #     min_y = int(min(y for _, y in destination))
    #     max_x = int(max(x for x, _ in destination))
    #     max_y = int(max(y for _, y in destination))
    #     width, height = max_x - min_x + 1, max_y - min_y + 1

    #     with Image.open(self.image_path) as opened_image:
    #         source = opened_image.convert("RGBA")

    #     # Pillow's perspective coefficients map output pixels back to the
    #     # source image. The transparent parts keep the image inside its quad.
    #     local_quad = [(x - min_x, y - min_y) for x, y in destination]
    #     coefficients = self._perspective_coefficients(
    #         local_quad,
    #         [(0, 0), (source.width, 0), (source.width, source.height), (0, source.height)],
    #     )
    #     transformed = source.transform(
    #         (width, height), Image.Transform.PERSPECTIVE, coefficients,
    #         resample=Image.Resampling.BICUBIC,
    #     )
    #     photo = ImageTk.PhotoImage(transformed, master=canvas)
    #     canvas.create_image(min_x, min_y, anchor="nw", image=photo)
    #     # Tkinter otherwise garbage-collects PhotoImage objects immediately.
    #     if not hasattr(canvas, "_picture_images"):
    #         canvas._picture_images = []
    #     canvas._picture_images.append(photo)

    # def _project_points(self, points):
    #     return [compute_2d_coordinates(x, y, z, globals.canvas_width, globals.canvas_height)
    #             for x, y, z in points]

    # @staticmethod
    # def _flatten(points):
    #     return [value for point in points for value in point]

    # @staticmethod
    # def _perspective_coefficients(destination, source):
    #     """Return the eight coefficients for a destination-to-source mapping."""
    #     matrix = []
    #     values = []
    #     for (x, y), (u, v) in zip(destination, source):
    #         matrix.extend(([x, y, 1, 0, 0, 0, -u * x, -u * y],
    #                        [0, 0, 0, x, y, 1, -v * x, -v * y]))
    #         values.extend((u, v))

    #     # Gaussian elimination keeps this class independent from NumPy.
    #     for column in range(8):
    #         pivot = max(range(column, 8), key=lambda row: abs(matrix[row][column]))
    #         matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
    #         values[column], values[pivot] = values[pivot], values[column]
    #         divisor = matrix[column][column]
    #         for index in range(column, 8):
    #             matrix[column][index] /= divisor
    #         values[column] /= divisor
    #         for row in range(8):
    #             if row == column:
    #                 continue
    #             factor = matrix[row][column]
    #             for index in range(column, 8):
    #                 matrix[row][index] -= factor * matrix[column][index]
    #             values[row] -= factor * values[column]
    #     return values
