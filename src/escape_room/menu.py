import tkinter as tk


class Menu(tk.Frame):

    def __init__(self, parent):
        super().__init__(
            parent,
            bg="#D4C8C8",
            bd=2,
            relief="solid"
        )


        self.create_menu()

    def create_menu(self):
        tk.Button(
            self,
            text="Save",
            command=self.save_game
        ).pack(fill="x", padx=20, pady=10)
       
        tk.Button(
            self,
            text="Return to \nstart screen",
            command=self.return_to_start_screen,
            height=2
        ).pack(fill="x", padx=20, pady=20)

    def save_game(self):
        self.app.save_game()

    def return_to_start_screen(self):
        self.app.return_to_start_screen()
        
