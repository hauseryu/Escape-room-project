class Table():
    def __init__(self):
        self.coordinates_tabletop = [
            ["#5A3518",
             (7.55, 0.67, 3.75),
             (5.55, 0.67, 3.75),
             (5.55, 0.78, 3.75),
             (7.55, 0.78, 3.75)],
            ["#6F4520",
             (5.55, 0.67, 3.75),
             (5.55, 0.67, 2.0),
             (5.55, 0.78, 2.0),
             (5.55, 0.78, 3.75)],
            ["#6F4520",
             (7.55, 0.67, 2.0),
             (7.55, 0.67, 3.75),
             (7.55, 0.78, 3.75),
             (7.55, 0.78, 2.0)],
            ["#8B5A2B",
             (5.55, 0.78, 2.0),
             (7.55, 0.78, 2.0),
             (7.55, 0.78, 3.75),
             (5.55, 0.78, 3.75)],
            ["#7A4A22",
             (5.55, 0.67, 2.0),
             (7.55, 0.67, 2.0),
             (7.55, 0.78, 2.0),
             (5.55, 0.78, 2.0)],
        ]

        self.coordinates_tablelegs = [
            *self._create_leg_coordinates(5.72, 3.52),
            *self._create_leg_coordinates(7.20, 3.52),
            *self._create_leg_coordinates(5.72, 2.15),
            *self._create_leg_coordinates(7.20, 2.15),
        ]

        self.coordinates_table = self.coordinates_tablelegs + self.coordinates_tabletop

    def _create_leg_coordinates(self, x, z):
        width = 0.16
        x2 = x + width
        z2 = z + width

        return [
            ["#4A2C14",
             (x2, 0, z2),
             (x, 0, z2),
             (x, 0.67, z2),
             (x2, 0.67, z2)],
            ["#6F4520",
             (x, 0, z2),
             (x, 0, z),
             (x, 0.67, z),
             (x, 0.67, z2)],
            ["#6F4520",
             (x2, 0, z),
             (x2, 0, z2),
             (x2, 0.67, z2),
             (x2, 0.67, z)],
            ["#7A4A22",
             (x, 0, z),
             (x2, 0, z),
             (x2, 0.67, z),
             (x, 0.67, z)],
        ]
