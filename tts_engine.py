from TTS.api import TTS
import sounddevice as sd
import numpy as np
import socket

print("Loading TTS model...")
tts = TTS(model_name="tts_models/en/ljspeech/vits", progress_bar=False)
print("TTS Engine Ready.")

HOST = "127.0.0.1"
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("Listening for text...")

while True:
    conn, addr = server.accept()
    data = conn.recv(1024).decode()

    if data:
        print("Speaking:", data)
        wav = tts.tts(data)
        wav = np.array(wav, dtype=np.float32)
        sd.play(wav, samplerate=22050)

    conn.close()