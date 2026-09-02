from PIL import Image, ImageTk
from riddles.riddle_generator import generate_riddle
from src.escape_room.gui_utilities.speech_bubble import SpeechBubble

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
        self.speech_bubble = SpeechBubble(self.riddles)

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
                lambda e: self.speech_bubble.show_bubble(canvas) 
            )
        
