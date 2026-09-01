from src.escape_room.gui_utilities import graphics

class Safe():
    def __init__(self, key = None, shift_coordinates=(0, 0, 0),room_state=None,unique_id=None):
        self.shift_coordinates = shift_coordinates
        self.password = "" # correct password, set using set_password method
        self.input_password = ""
        self.state = 0  # 0 = closed, 1 = open
        self.key = key  # key object that can be placed inside the safe
        self.room_state = room_state
        self.unique_id = unique_id
        self.safe_coordinates = [
        ["#333333",(5.00, 0.90, 4.00),(5.70, 0.90, 4.00),(5.70, 1.30, 4.00),(5.00, 1.30, 4.00)],
        ["#AAAAAA",(5.04, 0.94, 3.99),(5.66, 0.94, 3.99),(5.66, 1.26, 3.99),(5.04, 1.26, 3.99)],
        ["#111111",(5.27, 1.17, 3.98),(5.43, 1.17, 3.98),(5.43, 1.21, 3.98),(5.27, 1.21, 3.98)],
        ["#EEEEEE",(5.25, 1.08, 3.98),(5.31, 1.08, 3.98),(5.31, 1.12, 3.98),(5.25, 1.12, 3.98)],
        ["#EEEEEE",(5.32, 1.08, 3.98),(5.38, 1.08, 3.98),(5.38, 1.12, 3.98),(5.32, 1.12, 3.98)],
        ["#EEEEEE",(5.39, 1.08, 3.98),(5.45, 1.08, 3.98),(5.45, 1.12, 3.98),(5.39, 1.12, 3.98)],
        ["#EEEEEE",(5.25, 1.03, 3.98),(5.31, 1.03, 3.98),(5.31, 1.07, 3.98),(5.25, 1.07, 3.98)],
        ["#EEEEEE",(5.32, 1.03, 3.98),(5.38, 1.03, 3.98),(5.38, 1.07, 3.98),(5.32, 1.07, 3.98)],
        ["#EEEEEE",(5.39, 1.03, 3.98),(5.45, 1.03, 3.98),(5.45, 1.07, 3.98),(5.39, 1.07, 3.98)],
        ["#EEEEEE",(5.25, 0.98, 3.98),(5.31, 0.98, 3.98),(5.31, 1.02, 3.98),(5.25, 1.02, 3.98)],
        ["#EEEEEE",(5.32, 0.98, 3.98),(5.38, 0.98, 3.98),(5.38, 1.02, 3.98),(5.32, 1.02, 3.98)],
        ["#EEEEEE",(5.39, 0.98, 3.98),(5.45, 0.98, 3.98),(5.45, 1.02, 3.98),(5.39, 1.02, 3.98)],
        ]

        self.safe_coordinates_open = [
        ["#333333",(5.00, 0.90, 4.00),(5.70, 0.90, 4.00),(5.70, 1.30, 4.00),(5.00, 1.30, 4.00)],
        ["#242424",(5.04, 0.94, 3.99),(5.66, 0.94, 3.99),(5.66, 1.26, 3.99),(5.04, 1.26, 3.99)],
        ["#AAAAAA",(5.66, 0.94, 3.99),(5.66, 1.26, 3.99),(5.66, 1.26, 3.4), (5.66, 0.94, 3.4)],
        ]


    def check_password(self, input_password):
        return input_password == self.password
    def set_password(self, new_password):
        self.password = "".join(map(str, new_password))

    def clicked(self, event, tag, object, canvas, world_coordinates):
        self.input_password = ""
        canvas.delete("safe")
            
        if self.state == 0: # safe is closed, show input window
            graphics.draw(canvas, self.safe_coordinates, tag="safe", object=self, shift_coordinates=self.shift_coordinates)
            w = canvas.winfo_width()
            h = canvas.winfo_height()

            # dark overlay
            canvas.create_rectangle(0, 0, w, h, fill="#000000", stipple="gray50", outline="", tags="safe_input")    
            
            # background for input window
            safe_x1 = w / 2 - 200
            safe_y1 = h / 2 - 300
            safe_x2 = w / 2 + 200
            safe_y2 = h / 2 + 300
            canvas.create_rectangle(safe_x1, safe_y1,safe_x2, safe_y2,fill="#AAAAAA",outline="",tags="safe_input")

            # draw exit button             
            canvas.create_rectangle(safe_x1+350, safe_y1,safe_x2, safe_y1+50,fill="#AAAAAA",outline="",tags=("safe_input", "safe_exit"))
            canvas.create_text((safe_x1+safe_x2+350) / 2,(safe_y1 + safe_y1+50) / 2,text="X",font=("Arial", 18),fill="#9C2007",tags=("safe_input", "safe_exit"))
            canvas.tag_bind("safe_exit", "<Button-1>", lambda event: self.close_safe_input(event, canvas))

            # black rectangle for input field
            input_width = 240
            input_height = 50
            input_x1 = w / 2 - input_width / 2
            input_y1 = safe_y1 + 100
            input_x2 = w / 2 + input_width / 2
            input_y2 = input_y1 + input_height
            canvas.create_rectangle(input_x1, input_y1,input_x2, input_y2,fill="black",outline="",tags="safe_input")

            # keypad layout
            keys = [
                ["1", "2", "3"],
                ["4", "5", "6"],
                ["7", "8", "9"],
                ["C", "0", "*"]
            ]

            # button dimensions
            button_width = 40
            button_height = 40
            # gap between buttons
            gap_x = 55
            gap_y = 40

            # width of the entire keypad (3 buttons + 2 gaps)
            keypad_width = 2 * gap_x + 3 * button_width
            # starting x position for the keypad (centered)
            start_x = w / 2 - keypad_width / 2

            # starting y position for the keypad
            start_y = input_y2 + 35

            # draw the buttons
            for row, key_row in enumerate(keys):
                for col, key in enumerate(key_row):

                    x1 = start_x + col * (button_width + gap_x)
                    y1 = start_y + row * (button_height + gap_y)

                    x2 = x1 + button_width
                    y2 = y1 + button_height

                    # draw key button
                    canvas.create_rectangle(x1, y1,x2, y2,fill="white",outline="",tags=("safe_input", f"safe_key_{key}"))
                    canvas.create_text((x1 + x2) / 2,(y1 + y2) / 2,text=key,font=("Arial", 18),fill="black",tags=("safe_input", f"safe_key_{key}"))
                    canvas.tag_bind(f"safe_key_{key}", "<Button-1>", lambda event, k=key: self.handle_key_press(event, k, canvas))
        elif self.state == 1: # open safe
            canvas.delete("safe_input")
            canvas.delete("safe")
            graphics.draw(canvas, self.safe_coordinates_open, tag="safe", object=self, shift_coordinates=self.shift_coordinates)

    def close_safe_input(self, event, canvas):
        canvas.delete("safe_input")

    def handle_key_press(self, event, key, canvas):     
        if key == "C":
            self.input_password = ""
        elif key == "*":
            if self.check_password(self.input_password):
                self.state = 1
                self.room_state.set_state_object("safe",self.unique_id,"OPEN")
                self.input_password = ""
                canvas.delete("safe_input")
                canvas.delete("safe")
                graphics.draw(canvas, self.safe_coordinates_open, tag="safe", object=self, shift_coordinates=self.shift_coordinates)
                self.key.draw(canvas)
            else:
                self.input_password = ""
        else:
            self.input_password += key
        
        # Update the input field display
        w = canvas.winfo_width()
        h = canvas.winfo_height()
        input_width = 240
        input_height = 50
        input_x1 = w / 2 - input_width / 2
        input_y1 = h / 2 - 300 + 100
        input_x2 = w / 2 + input_width / 2
        input_y2 = input_y1 + input_height
        
        # Clear the previous text
        canvas.delete("safe_input_text")
        
        # Display the current input password (masked with asterisks)
        masked_input = "*" * len(self.input_password)
        canvas.create_text((input_x1 + input_x2) / 2,(input_y1 + input_y2) / 2,text=masked_input,font=("Arial", 18),fill="white",tags=("safe_input", "safe_input_text"))