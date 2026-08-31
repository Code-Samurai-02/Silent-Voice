import socket

HOST = "127.0.0.1"
PORT = 5000

_client = None


def connect():
    global _client

    if _client is None:
        _client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _client.connect((HOST, PORT))

        print("Connected to TTS.")


def speak(text):
    if not text or not text.strip():
        return

    if _client is None:
        connect()

    _client.sendall((text.strip() + "\n").encode("utf-8"))


def disconnect():
    global _client

    if _client is not None:
        _client.close()
        _client = None

        print("Disconnected from TTS.")