# Standard Library
import tkinter as tk
import threading

# Third-party Libraries
import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel

# Load Whisper model
model = WhisperModel("large-v3", device="cuda", compute_type="float16")

samplerate = 16000
duration = 5
threshold = 0.01
running = False


def listen():
    global running
    while running:
        audio = sd.rec(int(duration * samplerate),
                       samplerate=samplerate,
                       channels=1,
                       dtype='float32')
        sd.wait()

        audio = np.squeeze(audio)

        volume = np.abs(audio).mean()

        if volume < threshold:
            continue

        segments, _ = model.transcribe(audio)

        for segment in segments:
            text_box.insert(tk.END, segment.text + "\n")
            text_box.see(tk.END)


def start_listening():
    global running
    if not running:
        running = True
        threading.Thread(target=listen, daemon=True).start()


def stop_listening():
    global running
    running = False


# GUI Window
root = tk.Tk()
root.title("Speech to Text - Whisper")
root.geometry("600x400")

title = tk.Label(root, text="Real Time Speech to Text",
                 font=("Arial", 24, "bold"))
title.pack(pady=10)

text_box = tk.Text(root, height=25, width=130)
text_box.pack(pady=10)

start_btn = tk.Button(root,
                      text="Start Listening",
                      command=start_listening,
                      bg="green",
                      fg="white",
                      width=20)

start_btn.pack(pady=5)

stop_btn = tk.Button(root,
                     text="Stop Listening",
                     command=stop_listening,
                     bg="red",
                     fg="white",
                     width=20)

stop_btn.pack(pady=5)

root.mainloop()