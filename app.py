import customtkinter as ctk
import pygame
from dashboard import Dashboard
from game import GameBoard
from resultscreen import ResultScreen
from leaderboard import LeaderboardScreen
import json
import os
from tkinter import simpledialog, messagebox
from utils import resource_path, writable_path


music = resource_path("mixkit-playful-10.mp3")
leaderboard_file = writable_path("leaderboard.json")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("TicTacEase")
        self.geometry("800x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self.dashboard = Dashboard(app=self, master=self)
        self.dashboard.pack(pady=20, padx=20, fill="both", expand=True)

    def start_game(self, mode, level, player1, player2):
        self.dashboard.pack_forget()
        if hasattr(self, "result_screen"):
            self.result_screen.pack_forget()
        if hasattr(self, "leaderboard_screen"):
            self.leaderboard_screen.pack_forget()

        self.game_board = GameBoard(
            app=self,
            master=self,
            mode=mode,
            level=level,
            player1=player1,
            player2=player2
        )
        self.game_board.pack(pady=20, padx=20, fill="both", expand=True)

    def show_results(self, winner, move_analysis):
        if hasattr(self, "game_board"):
            self.game_board.pack_forget()

        self.result_screen = ResultScreen(
            app=self,
            master=self,
            winner=winner,
            player1=self.game_board.player1,
            player2=self.game_board.player2,
            move_analysis=move_analysis
        )
        self.result_screen.pack(pady=20, padx=20, fill="both", expand=True)

        if winner and winner != "Draw":
            self.update_leaderboard(winner)

    def restart_game(self):
        if self.game_board:
            self.game_board.reset_board()
            self.show_frame(self.game_board)

    def return_to_dashboard(self):
        if hasattr(self, "game_board"):
            self.game_board.pack_forget()
        if hasattr(self, "result_screen"):
            self.result_screen.pack_forget()
        if hasattr(self, "leaderboard_screen"):
            self.leaderboard_screen.pack_forget()

        self.dashboard.pack(pady=20, padx=20, fill="both", expand=True)

    def show_leaderboard(self):
        if hasattr(self, "game_board"):
            self.game_board.pack_forget()
        if hasattr(self, "result_screen"):
            self.result_screen.pack_forget()
        if hasattr(self, "dashboard"):
            self.dashboard.pack_forget()

        self.leaderboard_screen = LeaderboardScreen(app=self, master=self)
        self.leaderboard_screen.pack(pady=20, padx=20, fill="both", expand=True)

    def update_leaderboard(self, winner):

        if os.path.exists(leaderboard_file):
            with open(leaderboard_file, "r") as f:
                leaderboard = json.load(f)
        else:
            leaderboard = {}

        leaderboard[winner] = leaderboard.get(winner, 0) + 1

        with open(leaderboard_file, "w") as f:
            json.dump(leaderboard, f)

    def launch_lan_multiplayer(self):
        choice = simpledialog.askstring("LAN Multiplayer", "Do you want to host or join? (Enter: host/join)")
        if choice is None:
            return

        from network_handler import NetworkHandler

        if choice.lower() == "host":
            player_name = simpledialog.askstring("Your Name", "Enter your name:")
            opponent_name = "Waiting..."
            handler = NetworkHandler(role='host')
            handler.start_server()
            self.start_lan_game(handler, player_name, opponent_name)

        elif choice.lower() == "join":
            ip = simpledialog.askstring("Join Game", "Enter Host IP Address:")
            player_name = simpledialog.askstring("Your Name", "Enter your name:")
            opponent_name = "Host"

            if ip and player_name:
                handler = NetworkHandler(role='client', host_ip=ip)
                connected = handler.connect_to_server()
                if connected:
                    self.start_lan_game(handler, player_name, opponent_name)
                else:
                    messagebox.showerror("Connection Failed", "Could not connect to host.")
        else:
            messagebox.showwarning("Invalid Choice", "Please enter 'host' or 'join'.")

    def start_lan_game(self, network_handler, player_name, opponent_name):
        self.dashboard.pack_forget()
        from gameboard_lan_lan import GameBoardLAN
        self.game_screen = GameBoardLAN(
            app=self,
            master=self,
            network_handler=network_handler,
            player_name=player_name,
            opponent_name=opponent_name
        )
        self.game_screen.pack(padx=20, pady=20, fill="both", expand=True)



# 🎵 Background Music
pygame.mixer.init()
pygame.mixer.music.load(music)
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

if __name__ == "__main__":
    app = App()
    app.mainloop()
