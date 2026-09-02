import tkinter as tk
import queue
from pathlib import Path
from PIL import Image, ImageTk
from src.escape_room.application.context_manager import ContextManager

IMAGE_DIR = ContextManager.get_image_path()
CHAT_MESSAGING_ICON = IMAGE_DIR / "chat_messaging.png"

class ChatPanel(tk.Frame):
    """A subarea container to display chat horizontally."""
    def __init__(self, parent_widget, message_queue: queue.Queue, gui_master,player_name=None):
        # Initialize as a Tkinter Frame without hardcoded size limits
        super().__init__(parent_widget, bd=2, relief="groove", padx=10, pady=10)

        self.message_queue = message_queue # queue to send messages to other players
        self.gui_master = gui_master # Reference to trigger the event loop
        self.player_name = player_name

        # --- Section 1: Chat History Display ---
        # We use a tk.Text widget to show all past messages
        # width and height are in character units, not pixels
        try:
            icon = Image.open(CHAT_MESSAGING_ICON).convert("RGBA")
            self.icon_image = ImageTk.PhotoImage(icon, master=gui_master)
            
            # label uses loaded image
            self.icon_label = tk.Label(self, image=self.icon_image)
            self.icon_label.pack(side="left", anchor="n", padx=(0, 10))
        except Exception as e:
            print(f"[CHAT ERROR] Could not load icon: {e}")
        self.chat_history = tk.Text(self, width=20, height=8, state="disabled", wrap="word")
        self.chat_history.pack(fill="both", expand=True, pady=(0, 5))
        
        # --- Section 2: Input Field and Send Button Container ---
        self.input_frame = tk.Frame(self)
        self.input_frame.pack(fill="x", side="bottom") 
        
        self.chat_entry = tk.Entry(self.input_frame, font=("Arial", 11))
        self.chat_entry.pack(side="left", fill="x", expand=True, padx=(0, 5), ipady=8)
        
        self.chat_entry.bind("<Return>", self.on_send_click)
        
        self.send_button = tk.Button(self.input_frame, text="Send", font=("Arial", 10), command=self.on_send_click)
        self.send_button.pack(side="right", ipady=5)
      
    def on_send_click(self, event=None):
        """Triggered when the user clicks 'Send' or presses the Enter key."""
        message_text = self.chat_entry.get().strip()
        
        if message_text:
            # 1. Send the text to the chat history display
            self.append_message("You", message_text)

            # 2. QUEUE EVENT: create package and put into queue
            chat_payload = {
                "action": "chat_message",
                "sent_from": self.player_name,
                "text": message_text
            }
            self.message_queue.put(chat_payload)  # insert into message queue

            # 3. FIRE EVENT: Notify room.py via the Tkinter event loop
            # This triggers the event handler instantly, no .after() loop needed!
            self.gui_master.event_generate("<<ChatEvent>>", when="tail")

            # Clear the input field for the next message
            self.chat_entry.delete(0, tk.END)           

    def append_message(self, sender_name, text_content):
        """Helper method to securely inject a new message row into the locked history."""
        # 1. Temporarily unlock the text widget to allow modification
        self.chat_history.config(state="normal")
        
        # 2. Insert the formatted message at the very end
        formatted_line = f"[{sender_name}]: {text_content}\n"
        self.chat_history.insert(tk.END, formatted_line)
        
        # 3. Automatically scroll down to show the newest message
        self.chat_history.see(tk.END)
        
        # 4. Lock the widget again to prevent manual player editing
        self.chat_history.config(state="disabled")                 