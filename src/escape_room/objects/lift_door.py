from src.escape_room.gui_utilities import graphics
from src.escape_room.application.context_manager import ContextManager
from src.escape_room.gui_utilities.confirmation_popup import ConfirmationPopup

import math

class LiftDoor():
    def __init__(self, room_data, index, room_state, next_room_callback=None):

        # evaluate room data
        (x,y,z) = room_data["lift_door"][index][0] # get lift door coordinates (first element in list)
        self.unique_id = room_data["lift_door"][index][1]
        self.floor = room_data["lift_door"][index][2]
        self.next_room = room_data["lift_door"][index][3]
        self.check_action = room_data["lift_door"][index][4]
        self.index = index
        self.room_data = room_data
        self.room_state = room_state
        self.next_room_callback = next_room_callback
        self.shift_coordinates = (x-0,y-0,z-5)
        
        self.elevator_gate_coordinates = [
            # background rectangle
            ["#303030",(0.00, 0.00, 5.00),(0.00, 0.00, 6.50),(0.00, 2.50, 6.50),(0.00, 2.50, 5.00)], 

            # frame in the back, dark wrought iron
            ["#302D2A",(0.00, 0.00, 5.00),(0.00, 0.00, 5.10),(0.00, 2.50, 5.10),(0.00, 2.50, 5.00)], # left post
            ["#302D2A",(0.00, 0.00, 6.40),(0.00, 0.00, 6.50),(0.00, 2.50, 6.50),(0.00, 2.50, 6.40)], # right post
            ["#403B35",(0.00, 0.00, 5.00),(0.00, 0.10, 5.00),(0.00, 0.10, 6.50),(0.00, 0.00, 6.50)], # lower frame
            ["#403B35",(0.00, 2.40, 5.00),(0.00, 2.50, 5.00),(0.00, 2.50, 6.50),(0.00, 2.40, 6.50)], # upper frame

            # bars in the back
            ["#514940",(0.00, 0.10, 5.18),(0.00, 0.10, 5.23),(0.00, 2.40, 5.23),(0.00, 2.40, 5.18)],
            ["#514940",(0.00, 0.10, 5.43),(0.00, 0.10, 5.48),(0.00, 2.40, 5.48),(0.00, 2.40, 5.43)],
            ["#514940",(0.00, 0.10, 5.68),(0.00, 0.10, 5.73),(0.00, 2.40, 5.73),(0.00, 2.40, 5.68)],
            ["#514940",(0.00, 0.10, 5.93),(0.00, 0.10, 5.98),(0.00, 2.40, 5.98),(0.00, 2.40, 5.93)],
            ["#514940",(0.00, 0.10, 6.18),(0.00, 0.10, 6.23),(0.00, 2.40, 6.23),(0.00, 2.40, 6.18)],

            # crossbars in the back
            ["#514940",(0.00, 0.55, 5.10),(0.00, 0.60, 5.10),(0.00, 0.60, 6.40),(0.00, 0.55, 6.40)],
            ["#514940",(0.00, 1.25, 5.10),(0.00, 1.30, 5.10),(0.00, 1.30, 6.40),(0.00, 1.25, 6.40)],
            ["#514940",(0.00, 1.95, 5.10),(0.00, 2.00, 5.10),(0.00, 2.00, 6.40),(0.00, 1.95, 6.40)],

            # frame in the front, bronze color
            ["#76583D",(-0.08, 0.00, 5.00),(-0.08, 0.00, 5.10),(-0.08, 2.50, 5.10),(-0.08, 2.50, 5.00)], # left post
            ["#76583D",(-0.08, 0.00, 6.40),(-0.08, 0.00, 6.50),(-0.08, 2.50, 6.50),(-0.08, 2.50, 6.40)], # right post
            ["#96704A",(-0.08, 0.00, 5.00),(-0.08, 0.10, 5.00),(-0.08, 0.10, 6.50),(-0.08, 0.00, 6.50)], # lower frame
            ["#96704A",(-0.08, 2.40, 5.00),(-0.08, 2.50, 5.00),(-0.08, 2.50, 6.50),(-0.08, 2.40, 6.50)], # upper frame

            # bars in the front
            ["#96704A",(-0.08, 0.10, 5.18),(-0.08, 0.10, 5.23),(-0.08, 2.40, 5.23),(-0.08, 2.40, 5.18)],
            ["#96704A",(-0.08, 0.10, 5.43),(-0.08, 0.10, 5.48),(-0.08, 2.40, 5.48),(-0.08, 2.40, 5.43)],
            ["#96704A",(-0.08, 0.10, 5.68),(-0.08, 0.10, 5.73),(-0.08, 2.40, 5.73),(-0.08, 2.40, 5.68)],
            ["#96704A",(-0.08, 0.10, 5.93),(-0.08, 0.10, 5.98),(-0.08, 2.40, 5.98),(-0.08, 2.40, 5.93)],
            ["#96704A",(-0.08, 0.10, 6.18),(-0.08, 0.10, 6.23),(-0.08, 2.40, 6.23),(-0.08, 2.40, 6.18)],
           
            # crossbars in the front
            ["#96704A",(-0.08, 0.55, 5.10),(-0.08, 0.60, 5.10),(-0.08, 0.60, 6.40),(-0.08, 0.55, 6.40)],
            ["#96704A",(-0.08, 1.25, 5.10),(-0.08, 1.30, 5.10),(-0.08, 1.30, 6.40),(-0.08, 1.25, 6.40)],
            ["#96704A",(-0.08, 1.95, 5.10),(-0.08, 2.00, 5.10),(-0.08, 2.00, 6.40),(-0.08, 1.95, 6.40)],
            
            # decoration in the middle
            ["#B18A59",(-0.09, 2.20, 5.45),(-0.09, 2.24, 5.45),(-0.09, 2.24, 6.05),(-0.09, 2.20, 6.05)], # small horizontal decorative strip
            ["#B18A59",(-0.09, 2.12, 5.55),(-0.09, 2.16, 5.55),(-0.09, 2.16, 5.95),(-0.09, 2.12, 5.95)], # decorative strip below
            ["#C09A63",(-0.10, 1.65, 5.70),(-0.10, 1.78, 5.85),(-0.10, 1.65, 6.00),(-0.10, 1.52, 5.85)], # diamond-shaped ornament in the middle
            ["#B18A59",(-0.09, 2.22, 5.18),(-0.09, 2.26, 5.18),(-0.09, 2.26, 5.42),(-0.09, 2.22, 5.42)], # small decorative strip on the top left
            ["#B18A59",(-0.09, 2.22, 6.08),(-0.09, 2.26, 6.08),(-0.09, 2.26, 6.32),(-0.09, 2.22, 6.32)], # small decorative strip on the top right

        ]
        
        self.stone_arch_coordinates = [
            # background rectangle
            ["#8A8175",(0, 2.5, 4.75),(0, 2.5, 6.75),(0, 3, 6.75),(0, 3, 4.75)],

            ["#8A8175",(0, 0.0, 4.75),(0, 0.0, 5.00),(0, 2.50, 5.00),(0, 2.50, 4.75)], # left post
            ["#8A8175",(0, 0.0, 6.50),(0, 0.0, 6.75),(0, 2.50, 6.75),(0, 2.50, 6.50)], # right post           

            # decorative seams on the left post
            ["#625B52",(0, 0.65, 4.75),(0, 0.68, 4.75),(0, 0.68, 5.00),(0, 0.65, 5.00)],
            ["#625B52",(0, 1.35, 4.75),(0, 1.38, 4.75),(0, 1.38, 5.00),(0, 1.35, 5.00)],
            ["#625B52",(0, 2.05, 4.75),(0, 2.08, 4.75),(0, 2.08, 5.00),(0, 2.05, 5.00)],

            # seams on the right post
            ["#625B52",(0, 0.65, 6.50),(0, 0.68, 6.50),(0, 0.68, 6.75),(0, 0.65, 6.75)],
            ["#625B52",(0, 1.35, 6.50),(0, 1.38, 6.50),(0, 1.38, 6.75),(0, 1.35, 6.75)],
            ["#625B52",(0, 2.05, 6.50),(0, 2.08, 6.50),(0, 2.08, 6.75),(0, 2.05, 6.75)],
        ]

        
        self.elevator_gate_open_coordinates = [           
            # background rectangle
            ["#303030",(0.00, 0.00, 5.00),(0.00, 0.00, 6.50),(0.00, 2.50, 6.50),(0.00, 2.50, 5.00)],

            ["#76583D",(0.00, 0.00, 5.00),(0.08, 0.00, 5.00),(0.08, 2.50, 5.00),(0.00, 2.50, 5.00)], # outer post
            ["#76583D",(0.67, 0.00, 5.00),(0.75, 0.00, 5.00),(0.75, 2.50, 5.00),(0.67, 2.50, 5.00)], # inner post
            ["#96704A",(0.08, 0.00, 5.00),(0.67, 0.00, 5.00),(0.67, 0.10, 5.00),(0.08, 0.10, 5.00)], # lower frame
            ["#96704A",(0.08, 2.40, 5.00),(0.67, 2.40, 5.00),(0.67, 2.50, 5.00),(0.08, 2.50, 5.00)], # upper frame

            # vertical bars
            ["#96704A",(0.16, 0.10, 5.00),(0.20, 0.10, 5.00),(0.20, 2.40, 5.00),(0.16, 2.40, 5.00)],
            ["#96704A",(0.31, 0.10, 5.00),(0.35, 0.10, 5.00),(0.35, 2.40, 5.00),(0.31, 2.40, 5.00)],
            ["#96704A",(0.46, 0.10, 5.00),(0.50, 0.10, 5.00),(0.50, 2.40, 5.00),(0.46, 2.40, 5.00)],

            # Querstreben
            ["#96704A",(0.08, 0.70, 5.00),(0.67, 0.70, 5.00),             (0.67, 0.75, 5.00),             (0.08, 0.75, 5.00)],
            ["#96704A",(0.08, 1.40, 5.00),(0.67, 1.40, 5.00),             (0.67, 1.45, 5.00),             (0.08, 1.45, 5.00)],
            ["#96704A",(0.08, 2.05, 5.00),(0.67, 2.05, 5.00),             (0.67, 2.10, 5.00),             (0.08, 2.10, 5.00)],
            
            # right wing – 90 degrees open
            ["#76583D",(0.00, 0.00, 6.50),(0.08, 0.00, 6.50),(0.08, 2.50, 6.50),(0.00, 2.50, 6.50)], # outer post
            ["#76583D",(0.67, 0.00, 6.50),(0.75, 0.00, 6.50),(0.75, 2.50, 6.50),(0.67, 2.50, 6.50)], # inner post
            ["#96704A",(0.08, 0.00, 6.50),(0.67, 0.00, 6.50),(0.67, 0.10, 6.50),(0.08, 0.10, 6.50)], # lower frame
            ["#96704A",(0.08, 2.40, 6.50),(0.67, 2.40, 6.50),(0.67, 2.50, 6.50),(0.08, 2.50, 6.50)], # upper frame
            # vertical bars
            ["#96704A",(0.16, 0.10, 6.50),(0.20, 0.10, 6.50),(0.20, 2.40, 6.50),(0.16, 2.40, 6.50)],
            ["#96704A",(0.31, 0.10, 6.50),(0.35, 0.10, 6.50),(0.35, 2.40, 6.50),(0.31, 2.40, 6.50)],
            ["#96704A",(0.46, 0.10, 6.50),(0.50, 0.10, 6.50),(0.50, 2.40, 6.50),(0.46, 2.40, 6.50)],
            # crossbars
            ["#96704A",(0.08, 0.70, 6.50),(0.67, 0.70, 6.50),(0.67, 0.75, 6.50),(0.08, 0.75, 6.50)],
            ["#96704A",(0.08, 1.40, 6.50),(0.67, 1.40, 6.50),(0.67, 1.45, 6.50),(0.08, 1.45, 6.50)],
            ["#96704A",(0.08, 2.05, 6.50),(0.67, 2.05, 6.50),(0.67, 2.10, 6.50),(0.08, 2.10, 6.50)],
        ]
        self.call_button = [
            ["#9e9065",(0.00, 1.3, 6.55),(0.00, 1.3, 6.7),(0.00, 1.45, 6.7),(0.00, 1.45, 6.55)],
            ["#f5e9c4",(0.00, 1.33, 6.58),(0.00, 1.33, 6.67),(0.00, 1.42, 6.625)],           
        ]
        ContextManager().set_lift(self)
        self.set_floor(self.floor)
        self.state = "closed"


    def draw(self, canvas):        
        graphics.draw(canvas,self.stone_arch_coordinates,shift_coordinates=self.shift_coordinates)
        graphics.draw(canvas,self.call_button, object=self, shift_coordinates=self.shift_coordinates, tag = "lift_button")
        
        if self.state == "closed":
            graphics.draw(canvas,self.elevator_gate_coordinates, object=self, shift_coordinates=self.shift_coordinates, tag="lift_door")
        elif self.state == "open":
            graphics.draw(canvas,self.elevator_gate_open_coordinates, object=self, shift_coordinates=self.shift_coordinates, tag="lift_door")        

        floors = ["5", "4", "3", "2", "1", "G"]
        for i, floor in enumerate(floors):
            floor_angle = i * 36 + 80            
            x, y = self.calculate_circle_pos(radius=20, angle=floor_angle, x=0, y=2.65, z=5.75)
            canvas.create_text(x, y, text=floor, font=("Arial", 10), fill="black", tag="lift_door")

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
        if self.floor == 0:
            self.room_state.set_state_object("lift_door", self.unique_id, "active")
        angle_add = [0, 3, 7, 10, 18, 20]
        hand_x, hand_y = self.calculate_circle_pos(radius=0.1, angle=(floor * 36 + 270 + angle_add[floor]), x=-1, y=-1, z=-1)
        self.coordinates_hand = [
            ["#111111",(0.00, 2.6, 5.75),(hand_x, hand_y, 5.75)],
        ]

    def get_floor(self):
        return self.floor

    def draw_delete(self):
        ContextManager().get_canvas().delete("lift_door")
        ContextManager().get_canvas().delete("lift_button")
        ContextManager().get_canvas().delete("lift_hand")

    def clicked(self, event, tag, object, canvas, world_coordinates):
        if tag == "lift_button" and self.floor>3:
            ContextManager().get_action_manager().execute_action_sequence("lift_moves_to_ground")
        elif tag == "lift_door" and self.state == "closed":
            print("[DEBUG] lift door clicked!")
            open_allowed = True
            if self.check_action != None:
                open_allowed = ContextManager().get_action_manager().execute_action_sequence(self.check_action)
            if not open_allowed:
                print("[DEBUG] opening lift door not allowed!")
                return
            
            main_window = event.widget.winfo_toplevel()                
            # Call our custom English popup instead of messagebox
            popup = ConfirmationPopup(
                parent_window=main_window,
                title="Change Room",
                message="Do you want to enter the lift?",
                mouse_x=event.x_root, # global position of mouse coordinates
                mouse_y=event.y_root
            )
            # The code pauses until the user clicks a button, then checks popup.result
            if popup.result:
                print("[GAME] Player decided to change the room.")
                if self.next_room_callback != None:
                    self.next_room_callback(self.next_room, True)
            else:
                print("[GAME] Player decided to stay in the current room.")
            
            self.state = "open" # now open
            self.draw_delete()
            self.draw(canvas)
