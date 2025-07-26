import customtkinter as ctk
from component  import CustomMessageBox


class GameBoardLAN(ctk.CTkFrame):
    def __init__(self, app, master, network_handler, player_name, opponent_name):
        super().__init__(master)
        self.app = app
        self.network = network_handler
        self.player_name = player_name
        self.opponent_name = opponent_name

        self.symbol = "X" if self.network.role == "host" else "O"
        self.is_my_turn = self.symbol == "X"
        self.board = [""] * 9
        self.buttons = []

        self.network.set_receive_callback(self.receive_move)
        self.network.set_disconnect_callback(self.handle_disconnect)

        self.configure(fg_color="#121212")
        self.build_ui()

    def build_ui(self):
        # Game Info
        ctk.CTkLabel(
            self,
            text=f"🎮 {self.player_name} ({self.symbol}) vs {self.opponent_name} ({'O' if self.symbol == 'X' else 'X'})",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="white"
        ).pack(pady=(30, 10))

        # Game Grid
        grid_frame = ctk.CTkFrame(self, fg_color="#1e1e1e", corner_radius=12)
        grid_frame.pack(pady=20)

        for idx in range(9):
            btn = ctk.CTkButton(
                grid_frame,
                text="",
                width=90,
                height=90,
                font=ctk.CTkFont(size=32, weight="bold"),
                command=lambda i=idx: self.handle_click(i),
                fg_color="#2c2c2c",
                hover_color="#3e3e3e",
                corner_radius=10
            )
            btn.grid(row=idx // 3, column=idx % 3, padx=6, pady=6)
            self.buttons.append(btn)

        # Back Button
        ctk.CTkButton(
            self,
            text="🏠 Back to Dashboard",
            command=self.return_to_dashboard,
            fg_color="#FF8800",
            hover_color="#DD7700",
            text_color="black",
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=12,
            width=200
        ).pack(pady=20)

    def handle_click(self, index):
        if not self.is_my_turn:
            CustomMessageBox(self, title="Wait Turn", message="It's not your turn yet.")
            return

        if self.board[index] != "":
            CustomMessageBox(self, title="Invalid Move", message="That square is already taken.")
            return

        self.make_move(index, self.symbol)
        self.network.send_move(index)

        if self.check_winner(self.symbol):
            self.declare_winner(self.player_name)
        elif "" not in self.board:
            self.declare_draw()
        else:
            self.is_my_turn = False

    def receive_move(self, index):
        opponent_symbol = "O" if self.symbol == "X" else "X"
        self.make_move(index, opponent_symbol)

        if self.check_winner(opponent_symbol):
            self.declare_winner(self.opponent_name)
        elif "" not in self.board:
            self.declare_draw()
        else:
            self.is_my_turn = True

    def make_move(self, index, symbol):
        self.board[index] = symbol
        self.buttons[index].configure(text=symbol, text_color="white")

    def check_winner(self, symbol):
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        return any(all(self.board[i] == symbol for i in condition) for condition in win_conditions)

    def declare_winner(self, name):
        CustomMessageBox(self, title="🎉 Game Over", message=f"{name} wins!")
        self.after(1500, self.return_to_dashboard)

    def declare_draw(self):
        CustomMessageBox(self, title="Game Over", message="🤝 It's a draw!")
        self.after(1500, self.return_to_dashboard)

    def return_to_dashboard(self):
        self.network.close_connection()
        self.app.return_to_dashboard()

    def handle_disconnect(self):
        CustomMessageBox(self, title="Disconnected", message="⚠️ Opponent disconnected.")
        self.after(1500, self.return_to_dashboard)
