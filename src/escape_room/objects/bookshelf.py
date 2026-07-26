"""Bookshelf object placed where the wardrobe previously stood."""

from escape_room import graphics


class Bookshelf:
    """A filled bookshelf for the left, back corner of the room.

    The measurements deliberately occupy the old wardrobe's space:
    x=0..1.8, y=0..2 and z=3.5..4.
    """

    def __init__(self):
        # Wooden carcass, back panel, three shelf boards and the two side walls.
        self.coordinates_shelf = [
            ["#3B2114", (0, 0, 4), (1.8, 0, 4), (1.8, 2, 4), (0, 2, 4)],
            ["#5B331F", (0, 0, 3.5), (0, 0, 4), (0, 2, 4), (0, 2, 3.5)],
            ["#824D2F", (0, 2, 3.5), (1.8, 2, 3.5), (1.8, 2, 4), (0, 2, 4)],
            ["#6B3C25", (0, 0, 3.5), (1.8, 0, 3.5), (1.8, 0, 4), (0, 0, 4)],
            ["#8C5434", (0, 0.62, 3.49), (1.8, 0.62, 3.49), (1.8, 0.72, 3.49), (0, 0.72, 3.49)],
            ["#8C5434", (0, 1.28, 3.49), (1.8, 1.28, 3.49), (1.8, 1.38, 3.49), (0, 1.38, 3.49)],
            ["#8C5434", (0, 1.92, 3.49), (1.8, 1.92, 3.49), (1.8, 2.00, 3.49), (0, 2.00, 3.49)],
            ["#4B2A1A", (0, 0, 3.48), (0.10, 0, 3.48), (0.10, 2, 3.48), (0, 2, 3.48)],
            ["#4B2A1A", (1.70, 0, 3.48), (1.80, 0, 3.48), (1.80, 2, 3.48), (1.70, 2, 3.48)],
            ["#714128", (1.8, 0, 3.5), (1.8, 0, 4), (1.8, 2, 4), (1.8, 2, 3.5)],
        ]

        # Each entry is one book spine, ordered from left to right on each shelf.
        self.coordinates_books = [
            ["#8F3030", (0.16, 0.72, 3.475), (0.38, 0.72, 3.475), (0.38, 1.23, 3.475), (0.16, 1.23, 3.475)],
            ["#315B86", (0.39, 0.72, 3.475), (0.61, 0.72, 3.475), (0.61, 1.20, 3.475), (0.39, 1.20, 3.475)],
            ["#C18A2A", (0.62, 0.72, 3.475), (0.82, 0.72, 3.475), (0.82, 1.24, 3.475), (0.62, 1.24, 3.475)],
            ["#4E7D45", (0.83, 0.72, 3.475), (1.08, 0.72, 3.475), (1.08, 1.18, 3.475), (0.83, 1.18, 3.475)],
            ["#664070", (1.09, 0.72, 3.475), (1.30, 0.72, 3.475), (1.30, 1.23, 3.475), (1.09, 1.23, 3.475)],
            ["#A45B2A", (1.31, 0.72, 3.475), (1.62, 0.72, 3.475), (1.62, 1.21, 3.475), (1.31, 1.21, 3.475)],
            ["#234E73", (0.16, 1.38, 3.475), (0.40, 1.38, 3.475), (0.40, 1.85, 3.475), (0.16, 1.85, 3.475)],
            ["#8A6330", (0.41, 1.38, 3.475), (0.64, 1.38, 3.475), (0.64, 1.82, 3.475), (0.41, 1.82, 3.475)],
            ["#9B3D4C", (0.65, 1.38, 3.475), (0.87, 1.38, 3.475), (0.87, 1.85, 3.475), (0.65, 1.85, 3.475)],
            ["#386B59", (0.88, 1.38, 3.475), (1.14, 1.38, 3.475), (1.14, 1.80, 3.475), (0.88, 1.80, 3.475)],
            ["#793F29", (1.15, 1.38, 3.475), (1.37, 1.38, 3.475), (1.37, 1.84, 3.475), (1.15, 1.84, 3.475)],
            ["#55516D", (1.38, 1.38, 3.475), (1.62, 1.38, 3.475), (1.62, 1.85, 3.475), (1.38, 1.85, 3.475)],
        ]

        self.books_titles = [
            "Die Tür", "Python", "Sternenpfad", "Das Rätsel", "Nacht", "Schlüssel",
            "Alchemie", "Wolken", "Geheimnis", "Der Turm", "Zeit", "Ausweg",
        ]

    def draw_titles(self, canvas, canvas_width, canvas_height):
        for book, title in zip(self.coordinates_books, self.books_titles):
            x, y, z = self._center(book[1:])
            screen_x, screen_y = graphics.compute_2d_coordinates(
                x, y, z, canvas_width, canvas_height
            )
            # Text is kept compact so it fits on the narrow spines.
            canvas.create_text(
                screen_x, screen_y, text=title, angle=90, fill="#F7E6B5",
                font=("Arial", 7, "bold"), justify="center", width=42,
            )

    @staticmethod
    def _center(points):
        return tuple(sum(point[index] for point in points) / len(points) for index in range(3))
