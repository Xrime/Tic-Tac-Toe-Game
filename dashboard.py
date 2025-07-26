import customtkinter as ctk

class Dashboard(ctk.CTkFrame):
    def __init__(self, app, master):
        super().__init__(master, corner_radius=20)
        self.app = app
        self.configure(fg_color="#121212")

        # Scrollable container
        self.scrollable_container = ctk.CTkScrollableFrame(self, fg_color="#121212", corner_radius=0)
        self.scrollable_container.pack(expand=True, fill="both", padx=10, pady=10)

        # Logo
        self.logo = ctk.CTkLabel(self.scrollable_container, text="TicTacEase", text_color="#00FFAA", font=ctk.CTkFont(size=36, weight="bold"))
        self.logo.pack(pady=30)

        # Player Name Inputs
        self.name_frame = ctk.CTkFrame(self.scrollable_container, fg_color="#1e1e1e", corner_radius=16)
        self.name_frame.pack(pady=10, padx=20)

        ctk.CTkLabel(self.name_frame, text="🎮 Player 1:", text_color="white", font=ctk.CTkFont(size=14)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.player1_entry = ctk.CTkEntry(self.name_frame, corner_radius=10, width=200)
        self.player1_entry.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(self.name_frame, text="🤖 Player 2 / AI:", text_color="white", font=ctk.CTkFont(size=14)).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.player2_entry = ctk.CTkEntry(self.name_frame, corner_radius=10, width=200)
        self.player2_entry.grid(row=1, column=1, padx=10, pady=10)

        # Game Mode Section
        ctk.CTkLabel(self.scrollable_container, text="Select Game Mode", text_color="white", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(25, 5))

        self.mode_var = ctk.StringVar(value="PVP")
        self.mode_frame = ctk.CTkFrame(self.scrollable_container, fg_color="#1e1e1e", corner_radius=12)
        self.mode_frame.pack(padx=20)

        self.pvp_radio = ctk.CTkRadioButton(self.mode_frame, text="🧑‍🤝‍🧑 Player vs Player", variable=self.mode_var, value="PVP", text_color="white", font=ctk.CTkFont(size=14))
        self.pvp_radio.pack(anchor="w", padx=10, pady=5)

        self.ai_radio = ctk.CTkRadioButton(self.mode_frame, text="🤖 Player vs AI", variable=self.mode_var, value="AI", text_color="white", font=ctk.CTkFont(size=14))
        self.ai_radio.pack(anchor="w", padx=10, pady=5)

        self.lan_multiplayer_btn = ctk.CTkButton(
            self.mode_frame, text="🌐 LAN Multiplayer", command=self.app.launch_lan_multiplayer,
            fg_color="#2196F3", hover_color="#1976D2", text_color="white",
            font=ctk.CTkFont(size=14, weight="bold"), corner_radius=12
        )
        self.lan_multiplayer_btn.pack(pady=10)

        # AI Difficulty Section
        ctk.CTkLabel(self.scrollable_container, text="AI Difficulty", text_color="white", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(25, 5))

        self.level_var = ctk.StringVar(value="Easy")
        self.level_frame = ctk.CTkFrame(self.scrollable_container, fg_color="#1e1e1e", corner_radius=12)
        self.level_frame.pack(padx=20)

        for level in ["Easy", "Medium", "Hard"]:
            radio = ctk.CTkRadioButton(self.level_frame, text=level, variable=self.level_var, value=level, text_color="white", font=ctk.CTkFont(size=14))
            radio.pack(anchor="w", padx=10, pady=5)

        # Buttons
        self.start_btn = ctk.CTkButton(
            self.scrollable_container,
            text="🚀 Start Game",
            fg_color="#00FFAA",
            hover_color="#00DD99",
            text_color="black",
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.start_game,
            corner_radius=16,
            height=40,
            width=200
        )
        self.start_btn.pack(pady=(30, 10))

        self.leaderboard_btn = ctk.CTkButton(
            self.scrollable_container,
            text="🏆 View Leaderboard",
            fg_color="#FFA500",
            hover_color="#cc8400",
            text_color="black",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.app.show_leaderboard,
            corner_radius=12,
            height=40,
            width=200
        )
        self.leaderboard_btn.pack(pady=(0, 30))

    def start_game(self):
        player1 = self.player1_entry.get() or "Player 1"
        player2 = self.player2_entry.get() or "Player 2"
        mode = self.mode_var.get()
        level = self.level_var.get()
        self.app.start_game(mode, level, player1, player2)

    def reset(self):
        self.player1_entry.delete(0, 'end')
        self.player2_entry.delete(0, 'end')
        self.mode_var.set("PVP")
        self.level_var.set("Easy")
