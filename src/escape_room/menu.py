import tkinter as tk


class Menu(tk.Frame):

    def __init__(self, parent):
        super().__init__(
            parent,
            bg="#222222",
            bd=2,
            relief="solid"
        )


        self.create_menu()

    def create_menu(self):
        tk.Button(
            self,
            text="Speichern",
            command=self.save_game
        ).pack(fill="x", padx=20, pady=10)

        tk.Button(
            self,
            text="Beenden",
            command=self.quit_game
        ).pack(fill="x", padx=20, pady=10)

    def save_game(self):
        self.app.save_game()

    def quit_game(self):
        self.app.quit_game()