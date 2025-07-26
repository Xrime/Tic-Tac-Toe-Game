import customtkinter as ctk

class CustomMessageBox(ctk.CTkToplevel):
    def __init__(self, master, title="Message", message="Something happened!", width=400, height=200):
        super().__init__(master)
        self.title(title)
        self.geometry(f"{width}x{height}")
        self.resizable(False, False)
        self.configure(fg_color="#1e1e1e")

        ctk.CTkLabel(
            self,
            text=message,
            text_color="white",
            font=ctk.CTkFont(size=16, weight="bold"),
            wraplength=360,
            justify="center"
        ).pack(pady=30, padx=20)

        ctk.CTkButton(
            self,
            text="OK",
            command=self.destroy,
            corner_radius=12,
            fg_color="#00ffaa",
            hover_color="#00ddaa",
            text_color="black",
            font=ctk.CTkFont(size=14, weight="bold"),
            width=100
        ).pack(pady=10)
