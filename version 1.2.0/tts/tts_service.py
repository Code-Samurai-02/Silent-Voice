from kokoro import KPipeline
import sounddevice as sd
import socket
import numpy as np

HOST = "127.0.0.1"
PORT = 5000

VOICE = "af_heart"
SAMPLE_RATE = 24000
VOLUME = 3


def speak_audio(pipeline, text):
    print(f"Speaking: {text}", flush=True)

    audio_chunks = []

    for _, _, audio in pipeline(
        text,
        voice=VOICE
    ):
        audio_chunks.append(audio)

    if audio_chunks:
        audio = np.concatenate(audio_chunks)

        # Increase volume and prevent clipping
        audio = np.clip(audio * VOLUME, -1.0, 1.0)

        sd.play(audio, SAMPLE_RATE)
        sd.wait()


def main():
    print("Loading Kokoro...", flush=True)

    pipeline = KPipeline(lang_code="a")

    print("Kokoro TTS ready.", flush=True)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind((HOST, PORT))
    server.listen(1)

    print(f"TTS running on {HOST}:{PORT}", flush=True)
    print("Waiting for client...", flush=True)

    while True:
        conn, address = server.accept()

        print(f"Client connected: {address}", flush=True)

        with conn:
            buffer = ""

            while True:
                data = conn.recv(4096)

                if not data:
                    print("Client disconnected.", flush=True)
                    break

                buffer += data.decode("utf-8")

                # Handle multiple messages safely
                while "\n" in buffer:
                    text, buffer = buffer.split("\n", 1)

                    text = text.strip()

                    if text:
                        speak_audio(pipeline, text)


if __name__ == "__main__":
    main()