import serial
import time
import threading
import tkinter as tk
from tkinter import ttk

import middleware
import middleware_hi


ser = serial.Serial("COM5", 115200, timeout=1)

last_star_time = 0
STAR_DEBOUNCE_MS = 500

temp = ""
last_letter = None

valid_letters = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

lan = 1
running = False


def start_listening():
    global lan, running

    lan = 1 if language_var.get() == "English" else 2

    running = True

    status_label.config(text="Listening...", fg="#00ff9d")

    thread = threading.Thread(target=serial_reader)
    thread.daemon = True
    thread.start()


def serial_reader():
    global temp, last_letter, last_star_time

    while running:

        if ser.in_waiting:

            data = ser.readline().decode(errors="ignore")
            data = data.replace("\r", "").replace("\n", "")

            if not data or data == "Error":
                continue

            received_text.set(data)

            if data in valid_letters:
                last_letter = data
                stored_text.set(last_letter)
            elif data == "EMERGENCYCALL":
                last_letter = "EMERGENCYCALL"
                stored_text.set(last_letter)
            elif data == " ":
                temp += " "
                sentence_text.set(temp)
                time.sleep(1)

            elif data == "*":

                current_time = time.time() * 1000

                if (current_time - last_star_time) < STAR_DEBOUNCE_MS:
                    continue

                last_star_time = current_time

                if last_letter:
                    temp += last_letter
                    sentence_text.set(temp)
                    last_letter = None

                time.sleep(1)

            elif data == ".":

                final_text.set(temp)
                if temp == "EMERGENCYCALL":
                    print("EMERGENCY CALL TRIGGERED")
                    import call
                    temp = ""
                    last_letter = ""
                    continue
                if lan == 1:
                    middleware.send_text(str(temp))
                elif lan == 2:
                    middleware_hi.send_text(str(temp))

                time.sleep(1.5)

                temp = ""
                last_letter = ""


# GUI
root = tk.Tk()
root.title("Silent Voice")
root.geometry("520x420")
root.configure(bg="#121212")

title = tk.Label(
    root,
    text="Silent Voice Receiver",
    font=("Arial", 20, "bold"),
    bg="#121212",
    fg="#00d9ff"
)
title.pack(pady=10)


# Language selection
lang_frame = tk.Frame(root, bg="#121212")
lang_frame.pack(pady=10)

tk.Label(
    lang_frame,
    text="Select Language",
    bg="#13d6b9",
    fg="white",
    font=("Arial", 13, "bold")
).pack(pady=5)

language_var = tk.StringVar()
language_var.set("English")

language_dropdown = ttk.Combobox(
    lang_frame,
    textvariable=language_var,
    values=["English", "Hindi"],
    state="readonly",
    font=("Arial", 12, "bold"),
    width=15
)

language_dropdown.pack()

# Start button
start_btn = tk.Button(
    root,
    text="Start Listening",
    command=start_listening,
    font=("Arial", 12, "bold"),
    bg="#00d9ff",
    fg="black",
    width=18
)
start_btn.pack(pady=10)


status_label = tk.Label(
    root,
    text="Not Started",
    bg="#121212",
    fg="orange",
    font=("Arial", 12)
)
status_label.pack()


# Live data frame
data_frame = tk.Frame(root, bg="#1e1e1e", bd=2, relief="ridge")
data_frame.pack(pady=10, padx=20, fill="x")

received_text = tk.StringVar()
stored_text = tk.StringVar()

tk.Label(
    data_frame,
    text="Received",
    bg="#1e1e1e",
    fg="#bbbbbb"
).pack()

tk.Label(
    data_frame,
    textvariable=received_text,
    font=("Arial", 16),
    bg="#1e1e1e",
    fg="#00ff9d"
).pack(pady=3)

tk.Label(
    data_frame,
    text="Stored Letter",
    bg="#1e1e1e",
    fg="#bbbbbb"
).pack()

tk.Label(
    data_frame,
    textvariable=stored_text,
    font=("Arial", 16),
    bg="#1e1e1e",
    fg="#ffd166"
).pack(pady=3)


# Sentence builder
sentence_frame = tk.Frame(root, bg="#1e1e1e", bd=2, relief="ridge")
sentence_frame.pack(pady=10, padx=20, fill="x")

sentence_text = tk.StringVar()

tk.Label(
    sentence_frame,
    text="Current Sentence",
    bg="#1e1e1e",
    fg="white"
).pack()

tk.Label(
    sentence_frame,
    textvariable=sentence_text,
    font=("Arial", 18, "bold"),
    bg="#1e1e1e",
    fg="#00d9ff"
).pack(pady=5)


# Final output
final_frame = tk.Frame(root, bg="#1e1e1e", bd=2, relief="ridge")
final_frame.pack(pady=10, padx=20, fill="x")

final_text = tk.StringVar()

tk.Label(
    final_frame,
    text="Final Output",
    bg="#1e1e1e",
    fg="white"
).pack()

tk.Label(
    final_frame,
    textvariable=final_text,
    font=("Arial", 20, "bold"),
    bg="#1e1e1e",
    fg="#00ff9d"
).pack(pady=5)


root.mainloop()
