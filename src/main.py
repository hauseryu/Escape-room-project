import tkinter
import sys

from src.escape_room.application import globals
from src.escape_room.application.escape_app import EscapeApp

def main():
    root = tkinter.Tk()
    
    root.title("Escape Room Game")

    try:
        app = EscapeApp(root)
    except RuntimeError:
        root.destroy()
        sys.exit()
    
    root.geometry(f"{globals.canvas_width}x{globals.canvas_height}")
    root.mainloop()

if __name__ == "__main__":
    main()
