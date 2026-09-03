import os
import time
import threading
import tkinter as tk
from tkinter import scrolledtext

# =============================
# Add NVIDIA DLL paths to PATH
# =============================
import nvidia.cublas
import nvidia.cuda_nvrtc

for pkg in [nvidia.cublas, nvidia.cuda_nvrtc]:
    dll_dir = os.path.join(os.path.dirname(pkg.__path__[0]), pkg.__name__.split(".")[-1], "bin")
    if os.path.isdir(dll_dir):
        os.environ["PATH"] = dll_dir + os.pathsep + os.environ.get("PATH", "")
        os.add_dll_directory(dll_dir)

import sounddevice as sd
import scipy.io.wavfile as wav
from faster_whisper import WhisperModel


# =============================================================
# GUI Application
# =============================================================

class STTApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Silent Voice - Speech to Text")
        self.root.geometry("700x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#2b2b2b")

        # =============================
        # Settings
        # =============================
        self.SAMPLE_RATE = 16000
        self.CHANNELS = 1
        self.RECORD_SECONDS = 3
        self.AUDIO_FILE = "recording.wav"

        self.running = False
        self.model = None

        # =============================
        # UI Setup
        # =============================
        self._build_ui()

        # =============================
        # Load model
        # =============================
        self._log("Loading Whisper model...")
        self.status_var.set("Loading model...")

        load_thread = threading.Thread(target=self._load_model, daemon=True)
        load_thread.start()

        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    # ---------------------------------------------------------
    # Build the user interface
    # ---------------------------------------------------------
    def _build_ui(self):
        title_label = tk.Label(
            self.root,
            text="Silent Voice",
            font=("Helvetica", 22, "bold"),
            fg="#ffffff",
            bg="#2b2b2b",
        )
        title_label.pack(pady=(15, 5))

        subtitle_label = tk.Label(
            self.root,
            text="Speech to Text",
            font=("Helvetica", 12),
            fg="#aaaaaa",
            bg="#2b2b2b",
        )
        subtitle_label.pack()

        # --- Status ---
        self.status_var = tk.StringVar(value="Initializing...")
        self.status_label = tk.Label(
            self.root,
            textvariable=self.status_var,
            font=("Helvetica", 12, "bold"),
            fg="#ffc107",
            bg="#2b2b2b",
        )
        self.status_label.pack(pady=(15, 5))

        # --- Transcription Display ---
        tk.Label(
            self.root,
            text="Transcription",
            font=("Helvetica", 11, "bold"),
            fg="#cccccc",
            bg="#2b2b2b",
            anchor="w",
        ).pack(fill=tk.X, padx=20, pady=(10, 2))

        self.transcription_area = scrolledtext.ScrolledText(
            self.root,
            width=80,
            height=8,
            state=tk.DISABLED,
            font=("Helvetica", 12),
            bg="#1a1a2e",
            fg="#00e676",
            insertbackground="#ffffff",
            wrap=tk.WORD,
        )
        self.transcription_area.pack(padx=20, pady=(2, 10))

        # --- Buttons ---
        btn_frame = tk.Frame(self.root, bg="#2b2b2b")
        btn_frame.pack(pady=5)

        self.start_btn = tk.Button(
            btn_frame,
            text="▶  Start Listening",
            font=("Helvetica", 12, "bold"),
            fg="#ffffff",
            bg="#388e3c",
            activebackground="#2e7d32",
            activeforeground="#ffffff",
            width=18,
            relief=tk.FLAT,
            cursor="hand2",
            command=self._start_listening,
            state=tk.DISABLED,
        )
        self.start_btn.pack(side=tk.LEFT, padx=10)

        self.stop_btn = tk.Button(
            btn_frame,
            text="■  Stop",
            font=("Helvetica", 12, "bold"),
            fg="#ffffff",
            bg="#d32f2f",
            activebackground="#c62828",
            activeforeground="#ffffff",
            width=18,
            relief=tk.FLAT,
            cursor="hand2",
            command=self._stop_listening,
            state=tk.DISABLED,
        )
        self.stop_btn.pack(side=tk.LEFT, padx=10)

        # --- Log ---
        tk.Label(
            self.root,
            text="Log",
            font=("Helvetica", 11, "bold"),
            fg="#cccccc",
            bg="#2b2b2b",
            anchor="w",
        ).pack(fill=tk.X, padx=20, pady=(10, 2))

        self.log_area = scrolledtext.ScrolledText(
            self.root,
            width=80,
            height=8,
            state=tk.DISABLED,
            font=("Consolas", 10),
            bg="#1e1e1e",
            fg="#d4d4d4",
            insertbackground="#ffffff",
            wrap=tk.WORD,
        )
        self.log_area.pack(padx=20, pady=(2, 15))

    # ---------------------------------------------------------
    # Logging helper
    # ---------------------------------------------------------
    def _log(self, text):
        self.log_area.configure(state=tk.NORMAL)
        self.log_area.insert(tk.END, text + "\n")
        self.log_area.see(tk.END)
        self.log_area.configure(state=tk.DISABLED)

    # ---------------------------------------------------------
    # Append transcription text
    # ---------------------------------------------------------
    def _append_transcription(self, text):
        self.transcription_area.configure(state=tk.NORMAL)
        self.transcription_area.insert(tk.END, text + "\n")
        self.transcription_area.see(tk.END)
        self.transcription_area.configure(state=tk.DISABLED)

    # ---------------------------------------------------------
    # Load model (runs on background thread)
    # ---------------------------------------------------------
    def _load_model(self):
        print("Loading Whisper model...")

        self.model = WhisperModel(
            "large-v3-turbo",
            device="cuda",
            compute_type="float16"
        )

        print("Model loaded successfully.")
        self.root.after(0, self._on_model_loaded)

    def _on_model_loaded(self):
        self._log("Model loaded successfully.")
        self.status_var.set("Ready — Press Start")
        self.status_label.configure(fg="#00e676")
        self.start_btn.configure(state=tk.NORMAL)

    # ---------------------------------------------------------
    # Start / Stop controls
    # ---------------------------------------------------------
    def _start_listening(self):
        self.running = True
        self.start_btn.configure(state=tk.DISABLED)
        self.stop_btn.configure(state=tk.NORMAL)
        self.status_var.set("Listening...")
        self.status_label.configure(fg="#42a5f5")
        self._log("Starting continuous speech recognition...")

        print("Starting continuous speech recognition...")
        print("Press Ctrl+C to stop.\n")

        stt_thread = threading.Thread(target=self._stt_loop, daemon=True)
        stt_thread.start()

    def _stop_listening(self):
        self.running = False
        self.start_btn.configure(state=tk.NORMAL)
        self.stop_btn.configure(state=tk.DISABLED)
        self.status_var.set("Stopped")
        self.status_label.configure(fg="#ffc107")
        self._log("STT stopped.")

        print("\nSTT stopped.")

    # ---------------------------------------------------------
    # Continuous STT loop (runs on background thread)
    # ---------------------------------------------------------
    def _stt_loop(self):
        try:
            while self.running:

                print("Listening...")
                self.root.after(0, self._set_status, "🎙  Listening...", "#42a5f5")
                self.root.after(0, self._log, "Listening...")

                # Record audio
                audio = sd.rec(
                    int(self.RECORD_SECONDS * self.SAMPLE_RATE),
                    samplerate=self.SAMPLE_RATE,
                    channels=self.CHANNELS,
                    dtype="int16"
                )

                sd.wait()

                if not self.running:
                    break

                self.root.after(0, self._set_status, "⏳  Transcribing...", "#ffc107")

                # Save audio
                wav.write(
                    self.AUDIO_FILE,
                    self.SAMPLE_RATE,
                    audio
                )

                # Transcribe
                segments, info = self.model.transcribe(
                    self.AUDIO_FILE,
                    language="en",
                    beam_size=5
                )

                text = " ".join(
                    segment.text.strip()
                    for segment in segments
                )

                # Print result
                if text.strip():
                    print(f"Speech: {text}")
                    self.root.after(0, self._log, f"Speech: {text}")
                    self.root.after(0, self._append_transcription, text)
                else:
                    print("No speech detected.")
                    self.root.after(0, self._log, "No speech detected.")

                print()

        except Exception as e:
            self.root.after(0, self._log, f"Error: {e}")
            self.root.after(0, self._stop_listening)

    # ---------------------------------------------------------
    # Status helper
    # ---------------------------------------------------------
    def _set_status(self, text, color):
        self.status_var.set(text)
        self.status_label.configure(fg=color)

    # ---------------------------------------------------------
    # Cleanup on window close
    # ---------------------------------------------------------
    def _on_close(self):
        self.running = False
        self.root.destroy()


# =============================================================
# Entry Point
# =============================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = STTApp(root)
    root.mainloop()
