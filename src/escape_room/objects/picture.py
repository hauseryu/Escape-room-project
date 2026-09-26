from PIL import Image, ImageTk
from llm.riddle_generator import generate_riddle
from src.escape_room.gui_utilities.speech_bubble import SpeechBubble
from src.escape_room.gui_utilities import graphics
from src.escape_room.application.context_manager import ContextManager

class Picture:
    """A picture frame on the back wall (``z = 4``).
    """

    def __init__(self, room_data,index,image_path,room_state):

        # evaluate room data
        try:
            (x,y,z) = room_data["picture"][index]["coord"] # get picture coordinates (first element in list)
        except:
            (x,y,z) = (0,0,0)
        file_name = room_data["picture"][index]["image"] 
        image_location = image_path / file_name
        is_riddle = room_data["picture"][index]["is_riddle"]
        try:
            direction = room_data["picture"][index]["direction"]
        except:
            direction = "front"
        unique_id = room_data["picture"][index]["unique_id"] # unique identifier
        try:
            pic_move_coord = room_data["picture"][index]["pic_move_coord"] # move picture to 2-d pixels 
        except:
            pic_move_coord = (0,0)
        try:
            pic_resize = room_data["picture"][index]["pic_resize"] # resize picture in 2-d pixels 
        except:
            pic_resize = None
        try:
            draw_frame = room_data["picture"][index]["draw_frame"] # shall a frame be drawn?
        except:
            draw_frame = True
        try:
            needed_inventory =  room_data["picture"][index]["needed_inventory"] # this inventory item needs to be used to activate picture
        except:
            needed_inventory = None
        try:
            check_activation =  room_data["picture"][index]["check_activation"] # check the object state to enable using (clicking) the object
        except:
            check_activation = None
        try:
            is_clickable = room_data["picture"][index]["is_clickable"]
        except:
            is_clickable = False
        try:
            action_sequence = room_data["picture"][index]["action_sequence"]
        except:
            action_sequence = None
        shift_coordinates = (x-5.05,y-2.35,z-4.0)            

        # set attributes
        self.image_location = image_location
        self.is_riddle = is_riddle
        self.direction = direction
        self.shift_coordinates = shift_coordinates
        self.unique_id = unique_id
        self.room_state = room_state
        self.pic_move_coord = pic_move_coord
        self.pic_resize = pic_resize
        self.draw_frame = draw_frame
        self.needed_inventory = needed_inventory
        self.check_activation = check_activation
        self.is_clickable = is_clickable
        self.action_sequence = action_sequence

        if self.draw_frame:
            if self.direction == "front":
                self.coordinates_frame = [
                    ["#4A2B18", (5.05, 2.35, 4), (5.75, 2.35, 4),
                    (5.75, 1.45, 4), (5.05, 1.45, 4)],
                    ["#C79045", (5.10, 2.30, 4), (5.70, 2.30, 4),
                    (5.70, 1.50, 4), (5.10, 1.50, 4)],
                ]
                self.coordinates_image = [
                    ["#24364B", (5.15, 2.25, 4), (5.65, 2.25, 4),
                    (5.65, 1.55, 4), (5.15, 1.55, 4)],
                ]
            elif self.direction == "left":
                self.coordinates_frame = [
                    ["#4A2B18", (5.05, 2.35, 4.0), (5.05, 2.35, 4.7),
                    (5.05, 1.45, 4.7), (5.05, 1.45, 4.0)],
                    ["#C79045", (5.05, 2.30, 4.05), (5.05, 2.30, 4.65),
                    (5.05, 1.50, 4.65), (5.05, 1.50, 4.05)],
                ]
                self.coordinates_image = [
                    ["#24364B", (5.05, 2.25, 4.1), (5.05, 2.25, 4.6),
                    (5.05, 1.55, 4.6), (5.05, 1.55, 4.1)],
                ]
            elif self.direction == "right":
                self.coordinates_frame = [
                    ["#4A2B18", (5.05, 2.35, 4.0), (5.05, 2.35, 3.3),
                    (5.05, 1.45, 3.3), (5.05, 1.45, 4.0)],
                    ["#C79045", (5.05, 2.30, 3.95), (5.05, 2.30, 3.35),
                    (5.05, 1.50, 3.35), (5.05, 1.50, 3.95)],
                ]
                self.coordinates_image = [
                    ["#24364B", (5.05, 2.25, 3.9), (5.05, 2.25, 3.4),
                    (5.05, 1.55, 3.4), (5.05, 1.55, 3.9)],
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

    def draw(self, canvas, tag):
        # draw outline (frame)
        if self.draw_frame:
            graphics.draw(canvas,self.coordinates_frame,shift_coordinates=self.shift_coordinates)
            graphics.draw(canvas,self.coordinates_image,tag="picture",
                        shift_coordinates=self.shift_coordinates)
            # draw image
            x1, y1, x2, y2 = canvas.bbox(tag)
            image_width = x2 - x1
            image_height = y2 - y1
        else:
            (x1,y1)=self.pic_move_coord
        image = Image.open(self.image_location)
        
        if self.pic_resize == None:
            self.foto_image = ImageTk.PhotoImage(image, master=canvas)
        else:
            (image_width,image_height) = self.pic_resize
            resized_image = image.resize((image_width, image_height), Image.Resampling.LANCZOS)
            
            # 2. Das skalierte Bild an ImageTk übergeben
            self.foto_image = ImageTk.PhotoImage(resized_image, master=canvas)
        
        # 3. Das Bild auf dem Canvas wie gewohnt platzieren
        if self.is_riddle:
            self.image_id = canvas.create_image(x1, y1, anchor="nw", image=self.foto_image)
        else:
            self.image_id = canvas.create_image(self.pic_move_coord[0], self.pic_move_coord[1], anchor="nw", image=self.foto_image)

        if self.is_clickable:
            canvas.tag_bind(
                self.image_id,
                "<Button-1>", 
                lambda event: self.on_key_click(event)
            )            

    def on_key_click(self, event):
        print("[DEBUG] Picture clicked!")
        canvas = ContextManager().get_canvas()
        inventory = ContextManager().get_inventory()
        if self.needed_inventory != None:
            obj = inventory.getSelectedObject()
            if obj[0] != self.needed_inventory:
                return
        if self.check_activation != None:
            usage_allowed = ContextManager().get_action_manager().execute_action_sequence(self.check_activation)
            if not usage_allowed:
                print("[DEBUG] Object not yet activated!")
                return
        if self.riddles!=[]:
            self.speech_bubble.show_bubble(canvas)        
        elif self.action_sequence!=None:
            print("[DEBUG] execute action sequence of picture!")
            ContextManager().get_action_manager().execute_action_sequence(self.action_sequence)