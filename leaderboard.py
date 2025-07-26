import customtkinter as ctk
import json
import os

LEADERBOARD_FILE = "leaderboard.json"

class LeaderboardScreen(ctk.CTkFrame):
    def __init__(self, app, master):
        super().__init__(master, corner_radius=20)
        self.app = app
        self.configure(fg_color="#121212")
        self.build_ui()

    def build_ui(self):
        # Title
        ctk.CTkLabel(
            self,
            text="🏆 Leaderboard",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="white"
        ).pack(pady=(30, 10))

        # Scrollable Leaderboard Section
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self,
            width=600,
            height=360,
            fg_color="#1e1e1e",
            corner_radius=10
        )
        self.scrollable_frame.pack(pady=10, padx=20)

        self.load_leaderboard()

        # Buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=25)

        ctk.CTkButton(
            btn_frame,
            text="← Back to Dashboard",
            command=self.app.return_to_dashboard,
            fg_color="#00FFAA",
            hover_color="#00DD99",
            text_color="black",
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=12,
            width=180
        ).grid(row=0, column=0, padx=15)

        ctk.CTkButton(
            btn_frame,
            text="🗑 Reset Leaderboard",
            command=self.reset_leaderboard,
            fg_color="#FF5555",
            hover_color="#DD4444",
            text_color="white",
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=12,
            width=180
        ).grid(row=0, column=1, padx=15)

    def load_leaderboard(self):
        # Clear existing widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Load and display leaderboard data
        if os.path.exists(LEADERBOARD_FILE):
            with open(LEADERBOARD_FILE, 'r') as f:
                data = json.load(f)
        else:
            data = {}

        if data:
            sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)
            for idx, (player, wins) in enumerate(sorted_data, 1):
                entry = f"{idx}. {player} - {wins} win{'s' if wins != 1 else ''}"
                ctk.CTkLabel(
                    self.scrollable_frame,
                    text=entry,
                    font=ctk.CTkFont(size=16),
                    text_color="white"
                ).pack(anchor="w", pady=4, padx=15)
        else:
            ctk.CTkLabel(
                self.scrollable_frame,
                text="No games played yet.",
                font=ctk.CTkFont(size=16, slant="italic"),
                text_color="gray"
            ).pack(pady=20)

    def reset_leaderboard(self):
        if os.path.exists(LEADERBOARD_FILE):
            os.remove(LEADERBOARD_FILE)
        self.load_leaderboard()
