import customtkinter as ctk

class ResultScreen(ctk.CTkFrame):
    def __init__(self, app, master, winner, move_analysis, player1, player2):
        super().__init__(master)
        self.app = app
        self.winner = winner
        self.move_analysis = move_analysis
        self.player1 = player1
        self.player2 = player2

        self.symbol = "X"  # Add this line to define the starting symbol
        self.is_my_turn = True
        self.board = [""] * 9
        self.buttons = []

        self.configure(fg_color="#121212")
        self.build_ui()

    def build_ui(self):
        ctk.CTkLabel(
            self,
            text="🎮 Game Over",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="white"
        ).pack(pady=(30, 10))

        result_text = "🤝 It's a Draw!" if self.winner is None else f"🏆 {self.player1 if self.winner == 'X' else self.player2} Wins!"
        result_color = "#AAAAAA" if self.winner is None else "#00FFAA"

        ctk.CTkLabel(
            self,
            text=result_text,
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=result_color
        ).pack(pady=(0, 20))

        ctk.CTkLabel(
            self,
            text="📊 Move Analysis",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="white"
        ).pack(pady=(0, 10))

        # Scrollable frame
        scrollable = ctk.CTkScrollableFrame(self, width=500, height=220, fg_color="#1e1e1e", corner_radius=10)
        scrollable.pack(pady=10, padx=20)

        for move in self.move_analysis:
            ctk.CTkLabel(
                scrollable,
                text=move,
                font=ctk.CTkFont(size=14),
                text_color="white",
                anchor="w",
                justify="left"
            ).pack(anchor="w", padx=10, pady=4)

        # Action Buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=30)



        ctk.CTkButton(
            btn_frame,
            text="🏠 Dashboard",
            command=self.app.return_to_dashboard,
            fg_color="#FFA500",
            hover_color="#FF8C00",
            text_color="black",
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=12,
            width=140
        ).grid(row=0, column=1, padx=15)

    def reset_board(self):
        self.board = [""] * 9
        self.is_my_turn = self.symbol == "O"
        for btn in self.buttons:
            btn.configure(text="")

