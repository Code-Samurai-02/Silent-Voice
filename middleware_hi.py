import socket
from deep_translator import GoogleTranslator

def eng_to_hindi(text: str) -> str:
    return GoogleTranslator(source='en', target='hi').translate(text)

HOST = "127.0.0.1"
PORT = 5005

def send_text(text: str):
    temp = eng_to_hindi(text)
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(temp.encode("utf-8"))
    except ConnectionRefusedError:
        print("TTS server is not running.")