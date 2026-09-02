from pathlib import Path

# note: ContextManager has static methods. If used as object, it implements a singleton
class ContextManager():

    _instance = None # singleton instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls) # superclass object handles object creation
        return cls._instance

    def __init__(self):
        # make sure that only once objects are initialized
        if not hasattr(self, "initialized"):
            self.clock = None
            self.canvas = None
            self.initialized = True
            self.action_manager = None
            self.room = None

    @staticmethod
    def get_image_path() -> Path:
        image_path = Path(__file__).resolve().parent.parent / "assets" / "images"
        return image_path

    @staticmethod
    def get_sound_path() -> Path:
        sound_path = Path(__file__).resolve().parent.parent / "assets" / "sounds"
        return sound_path

    # action manager access
    def get_action_manager(self):
        return self.action_manager

    def set_action_manager(self,action_manager):
        self.action_manager = action_manager

    # clock object set/get
    def set_clock(self,clock):
        self.clock = clock

    def get_clock(self):
        return self.clock

    # canvas set/get
    def set_canvas(self,canvas):
        self.canvas = canvas

    def get_canvas(self):
        return self.canvas

    # room
    def set_room(self,room):
        self.room = room

    def get_room(self):
        return self.room
    