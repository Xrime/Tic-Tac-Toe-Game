import socket
import threading

class NetworkHandler:
    def __init__(self, is_host, ip='127.0.0.1', port=5555):
        self.is_host = is_host
        self.ip = ip
        self.port = port
        self.conn = None
        self.addr = None
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False

    def start(self):
        if self.is_host:
            return self.start_host()
        else:
            return self.start_client()

    def start_host(self):
        try:
            self.socket.bind((self.ip, self.port))
            self.socket.listen(1)
            print(f"[HOSTING] Waiting for connection on {self.ip}:{self.port}...")
            self.conn, self.addr = self.socket.accept()
            self.connected = True
            print(f"[CONNECTED] Client connected from {self.addr}")
            return True
        except Exception as e:
            print(f"[ERROR] Host error: {e}")
            return False

    def start_client(self):
        try:
            self.socket.connect((self.ip, self.port))
            self.conn = self.socket
            self.connected = True
            print(f"[CONNECTED] Connected to host at {self.ip}:{self.port}")
            return True
        except Exception as e:
            print(f"[ERROR] Connection error: {e}")
            return False

    def send(self, data):
        try:
            if self.conn:
                self.conn.sendall(data.encode())
        except Exception as e:
            print(f"[ERROR] Send failed: {e}")

    def receive(self):
        try:
            if self.conn:
                data = self.conn.recv(1024).decode()
                return data
        except Exception as e:
            print(f"[ERROR] Receive failed: {e}")
        return None

    def close(self):
        if self.conn:
            self.conn.close()
        self.socket.close()
        self.connected = False
        print("[DISCONNECTED] Connection closed.")
