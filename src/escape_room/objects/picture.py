from PIL import Image, ImageTk
from riddles.riddle_generator import generate_riddle

class Picture:
    """A picture frame on the back wall (``z = 4``).
    """

    def __init__(self, image_path=None,is_riddle=None,shift_coordinates = (0,0,0),unique_id=None,room_state=None):
        self.image_path = image_path
        self.is_riddle = is_riddle
        self.shift_coordinates = shift_coordinates
        self.unique_id = unique_id
        self.room_state = room_state

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
        self.image_id = None
        
        self.riddles = []
        self.correct_answers = []
        self.current_riddle = 0

        # check if riddle was created for the picture object already before
        if self.is_riddle:
            riddle_in_room_state = self.room_state.get_state_object("picture",self.unique_id)
            if riddle_in_room_state != None:
                self.riddles = riddle_in_room_state[0:3]
                self.correct_answers = riddle_in_room_state[3:6]
                print("[GAME] Riddle answers: ", end="")
                print(self.correct_answers)
                return

            for _ in range(3):
                try:
                    (riddle, correct_answer) = generate_riddle()
                except ValueError:
                    riddle="riddle not available"
                    correct_answer=""

                self.riddles.append(riddle)
                self.correct_answers.append(correct_answer)
            print("[GAME] Riddle answers: ", end="")
            print(self.correct_answers)        
            self.room_state.set_state_object("picture",self.unique_id,
                                            self.riddles + self.correct_answers)

    def draw_image(self, canvas, tag):
        x1, y1, x2, y2 = canvas.bbox(tag)
        image_width = x2 - x1
        image_heigth = y2 - y1
        image = Image.open(self.image_path)
        image = image.resize((image_width, image_heigth), Image.Resampling.LANCZOS)
        
        self.foto_image = ImageTk.PhotoImage(image, master=canvas)
        
        self.image_id = canvas.create_image(x1, y1, anchor="nw", image=self.foto_image)
        if self.is_riddle:    
            canvas.tag_bind(
                self.image_id,
                "<Button-1>",
                lambda e: self.show_riddle(canvas)
            )
        
    def show_riddle(self, canvas):

            self.current_riddle = 0

            self.draw_riddle(canvas)

            # keyboard navigation
            canvas.focus_set()
            canvas.bind("<Left>", self.previous_riddle)
            canvas.bind("<Right>", self.next_riddle)
            canvas.bind("<Escape>", lambda e: self.close_riddle(canvas))

    def draw_riddle(self, canvas):
        # remove old riddle
        canvas.delete("riddle")

        w = canvas.winfo_width()
        h = canvas.winfo_height()

        # dark overlay
        canvas.create_rectangle(
            0,
            0,
            w,
            h,
            fill="black",
            stipple="gray50",
            tags="riddle"
        )

        # pergament
        margin_x = w * 0.2

        top = h * 0.15 + 100
        bottom = h - 50

        canvas.create_rectangle(
            margin_x,
            top,
            w - margin_x,
            bottom,
            fill="#d8c3a5",
            outline="#7a5230",
            width=4,
            tags="riddle riddle_content"
        )
        
        arrow_space = 130

        text_x = margin_x + arrow_space
        text_y = top + 100

        text_width = w - 2 * margin_x - 2 * arrow_space

        # current riddle text
        canvas.create_text(
            text_x,
            text_y,
            text=self.riddles[self.current_riddle],
            width=text_width,
            font=("Times New Roman", 27),
            justify="left",
            anchor="nw",
            fill="#3b281b",
            tags="riddle riddle_content"
        )
        
        arrow_offset = 70

        # left arrow
        if self.current_riddle > 0:
            canvas.create_text(
                margin_x + arrow_offset,
                h / 2,
                text="←",
                font=("Arial", 35, "bold"),
                fill="#5c3b20",
                tags="riddle previous"
            )

        # right arrow
        if self.current_riddle < len(self.riddles) - 1:
            canvas.create_text(
                w - margin_x - arrow_offset,
                h / 2,
                text="→",
                font=("Arial", 35, "bold"),
                fill="#5c3b20",
                tags="riddle next"
            )

        # Display "1 / 3"
        canvas.create_text(
            w / 2,
            bottom - 35,
            text=f"{self.current_riddle + 1} / {len(self.riddles)}",
            font=("Times New Roman", 18),
            fill="#3b281b",
            tags="riddle riddle_content"
        )

        # Close
        canvas.create_text(
            w - margin_x - 30,
            top + 30,
            text="✕",
            font=("Arial", 20, "bold"),
            fill="#5c3b20",
            tags="riddle riddle_close"
        )

        # Click on X
        canvas.tag_bind(
            "riddle_close",
            "<Button-1>",
            lambda e: self.close_riddle(canvas)
        )

        # Click on left arrow
        canvas.tag_bind(
            "previous",
            "<Button-1>",
            lambda e: self.previous_riddle(e, canvas)
        )

        # Click on right arrow
        canvas.tag_bind(
            "next",
            "<Button-1>",
            lambda e: self.next_riddle(e, canvas)
        )

        # Click on left/right side of the parchment
        canvas.tag_bind(
            "riddle_content",
            "<Button-1>",
            lambda e: self.click_riddle(e, canvas)
        )

    def next_riddle(self, event, canvas=None):
        if canvas is None:
            canvas = event.widget

        if self.current_riddle < len(self.riddles) - 1:
            self.current_riddle += 1
            self.draw_riddle(canvas)

    def previous_riddle(self, event, canvas=None):
        if canvas is None:
            canvas = event.widget

        if self.current_riddle > 0:
            self.current_riddle -= 1
            self.draw_riddle(canvas)

    def click_riddle(self, event, canvas):
        """Click on the left/right side of the riddle."""
        w = canvas.winfo_width()

        if event.x < w / 2:
            self.previous_riddle(event, canvas)
        else:
            self.next_riddle(event, canvas)

    def close_riddle(self, canvas):
        canvas.delete("riddle")

        canvas.unbind("<Left>")
        canvas.unbind("<Right>")
        canvas.unbind("<Escape>")