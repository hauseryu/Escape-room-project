from escape_room import graphics

class Safe():
    def __init__(self, shift_coordinates=(0, 0, 0)):
        self.shift_coordinates = shift_coordinates
        self.password = "123"
        self.state = 0  # 0 = closed, 1 = open
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
        self.password = new_password

    def clicked(self, event, tag, object, canvas, world_coordinates):        
        canvas.delete("safe")
            
        if self.state == 0: # safe is closed, show input window
            graphics.draw(canvas, self.safe_coordinates, tag="safe", object=self, shift_coordinates=self.shift_coordinates)
            w = canvas.winfo_width()
            h = canvas.winfo_height()
            canvas.create_rectangle(w/2-200, h/2-300, w/2+200, h/2+300, fill="#AAAAAA", outline="", tags="safe_input")
            input_keys = [(w/2-170, h/2-150), (w/2-25, h/2-150), (w/2+120, h/2-150),
            ]
            
