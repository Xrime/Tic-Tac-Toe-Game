import sys, os

def resource_path(relative_path: str) -> str:
    return os.path.join(getattr(sys, "_MEIPASS", os.path.abspath(".")), relative_path)

def writable_path(filename: str) -> str:
    """For files you create/modify at runtime (e.g., leaderboard.json)."""
    return os.path.join(os.getcwd(), filename)
