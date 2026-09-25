from src.escape_room.gui_utilities import graphics

class HotelDoor():
    def __init__(self, room_data, index, room_state):

        # evaluate room data
        (x,y,z) = room_data["hotel_door"][index][0] # get hotel door coordinates (first element in list)
        self.index = index
        self.room_data = room_data
        self.state = 0 # 0=shut, 1=open
        shift_coordinates = (x-2.75,y-0,z-4)
        unique_id = room_data["hotel_door"][index][1]

        # set attributes
        self.shift_coordinates = shift_coordinates

        self.hotel_door_coordinates = [
            # === HAUPTRAHMEN (AUSSEN) ===
            ["#4A3429", (2.75, 0.00, 4.00), (5.25, 0.00, 4.00), (5.25, 2.60, 4.00), (2.75, 2.60, 4.00)], # Outer wooden frame

            # === LINKE TÜRFLÜGEL ===
            ["#5A4032", (2.85, 0.05, 3.98), (3.98, 0.05, 3.98), (3.98, 2.50, 3.98), (2.85, 2.50, 3.98)], # Left door wing (wood)
            ["#141F1F", (3.05, 0.30, 3.96), (3.78, 0.30, 3.96), (3.78, 2.25, 3.96), (3.05, 2.25, 3.96)], # Left door glass insert (dark)

            # === RECHTER TÜRFLÜGEL ===
            ["#4C382E", (4.02, 0.05, 3.98), (5.15, 0.05, 3.98), (5.15, 2.50, 3.98), (4.02, 2.50, 3.98)], # Right door wing (wood)
            ["#141F1F", (4.22, 0.30, 3.96), (4.95, 0.30, 3.96), (4.95, 2.25, 3.96), (4.22, 2.25, 3.96)], # Right door glass insert (dark)

            # === TÜRGRIFFE (MESSING / GOLD) ===
            ["#C5A059", (3.86, 0.70, 3.92), (3.90, 0.70, 3.92), (3.90, 1.60, 3.92), (3.86, 1.60, 3.92)], # Left vertical handle bar
            ["#A88448", (3.84, 1.60, 3.93), (3.92, 1.60, 3.93), (3.92, 1.65, 3.93), (3.84, 1.65, 3.93)], # Left handle top mount
            ["#A88448", (3.84, 0.65, 3.93), (3.92, 0.65, 3.93), (3.92, 0.70, 3.93), (3.84, 0.70, 3.93)], # Left handle bottom mount

            ["#C5A059", (4.10, 0.70, 3.92), (4.14, 0.70, 3.92), (4.14, 1.60, 3.92), (4.10, 1.60, 3.92)], # Right vertical handle bar
            ["#A88448", (4.08, 1.60, 3.93), (4.16, 1.60, 3.93), (4.16, 1.65, 3.93), (4.08, 1.65, 3.93)], # Right handle top mount
            ["#A88448", (4.08, 0.65, 3.93), (4.16, 0.65, 3.93), (4.16, 0.70, 3.93), (4.08, 0.70, 3.93)], # Right handle bottom mount

            # === HINTERGRUND-OBJEKTE (Hinter dem Glas, z = 4.30) ===
            ["#D3CBC4", (3.10, 0.30, 4.30), (3.45, 0.30, 4.30), (3.45, 0.55, 4.30), (3.10, 0.55, 4.30)], # Left plant pot (white)
            ["#192D1F", (3.05, 0.55, 4.28), (3.50, 0.55, 4.28), (3.50, 1.50, 4.28), (3.05, 1.50, 4.28)], # Left plant/shrub (dark green)

            ["#D3CBC4", (4.55, 0.30, 4.30), (4.90, 0.30, 4.30), (4.90, 0.55, 4.30), (4.55, 0.55, 4.30)], # Right plant pot (white)
            ["#192D1F", (4.50, 0.55, 4.28), (4.95, 0.55, 4.28), (4.95, 1.50, 4.28), (4.50, 1.50, 4.28)], # Right plant/shrub (dark green)
        ]

        self.hotel_door_open_70_coordinates = [
            # === HAUPTRAHMEN (Bleibt unverändert im Hintergrund) ===
            ["#4A3429", (2.75, 0.00, 4.00), (5.25, 0.00, 4.00), (5.25, 2.60, 4.00), (2.75, 2.60, 4.00)], # Outer wooden frame

            # === HINTERGRUND-OBJEKTE (Pflanzen bleiben unverändert hinten) ===
            # ["#D3CBC4", (3.10, 0.30, 4.30), (3.45, 0.30, 4.30), (3.45, 0.55, 4.30), (3.10, 0.55, 4.30)], # Left plant pot
            # ["#192D1F", (3.05, 0.55, 4.28), (3.50, 0.55, 4.28), (3.50, 1.50, 4.28), (3.05, 1.50, 4.28)], # Left plant
            # ["#D3CBC4", (4.55, 0.30, 4.30), (4.90, 0.30, 4.30), (4.90, 0.55, 4.30), (4.55, 0.55, 4.30)], # Right plant pot
            # ["#192D1F", (4.50, 0.55, 4.28), (4.95, 0.55, 4.28), (4.95, 1.50, 4.28), (4.50, 1.50, 4.28)], # Right plant
            ["#000000", (2.85, 0.05, 4.10), (5.15, 0.05, 4.10), (5.15, 2.50, 4.10), (2.85, 2.50, 4.10)], # Black interior background
            # ==================== 70° GEÖFFNETE TÜRFLÜGEL ====================

            # === LINKE TÜRFLÜGEL (Dreht sich an Angel X=2.85, Z=3.98 in den Raum) ===
            ["#5A4032", (2.85, 0.05, 3.98), (3.24, 0.05, 2.92), (3.24, 2.50, 2.92), (2.85, 2.50, 3.98)], # Left door wing (wood)
            ["#141F1F", (2.92, 0.30, 3.80), (3.17, 0.30, 3.11), (3.17, 2.25, 3.11), (2.92, 2.25, 3.80)], # Left door glass

            # GRIFF LINKS (Sitzt an der schrägen Innenkante des Flügels bei X=3.24, Z=2.92)
            ["#C5A059", (3.20, 0.70, 2.95), (3.22, 0.70, 2.90), (3.22, 1.60, 2.90), (3.20, 1.60, 2.95)], # Left vertical handle bar
            ["#A88448", (3.19, 1.60, 2.97), (3.23, 1.65, 2.97), (3.23, 1.65, 2.89), (3.19, 1.60, 2.89)], # Left handle top mount
            ["#A88448", (3.19, 0.65, 2.97), (3.23, 0.70, 2.97), (3.23, 0.70, 2.89), (3.19, 0.65, 2.89)], # Left handle bottom mount


            # === RECHTER TÜRFLÜGEL (Dreht sich an Angel X=5.15, Z=3.98 in den Raum) ===
            ["#4C382E", (5.15, 0.05, 3.98), (4.76, 0.05, 2.92), (4.76, 2.50, 2.92), (5.15, 2.50, 3.98)], # Right door wing (wood)
            ["#141F1F", (5.08, 0.30, 3.80), (4.83, 0.30, 3.11), (4.83, 2.25, 3.11), (5.08, 2.25, 3.80)], # Right door glass

            # GRIFF RECHTS (Sitzt an der schrägen Innenkante des Flügels bei X=4.76, Z=2.92)
            ["#C5A059", (4.80, 0.70, 2.95), (4.78, 0.70, 2.90), (4.78, 1.60, 2.90), (4.80, 1.60, 2.95)], # Right vertical handle bar
            ["#A88448", (4.81, 1.60, 2.97), (4.77, 1.65, 2.97), (4.77, 1.65, 2.89), (4.81, 1.60, 2.89)], # Right handle top mount
            ["#A88448", (4.81, 0.65, 2.97), (4.77, 0.70, 2.97), (4.77, 0.70, 2.89), (4.81, 0.65, 2.89)], # Right handle bottom mount
        ]

    def draw(self, canvas):
        # draw outline
        if self.state==0:
            graphics.draw(canvas,self.hotel_door_coordinates,shift_coordinates=self.shift_coordinates)
        elif self.state==1:
            graphics.draw(canvas,self.hotel_door_open_70_coordinates,shift_coordinates=self.shift_coordinates)