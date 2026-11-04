from numpy.strings import index

from src.escape_room.gui_utilities import graphics
from src.escape_room.application.context_manager import ContextManager
from src.escape_room.gui_utilities.confirmation_popup import ConfirmationPopup
import math

# Room dimensions:
# x = width:  0 to 2 m
# y = height: 0 to 3 m
# z = depth:  0 to 2 m
# Vanishing point: x = 1

def quad_x(x, y1, z1, y2, z2, color):
    # Create a rectangle on a plane with constant x
    return [
        color,
        (x, y1, z1),
        (x, y1, z2),
        (x, y2, z2),
        (x, y2, z1),
    ]

def quad_z(z, x1, y1, x2, y2, color):
    # Create a rectangle on a plane with constant z
    return [
        color,
        (x1, y1, z),
        (x2, y1, z),
        (x2, y2, z),
        (x1, y2, z),
    ]

class Lift():
    def __init__(self, room_data, index, room_state, next_room_callback=None):
        coord = room_data["lift"][index][0] # get lift coordinates (first element in list)
        shift_coord = (coord[0]-0.02,coord[1]-0.10,coord[2]-0.30)        
        self.shift_coordinates = shift_coord
        self.room_state = room_state
        self.set_floor(0) # default floor is 0 (ground floor)
        self.unique_id = room_data["lift"][index][1]
        self.state = "closed" # default state is closed
        self.next_room_callback = next_room_callback
        ContextManager().set_lift(self)
        ind = 2 # start index to read from room_data
        self.floor_room = []
        try:
            while True:
                floor = room_data["lift"][index][ind] # get floor to exit
                next_room = room_data["lift"][index][ind+1] # get next room to go to
                self.floor_room.append((floor, next_room))
                ind+=2
        except IndexError:
            pass

# ============================================================
# 1. Left elevator gate
# Plane x = 0; gate extends along the z-axis
# ============================================================

        self.elevator_gate_coordinates = [
            # Dark background panel, extending all the way to the floor
            quad_x(0.02, 0.00, 0.15, 2.40, 1.40, "#211B17"),

            # Outer gate frame
            quad_x(0.00, 0.00, 0.15, 2.40, 0.22, "#302D2A"),
            quad_x(0.00, 0.00, 1.33, 2.40, 1.40, "#302D2A"),

            # Bottom and top frame sections
            quad_x(-0.01, 0.00, 0.22, 0.10, 1.33, "#76583D"),
            quad_x(-0.01, 2.30, 0.22, 2.40, 1.33, "#96704A"),

            # Vertical grille bars
            quad_x(-0.02, 0.10, 0.32, 2.30, 0.36, "#96704A"),
            quad_x(-0.02, 0.10, 0.56, 2.30, 0.60, "#96704A"),
            quad_x(-0.02, 0.10, 0.80, 2.30, 0.84, "#96704A"),
            quad_x(-0.02, 0.10, 1.04, 2.30, 1.08, "#96704A"),
            quad_x(-0.02, 0.10, 1.25, 2.30, 1.29, "#96704A"),

            # Horizontal grille bars
            quad_x(-0.03, 0.45, 0.22, 0.51, 1.33, "#B18A59"),
            quad_x(-0.03, 0.95, 0.22, 1.01, 1.33, "#B18A59"),
            quad_x(-0.03, 1.45, 0.22, 1.51, 1.33, "#B18A59"),
            quad_x(-0.03, 1.95, 0.22, 2.01, 1.33, "#B18A59"),

            # Central decorative plate
            quad_x(-0.04, 1.30, 0.70, 1.55, 0.95, "#C09A63"),
        ]

# ============================================================
# 2. Right side wall
# Plane x = 8
# ============================================================

        self.elevator_right_wall_coordinates = [
            # Main wall surface
            quad_x(2.00, 0.00, 0.00, 3.00, 2.00, "#38251B"),

            # Bottom baseboard
            quad_x(1.98, 0.10, 0.00, 0.30, 2.00, "#76583D"),

            # Upper decorative cornice
            quad_x(1.98, 2.80, 0.00, 2.95, 2.00, "#96704A"),

            # Wooden wall panels
            quad_x(1.97, 0.40, 0.12, 2.60, 0.55, "#593820"),
            quad_x(1.97, 0.40, 0.62, 2.60, 1.05, "#493020"),
            quad_x(1.97, 0.40, 1.12, 2.60, 1.88, "#593820"),

            # Decorative horizontal trim
            quad_x(1.95, 0.40, 0.15, 2.60, 0.19, "#96704A"),
            quad_x(1.95, 0.40, 1.82, 2.60, 1.86, "#96704A"),

            # Brass handrail
            quad_x(1.94, 1.20, 0.10, 1.30, 1.90, "#B18A40"),
        ]

