import asyncio
import edge_tts
import socket
import sounddevice as sd
import soundfile as sf
import io

HOST = "127.0.0.1"
PORT = 5005

VOICE = "hi-IN-SwaraNeural"

async def speak(text):
    communicate = edge_tts.Communicate(text=text, voice=VOICE)
    
    audio_bytes = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_bytes += chunk["data"]

    audio_file = io.BytesIO(audio_bytes)
    data, samplerate = sf.read(audio_file)
    sd.play(data, samplerate)
    sd.wait()

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("TTS Server Running...")

        while True:
            conn, addr = s.accept()
            with conn:
                text = conn.recv(4096).decode("utf-8")
                if text:
                    asyncio.run(speak(text))

if __name__ == "__main__":
    start_server()