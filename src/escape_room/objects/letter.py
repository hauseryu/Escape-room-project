class Letter():
    def __init__(self, text = "", shift_coordinates=(0,0,0)):
        self.shift_coordinates = shift_coordinates
        self.text = text
        self.coordinates = [
            ["#F5F2EB", (3.5, 0, 2), (3.7, 0, 2), (3.7, 0, 1.8), (3.5, 0, 1.8)],
            ["#F5F2EB", (3.5, 0, 2), (3.6, 0, 1.86), (3.7, 0, 2)]
        ]
        self.coordinates_stamp = [
            [3.6, 0, 1.86, 0.015, "#B02525", 0, 360]
            ]

    def clicked(self,event,tag,object,canvas,world_coordinates,arc_coordinates):
        print("Letter clicked!")

    