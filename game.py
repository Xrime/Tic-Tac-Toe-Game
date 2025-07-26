import customtkinter as ctk
import random
import json
import os

LEADERBOARD_FILE = "leaderboard.json"

class GameBoard(ctk.CTkFrame):
    def __init__(self, app, master, mode, level, player1, player2):
        super().__init__(master)
        self.app = app
        self.mode = mode
        self.level = level
        self.player1 = player1
        self.player2 = player2

        self.current_player = "X"
        self.board = [""] * 9
        self.buttons = []

        self.configure(fg_color="#121212")  # Background color
        self.build_ui()

    def build_ui(self):
        # Game Board Grid
        grid_frame = ctk.CTkFrame(self, fg_color="#1e1e1e", corner_radius=16)
        grid_frame.pack(pady=50)

        for idx in range(9):
            btn = ctk.CTkButton(
                grid_frame,
                text="",
                width=100,
                height=100,
                font=ctk.CTkFont(size=32, weight="bold"),
                command=lambda i=idx: self.handle_click(i),
                fg_color="#2e2e2e",
                hover_color="#444",
                corner_radius=12,
                text_color="white"
            )
            btn.grid(row=idx // 3, column=idx % 3, padx=8, pady=8)
            self.buttons.append(btn)

        # Back to Dashboard Button
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=20)

        ctk.CTkButton(
            btn_frame,
            text="⬅️ Back to Dashboard",
            command=self.return_to_dashboard,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#00ADB5",
            hover_color="#007d82",
            text_color="black",
            corner_radius=10,
            height=36,
            width=180
        ).pack()

    def return_to_dashboard(self):
        self.pack_forget()
        self.app.dashboard.pack(pady=20, padx=20, fill="both", expand=True)

    def handle_click(self, i):
        if self.board[i] == "":
            self.board[i] = self.current_player
            self.buttons[i].configure(text=self.current_player, state="disabled")

            result = self.check_winner()
            if result:
                self.end_game(result)
                return

            if self.mode == "AI" and self.current_player == "X":
                self.current_player = "O"
                self.after(500, self.ai_move)
            else:
                self.current_player = "X" if self.current_player == "O" else "O"

    def ai_move(self):
        move = self.get_ai_move()
        self.board[move] = "O"
        self.buttons[move].configure(text="O", state="disabled")

        result = self.check_winner()
        if result:
            self.end_game(result)
        else:
            self.current_player = "X"

    def get_ai_move(self):
        empty = [i for i, v in enumerate(self.board) if v == ""]

        if self.level == "Easy":
            return random.choice(empty)

        elif self.level == "Medium":
            # Check if AI can win
            for i in empty:
                self.board[i] = "O"
                if self.check_winner() == "O":
                    self.board[i] = ""
                    return i
                self.board[i] = ""

            # Check if AI needs to block player
            for i in empty:
                self.board[i] = "X"
                if self.check_winner() == "X":
                    self.board[i] = ""
                    return i
                self.board[i] = ""

            return random.choice(empty)

        elif self.level == "Hard":
            return self.minimax(self.board, True)[1]

    def minimax(self, board, is_maximizing):
        winner = self.check_winner(board)
        if winner == "O":
            return (1, None)
        elif winner == "X":
            return (-1, None)
        elif "" not in board:
            return (0, None)

        best_move = None
        if is_maximizing:
            max_eval = -float("inf")
            for i in range(9):
                if board[i] == "":
                    board[i] = "O"
                    eval = self.minimax(board, False)[0]
                    board[i] = ""
                    if eval > max_eval:
                        max_eval = eval
                        best_move = i
            return (max_eval, best_move)

        else:
            min_eval = float("inf")
            for i in range(9):
                if board[i] == "":
                    board[i] = "X"
                    eval = self.minimax(board, True)[0]
                    board[i] = ""
                    if eval < min_eval:
                        min_eval = eval
                        best_move = i
            return (min_eval, best_move)

    def check_winner(self, board=None):
        current_board = board if board else self.board
        combos = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for a, b, c in combos:
            if current_board[a] == current_board[b] == current_board[c] and current_board[a] != "":
                return current_board[a]
        if "" not in current_board:
            return "Draw"
        return None

    def end_game(self, result):
        move_analysis = self.generate_move_analysis(result)
        winner = None if result == "Draw" else result

        # Save to leaderboard
        if winner:
            actual_winner = self.player1 if winner == "X" else self.player2
            self.update_leaderboard(actual_winner)

        self.app.show_results(winner, move_analysis)

    def update_leaderboard(self, winner_name):
        if os.path.exists(LEADERBOARD_FILE):
            with open(LEADERBOARD_FILE, 'r') as f:
                data = json.load(f)
        else:
            data = {}

        data[winner_name] = data.get(winner_name, 0) + 1

        with open(LEADERBOARD_FILE, 'w') as f:
            json.dump(data, f, indent=4)

    def generate_move_analysis(self, result):
        analysis = []
        move_count = 0
        for index, move in enumerate(self.board):
            if move != "":
                move_count += 1
                row, col = index // 3, index % 3
                turn = f"📍 Turn {move_count}: Player {move} → Row {row + 1}, Col {col + 1}"
                analysis.append(turn)

        if result == "Draw":
            analysis.append("🤝 It's a draw. Balanced play from both sides!")
        else:
            winner_name = self.player1 if result == "X" else self.player2
            analysis.append(f"🏆 {winner_name} wins the game! Great moves!")

        return analysis

    def reset_board(self):
        self.board = [""] * 9
        self.current_player = "X"  # Reset to starting player
        for btn in self.buttons:
            btn.configure(text="", state="normal")  # Reset text and enable button