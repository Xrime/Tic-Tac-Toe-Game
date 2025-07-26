import customtkinter as ctk
import os

class Dashboard(ctk.CTkFrame):
    def __init__(self, app, master=None):
        super().__init__(master)
        self.app = app
        self.configure(fg_color="transparent")

        # Modern dark overlay frame (no video)
        self.overlay = ctk.CTkFrame(
            self,
            fg_color="#1e1e1e",
            corner_radius=20
        )
        self.overlay.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.6, relheight=0.7)

        self.create_widgets()

    def create_widgets(self):
        ctk.CTkLabel(
            self.overlay,
            text="Welcome to TicTacEase",
            font=("Segoe UI", 28, "bold"),
            text_color="#00FFAA"
        ).pack(pady=20)

        self.mode_var = ctk.StringVar(value="PvP")
        ctk.CTkLabel(self.overlay, text="Game Mode", text_color="#dddddd").pack()
        ctk.CTkOptionMenu(self.overlay, values=["PvP", "AI"], variable=self.mode_var).pack(pady=5)

        self.level_var = ctk.StringVar(value="Easy")
        ctk.CTkLabel(self.overlay, text="AI Level", text_color="#dddddd").pack()
        ctk.CTkOptionMenu(self.overlay, values=["Easy", "Medium", "Hard"], variable=self.level_var).pack(pady=5)

        ctk.CTkLabel(self.overlay, text="Player 1 Name", text_color="#dddddd").pack()
        self.p1_entry = ctk.CTkEntry(self.overlay, placeholder_text="Player 1")
        self.p1_entry.pack(pady=5)

        ctk.CTkLabel(self.overlay, text="Player 2 Name", text_color="#dddddd").pack()
        self.p2_entry = ctk.CTkEntry(self.overlay, placeholder_text="Player 2 / Robot")
        self.p2_entry.pack(pady=5)

        ctk.CTkButton(self.overlay, text="Start Game", command=self.start_game).pack(pady=20)

    def start_game(self):
        mode = self.mode_var.get()
        level = self.level_var.get()
        player1 = self.p1_entry.get()
        player2 = self.p2_entry.get()
        self.app.start_game(mode, level, player1, player2)
