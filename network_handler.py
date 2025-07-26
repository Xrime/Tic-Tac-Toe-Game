import socket
import threading

class NetworkHandler:
    def __init__(self, role, host_ip="127.0.0.1", port=65432):
        self.role = role
        self.host_ip = host_ip
        self.port = port
        self.conn = None
        self.sock = None
        self.receive_callback = None

    def start_server(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host_ip, self.port))
        self.sock.listen(1)
        print("Waiting for client to connect...")
        self.conn, _ = self.sock.accept()
        print("Client connected")
        threading.Thread(target=self.receive_loop, daemon=True).start()

    def connect_to_server(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host_ip, self.port))
            self.conn = self.sock
            threading.Thread(target=self.receive_loop, daemon=True).start()
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            return False

    def send(self, data):
        try:
            self.conn.sendall(data.encode())
        except:
            print("Failed to send data")

    def receive_loop(self):
        while True:
            try:
                data = self.conn.recv(1024)
                if data:
                    message = data.decode()
                    if self.receive_callback:
                        self.receive_callback(message)
                else:
                    break
            except:
                break

    def set_receive_callback(self, callback):
        self.receive_callback = callback
