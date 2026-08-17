import unittest
from pathlib import Path
import sys
import tkinter

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from src.escape_room.start_screen import StartScreen

class FakeCanvas:
    def __init__(self):
        self.images = []
        self.rectangles = []
        self.texts = []
        self.bindings = []
        self.deleted = []

    def create_image(self, *points, **kwargs):
        self.images.append({
            "points": points,
            **kwargs,
        })

    def create_rectangle(self, *points, **kwargs):
        self.rectangles.append({
            "points": points,
            **kwargs,
        })

    def create_text(self, *points, **kwargs):
        if len(points) != 2:
            raise ValueError("create_text expects x and y coordinates")
        self.texts.append({
            "points": points,
            **kwargs,
        })

    def tag_bind(self, tag, event, callback):
        self.bindings.append((tag, event, callback))

    def delete(self, target):
        self.deleted.append(target)

    def create_window(self, x, y, *args, **kwargs):
        return 1

def winfo_children():
    return 0
    
class StartScreenTest(unittest.TestCase):
    def test_draw_creates_title_and_start_button(self):
        canvas = FakeCanvas()
        callback = object()
        canvas.master = tkinter.Tk() 
        canvas.winfo_children = winfo_children
        start_screen = StartScreen(canvas, callback,"")

        start_screen.draw()

        self.assertIn("all", canvas.deleted)
        self.assertEqual(canvas.texts[1]["text"], "ESCAPE ROOM")
        self.assertEqual(canvas.texts[-1]["text"], "START GAME")
        self.assertEqual(canvas.bindings[3], ("start_button", "<Button-1>", callback))


if __name__ == "__main__":
    unittest.main()