# ============================================================
# 3. Back wall opposite the viewer
# Plane z = 4
# ============================================================

        self.elevator_front_wall_coordinates = [
            # Main wall surface
            quad_z(2.00, 0.00, 0.00, 2.00, 3.00, "#38251B"),

            # Bottom baseboard
            quad_z(1.98, 0.00, 0.10, 2.00, 0.30, "#76583D"),

            # Upper decorative cornice
            quad_z(1.98, 0.00, 2.80, 2.00, 2.95, "#96704A"),

            # Left wooden panel
            quad_z(1.97, 0.08, 0.40, 0.88, 2.60, "#593820"),

            # Right wooden panel
            quad_z(1.97, 1.12, 0.40, 1.92, 2.60, "#593820"),

            # Central decorative panel
            quad_z(1.96, 0.92, 0.40, 1.08, 2.70, "#76583D"),

            # Vertical decorative trim
            quad_z(1.95, 0.12, 0.50, 0.16, 2.50, "#B18A59"),
            quad_z(1.95, 0.84, 0.50, 0.88, 2.50, "#B18A59"),
            quad_z(1.95, 1.12, 0.50, 1.16, 2.50, "#B18A59"),
            quad_z(1.95, 1.84, 0.50, 1.88, 2.50, "#B18A59"),

            # Brass handrail
            quad_z(1.94, 0.00, 1.20, 2.00, 1.30, "#B18A40"),
        ]

    def draw(self,canvas):
        graphics.draw(canvas, self.elevator_gate_coordinates, shift_coordinates=self.shift_coordinates,
                      tag="elevator_gate",object=self)
        graphics.draw(canvas, self.elevator_right_wall_coordinates, shift_coordinates=self.shift_coordinates,
                      tag="elevator_right_wall",object=self)
        graphics.draw(canvas, self.elevator_front_wall_coordinates, shift_coordinates=self.shift_coordinates,
                      tag="elevator_front_wall",object=self)
        graphics.draw(canvas,self.coordinates_hand, shift_coordinates=self.shift_coordinates, tag="lift_hand")

    def draw_hand_delete(self,canvas):
        canvas.delete("lift_hand")

    def draw_hand(self,canvas):
        graphics.draw(canvas,self.coordinates_hand, shift_coordinates=self.shift_coordinates, tag="lift_hand")

    def calculate_circle_pos(self, radius, angle, x, y, z):
        radians = math.radians(angle)
        if x == -1:
            x = 0
            y = 2.65
        else:
            x, y  = graphics.compute_2d_coordinates(x, y, z, shift_coordinates=self.shift_coordinates)
        x = x + radius * math.sin(radians)
        y = y + radius * math.cos(radians)
        return x, y

    def set_floor(self, floor):
        self.floor = floor
        # if self.floor == 0:
        #     self.room_state.set_state_object("lift", self.unique_id, "active")
        angle_add = [0, 50, 160, 210, 240, 250] # [0, 3, 7, 10, 18, 20]
        radius_add = [0.1, 0.06, 0.1, 0.13, 0.15, 0.19] 
        hand_x, hand_y = self.calculate_circle_pos(radius_add[floor], angle=(270 + angle_add[floor]), x=-1, y=-1, z=-1)
        self.coordinates_hand = [
            ["#111111",(0.00, 2.45, 0.85),(hand_x, hand_y, 1),(0.00, 2.45, 0.9)],
        ]

    def get_floor(self):
        return self.floor

    def draw_delete(self):
        # ContextManager().get_canvas().delete("lift_door")
        ContextManager().get_canvas().delete("lift_button")
        ContextManager().get_canvas().delete("lift_hand")

    def clicked(self, event, tag, object, canvas, world_coordinates):
        if tag=="elevator_gate" and self.state == "closed":
            print("[DEBUG] elevator gate clicked!")
            main_window = event.widget.winfo_toplevel()                
            # Call our custom English popup instead of messagebox
            popup = ConfirmationPopup(
                parent_window=main_window,
                title="Change Room",
                message="Do you want to exit the lift?",
                mouse_x=event.x_root, # global position of mouse coordinates
                mouse_y=event.y_root
            )
            # The code pauses until the user clicks a button, then checks popup.result
            if popup.result:
                print("[GAME] Player decided to change the room.")
                for (floor, next_room) in self.floor_room:
                    if floor == self.floor:
                        print(f"[GAME] Changing to room: {next_room}")
                        if self.next_room_callback != None:
                            self.next_room_callback(next_room, True)
                        else:
                            print("[GAME] No next room callback defined.")
                        break
            else:
                print("[GAME] Player decided to stay in the current room.")
            
            self.state = "open" # now open
