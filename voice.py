# Standard Library
import tkinter as tk
import threading
import os

# Third-party
import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel
from PIL import Image, ImageTk


# Load Whisper
model = WhisperModel("large-v3", device="cuda", compute_type="float16")

samplerate = 16000
duration = 4
threshold = 0.01
running = False
mode = "text"


# ---------- SIGN IMAGE DISPLAY ----------
def show_signs(text):

    for widget in sign_frame.winfo_children():
        widget.destroy()

    if mode == "text":
        return

    text = text.upper()
    words = text.split(" ")

    row = 0

    for word in words:

        col = 0

        for letter in word:

            if letter.isalpha():

                path = os.path.join("sign", f"{letter}.jpg")

                if os.path.exists(path):

                    img = Image.open(path)
                    img = img.resize((80, 80))

                    img = ImageTk.PhotoImage(img)

                    lbl = tk.Label(sign_frame, image=img, bg="#121212")
                    lbl.image = img
                    lbl.grid(row=row, column=col, padx=5, pady=5)

                    col += 1

        row += 1


# ---------- SPEECH LISTENER ----------
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

            text = segment.text.strip()

            text_box.insert(tk.END, text + "\n")
            text_box.see(tk.END)

            show_signs(text)


# ---------- CONTROL ----------
def start_listening():
    global running

    if not running:
        running = True
        status_label.config(text="Listening...", fg="#00ff9d")
        threading.Thread(target=listen, daemon=True).start()


def stop_listening():
    global running
    running = False
    status_label.config(text="Stopped", fg="orange")


def change_mode():
    global mode
    mode = mode_var.get()


# ---------- GUI ----------
root = tk.Tk()
root.title("Silent Voice - Speech to Sign")
root.geometry("900x650")
root.configure(bg="#121212")


title = tk.Label(root,
                 text="Silent Voice : Speech → Text / Sign",
                 font=("Arial", 22, "bold"),
                 bg="#121212",
                 fg="#00d9ff")
title.pack(pady=10)


status_label = tk.Label(root,
                        text="Idle",
                        font=("Arial", 12),
                        bg="#121212",
                        fg="orange")
status_label.pack()


# ---------- MODE SELECTOR ----------
mode_frame = tk.Frame(root, bg="#121212")
mode_frame.pack(pady=10)

mode_var = tk.StringVar(value="text")

tk.Label(mode_frame,
         text="Mode:",
         bg="#121212",
         fg="white",
         font=("Arial", 12)).pack(side="left", padx=5)

tk.Radiobutton(mode_frame,
               text="Text Only",
               variable=mode_var,
               value="text",
               command=change_mode,
               bg="#121212",
               fg="white",
               selectcolor="#333").pack(side="left", padx=5)

tk.Radiobutton(mode_frame,
               text="Sign + Text",
               variable=mode_var,
               value="sign",
               command=change_mode,
               bg="#121212",
               fg="white",
               selectcolor="#333").pack(side="left", padx=5)


# ---------- TEXT BOX ----------
text_box = tk.Text(root,
                   height=8,
                   font=("Arial", 16),
                   bg="#0f0f0f",
                   fg="#00ff9d",
                   insertbackground="white")
text_box.pack(fill="x", padx=20, pady=10)


# ---------- SIGN DISPLAY WITH SCROLL ----------
sign_container = tk.Frame(root, bg="#121212")
sign_container.pack(fill="both", expand=True, padx=20, pady=10)

canvas = tk.Canvas(sign_container, bg="#121212", highlightthickness=0)
scrollbar = tk.Scrollbar(sign_container, orient="vertical", command=canvas.yview)

scrollable_frame = tk.Frame(canvas, bg="#121212")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")


def resize_canvas(event):
    canvas.itemconfig(canvas_window, width=event.width)


canvas.bind("<Configure>", resize_canvas)

canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")


# Mouse wheel scroll
def _on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


canvas.bind_all("<MouseWheel>", _on_mousewheel)

sign_frame = scrollable_frame


# ---------- BUTTONS ----------
btn_frame = tk.Frame(root, bg="#121212")
btn_frame.pack(pady=10)

start_btn = tk.Button(btn_frame,
                      text="Start Listening",
                      command=start_listening,
                      bg="#00c853",
                      fg="black",
                      width=15)

start_btn.grid(row=0, column=0, padx=10)

stop_btn = tk.Button(btn_frame,
                     text="Stop Listening",
                     command=stop_listening,
                     bg="#ff5252",
                     fg="white",
                     width=15)

stop_btn.grid(row=0, column=1, padx=10)


root.mainloop()
