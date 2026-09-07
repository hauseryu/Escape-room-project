from src.escape_room.gui_utilities import graphics

class Sofa():
    def __init__(self,direction,shift_coordinates=(0,0,0),unique_id=None):
        self.shift_coordinates = shift_coordinates
        self.unique_id = unique_id
        self.state = 0 # 0 = closed, 1 = open

        base_sofa = 4
      
# Biedermeier-Sofa (Blau gestreift, Holzrahmen, Seitenansicht nach rechts geöffnet)
# Format: [Farbe, (X1, Y1, Z1), (X2, Y2, Z2), (X3, Y3, Z3), (X4, Y4, Z4)]

# Holzfarben: #5A3825 (Nussbaum dunkel), #8B5A2B (Mittelbraun)
# Blautöne: #2B4C7E (Dunkelblau), #4A75A0 (Hellblau für Streifen)

        # 1. Die markante, geschwungene Biedermeier-Rückenlehne (X = 0)
        # Durch den leichten Versatz bei Y simulieren wir die typische Biedermeier-Wölbung
        backrest_rotated = [
            ["#5A3825", (0.0, 0.4, 4.0), (0.0, 0.4, 2.5), (0.0, 0.90, 2.5), (0.0, 0.85, 4.0)], # Holz-Rückwand ganz außen
            ["#8B5A2B", (0.4, 0.85, 4.0), (0.4, 0.90, 2.5), (0.0, 0.90, 2.5), (0.0, 0.85, 4.0)], # Geschwungene Oberkante (Holz)
        ]

        # 2. Die Sitzfläche & das Biedermeier-Streifenmuster
        # Wir zeichnen die Grundfläche blau und setzen schmalere Polygone als Streifen darauf ab
        seating_rotated = [
            ["#2B4C7E", (0.4, 0.4, 4.0), (0.4, 0.4, 2.5), (0.0, 0.4, 2.5), (0.0, 0.4, 4.0)], # Blaue Sitz-Basis oben
            ["#5A3825", (0.4, 0.1, 4.0), (0.4, 0.1, 2.5), (0.4, 0.4, 2.5), (0.4, 0.4, 4.0)], # Holz-Zarge unter der Sitzfläche
            
            # Vertikale Streifen-Polygone auf der Sitzfläche (Z-Achse entlang gerichtet)
            ["#4A75A0", (0.39, 0.405, 3.85), (0.39, 0.405, 3.65), (0.01, 0.405, 3.65), (0.01, 0.405, 3.85)], # Streifen 1
            ["#4A75A0", (0.39, 0.405, 3.45), (0.39, 0.405, 3.25), (0.01, 0.405, 3.25), (0.01, 0.405, 3.45)], # Streifen 2
            ["#4A75A0", (0.39, 0.405, 3.05), (0.39, 0.405, 2.85), (0.01, 0.405, 2.85), (0.01, 0.405, 3.05)], # Streifen 3
        ]

        # 3. Die grazilen, geschwungenen Armlehnen (inklusive der eleganten Beine)
        armrest_back = [
            ["#2B4C7E", (0.4, 0.1, 4.0), (0.4, 0.6, 4.0), (0.0, 0.6, 4.0), (0.0, 0.1, 4.0)], # Blaues Innenpolster hinten
            ["#8B5A2B", (0.4, 0.6, 4.0), (0.4, 0.6, 3.8), (0.0, 0.6, 3.8), (0.0, 0.6, 4.0)], # Holz-Armauflage hinten
            ["#5A3825", (0.4, -0.3, 4.0), (0.4, 0.1, 4.0), (0.3, 0.1, 4.0), (0.3, -0.3, 4.0)] # Geschwungenes Holzbein hinten unten
        ]

        armrest_front = [
            ["#2B4C7E", (0.4, 0.1, 2.5), (0.4, 0.6, 2.5), (0.0, 0.6, 2.5), (0.0, 0.1, 2.5)], # Blaues Innenpolster vorn
            ["#8B5A2B", (0.4, 0.6, 2.5), (0.4, 0.6, 2.7), (0.0, 0.6, 2.7), (0.0, 0.6, 2.5)], # Holz-Armauflage vorn
            ["#5A3825", (0.4, -0.3, 2.5), (0.4, 0.1, 2.5), (0.3, 0.1, 2.5), (0.3, -0.3, 2.5)] # Geschwungenes Holzbein vorn unten (Z=2.5)
        ]

        if direction == "left":
            self.sofa_coordinates = armrest_back + backrest_rotated + seating_rotated + armrest_front
        elif direction == "right":
            self.sofa_coordinates = armrest_front + backrest_rotated + seating_rotated + armrest_back

