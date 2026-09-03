import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tts.tts_client import connect, speak, disconnect

# =============================================================
# GUI Application
# =============================================================

class SilentVoiceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Silent Voice - Sign Language Interpreter")
        self.root.geometry("700x550")
        self.root.resizable(False, False)
        self.root.configure(bg="#2b2b2b")

        # -------------------------
        # Variables MUST be outside loop
        # -------------------------
        self.temp = ""
        self.word = ""

        # -------------------------
        # TTS
        # -------------------------
        connect()

        # -------------------------
        # UI Setup
        # -------------------------
        self._build_ui()

        # -------------------------
        # UDP (runs on background thread)
        # -------------------------
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("0.0.0.0", 5001))
        self.running = True

        udp_thread = threading.Thread(target=self._udp_loop, daemon=True)
        udp_thread.start()

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
            text="Sign Language Interpreter",
            font=("Helvetica", 12),
            fg="#aaaaaa",
            bg="#2b2b2b",
        )
        subtitle_label.pack()

        # --- Current Letter ---
        letter_frame = tk.Frame(self.root, bg="#2b2b2b")
        letter_frame.pack(pady=(15, 5))

        tk.Label(
            letter_frame,
            text="Current Letter:",
            font=("Helvetica", 12),
            fg="#aaaaaa",
            bg="#2b2b2b",
        ).pack(side=tk.LEFT)

        self.letter_var = tk.StringVar(value="-")
        tk.Label(
            letter_frame,
            textvariable=self.letter_var,
            font=("Helvetica", 28, "bold"),
            fg="#00e676",
            bg="#2b2b2b",
            width=3,
        ).pack(side=tk.LEFT, padx=(10, 0))

        # --- Current Word ---
        word_frame = tk.Frame(self.root, bg="#2b2b2b")
        word_frame.pack(pady=(5, 10))

        tk.Label(
            word_frame,
            text="Word:",
            font=("Helvetica", 12),
            fg="#aaaaaa",
            bg="#2b2b2b",
        ).pack(side=tk.LEFT)

        self.word_var = tk.StringVar(value="")
        tk.Label(
            word_frame,
            textvariable=self.word_var,
            font=("Helvetica", 20, "bold"),
            fg="#42a5f5",
            bg="#2b2b2b",
            anchor="w",
            width=30,
        ).pack(side=tk.LEFT, padx=(10, 0))

        # --- Status ---
        self.status_var = tk.StringVar(value="UDP server listening...")
        tk.Label(
            self.root,
            textvariable=self.status_var,
            font=("Helvetica", 10),
            fg="#ffc107",
            bg="#2b2b2b",
        ).pack(pady=(0, 5))

        # --- Log ---
        tk.Label(
            self.root,
            text="Log",
            font=("Helvetica", 11, "bold"),
            fg="#cccccc",
            bg="#2b2b2b",
            anchor="w",
        ).pack(fill=tk.X, padx=20)

        self.log_area = scrolledtext.ScrolledText(
            self.root,
            width=80,
            height=15,
            state=tk.DISABLED,
            font=("Consolas", 10),
            bg="#1e1e1e",
            fg="#d4d4d4",
            insertbackground="#ffffff",
            wrap=tk.WORD,
        )
        self.log_area.pack(padx=20, pady=(2, 15))

        self._log("UDP server listening...")

    # ---------------------------------------------------------
    # Logging helper
    # ---------------------------------------------------------
    def _log(self, text):
        self.log_area.configure(state=tk.NORMAL)
        self.log_area.insert(tk.END, text + "\n")
        self.log_area.see(tk.END)
        self.log_area.configure(state=tk.DISABLED)

    # ---------------------------------------------------------
    # Update UI from background thread (thread-safe)
    # ---------------------------------------------------------
    def _update_ui(self, letter=None, log_text=None):
        if letter is not None:
            self.letter_var.set(letter)
        self.word_var.set(self.word)
        if log_text is not None:
            self._log(log_text)

    # ---------------------------------------------------------
    # UDP listener loop (runs on daemon thread)
    # ---------------------------------------------------------
    def _udp_loop(self):
        while self.running:
            try:
                data, addr = self.sock.recvfrom(1024)
            except OSError:
                break

            message = data.decode().strip()

            print("Received:", message)

            # -------------------------------------------------
            # Letters
            # -------------------------------------------------

            if message == "Thumb_Up-Index_Down-Middle_Down-Ring_Down-Pinky_Down":
                print("a")
                self.temp = "a"
                self.root.after(0, self._update_ui, "a", "Received: a")

            elif message == "Thumb_Half-Index_Up-Middle_Up-Ring_Up-Pinky_Up":
                print("b")
                self.temp = "b"
                self.root.after(0, self._update_ui, "b", "Received: b")

            elif message == "Thumb_Up-Index_Half-Middle_Half-Ring_Half-Pinky_Half":
                print("c")
                self.temp = "c"
                self.root.after(0, self._update_ui, "c", "Received: c")

            elif message == "Thumb_Half-Index_Up-Middle_Down-Ring_Down-Pinky_Down":
                print("d")
                self.temp = "d"
                self.root.after(0, self._update_ui, "d", "Received: d")

            elif message == "Thumb_Half-Index_Half-Middle_Half-Ring_Half-Pinky_Half":
                print("e")
                self.temp = "e"
                self.root.after(0, self._update_ui, "e", "Received: e")

            elif message == "Thumb_Half-Index_Half-Middle_Up-Ring_Up-Pinky_Up":
                print("f")
                self.temp = "f"
                self.root.after(0, self._update_ui, "f", "Received: f")

            elif message == "Thumb_Up-Index_Down-Middle_Down-Ring_Half-Pinky_Up":
                print("g")
                self.temp = "g"
                self.root.after(0, self._update_ui, "g", "Received: g")

            elif message == "Thumb_Down-Index_Half-Middle_Half-Ring_Down-Pinky_Down":
                print("h")
                self.temp = "h"
                self.root.after(0, self._update_ui, "h", "Received: h")

            elif message == "Thumb_Up-Index_Down-Middle_Down-Ring_Down-Pinky_Up":
                print("i")
                self.temp = "i"
                self.root.after(0, self._update_ui, "i", "Received: i")

            elif message == "Thumb_Up-Index_Down-Middle_Half-Ring_Half-Pinky_Up":
                print("j")
                self.temp = "j"
                self.root.after(0, self._update_ui, "j", "Received: j")

            elif message == "Thumb_Up-Index_Up-Middle_Up-Ring_Down-Pinky_Down":
                print("k")
                self.temp = "k"
                self.root.after(0, self._update_ui, "k", "Received: k")

            elif message == "Thumb_Up-Index_Up-Middle_Down-Ring_Down-Pinky_Down":
                print("l")
                self.temp = "l"
                self.root.after(0, self._update_ui, "l", "Received: l")

            elif message == "Thumb_Half-Index_Up-Middle_Up-Ring_Down-Pinky_Up":
                print("m")
                self.temp = "m"
                self.root.after(0, self._update_ui, "m", "Received: m")

            elif message == "Thumb_Half-Index_Up-Middle_Down-Ring_Half-Pinky_Up":
                print("n")
                self.temp = "n"
                self.root.after(0, self._update_ui, "n", "Received: n")

            elif message == "Thumb_Down-Index_Down-Middle_Down-Ring_Down-Pinky_Up":
                print("o")
                self.temp = "o"
                self.root.after(0, self._update_ui, "o", "Received: o")

            elif message == "Thumb_Up-Index_Up-Middle_Down-Ring_Half-Pinky_Up":
                print("p")
                self.temp = "p"
                self.root.after(0, self._update_ui, "p", "Received: p")

            elif message == "Thumb_Half-Index_Down-Middle_Down-Ring_Half-Pinky_Up":
                print("q")
                self.temp = "q"
                self.root.after(0, self._update_ui, "q", "Received: q")

            elif message == "Thumb_Down-Index_Up-Middle_Up-Ring_Down-Pinky_Down":
                print("r")
                self.temp = "r"
                self.root.after(0, self._update_ui, "r", "Received: r")

            elif message == "Thumb_Half-Index_Half-Middle_Half-Ring_Down-Pinky_Down":
                print("s")
                self.temp = "s"
                self.root.after(0, self._update_ui, "s", "Received: s")

            elif message == "Thumb_Up-Index_Half-Middle_Down-Ring_Down-Pinky_Down":
                print("t")
                self.temp = "t"
                self.root.after(0, self._update_ui, "t", "Received: t")

            elif message == "Thumb_Half-Index_Up-Middle_Up-Ring_Down-Pinky_Down":
                print("u")
                self.temp = "u"
                self.root.after(0, self._update_ui, "u", "Received: u")

            elif message == "Thumb_Up-Index_Down-Middle_Up-Ring_Down-Pinky_Up":
                print("v")
                self.temp = "v"
                self.root.after(0, self._update_ui, "v", "Received: v")

            elif message == "Thumb_Half-Index_Up-Middle_Up-Ring_Up-Pinky_Down":
                print("w")
                self.temp = "w"
                self.root.after(0, self._update_ui, "w", "Received: w")

            elif message == "Thumb_Half-Index_Half-Middle_Down-Ring_Down-Pinky_Down":
                print("x")
                self.temp = "x"
                self.root.after(0, self._update_ui, "x", "Received: x")

            elif message == "Thumb_Up-Index_Up-Middle_Down-Ring_Down-Pinky_Up":
                print("y")
                self.temp = "y"
                self.root.after(0, self._update_ui, "y", "Received: y")

            elif message == "Thumb_Up-Index_Up-Middle_Up-Ring_Down-Pinky_Up":
                print("z")
                self.temp = "z"
                self.root.after(0, self._update_ui, "z", "Received: z")

            # -------------------------------------------------
            # Space
            # -------------------------------------------------

            elif message == "space":
                print("SPACE")
                self.word += " "
                self.root.after(0, self._update_ui, "␣", "SPACE")

            # -------------------------------------------------
            # Add current letter to word
            # -------------------------------------------------

            elif message == "next":
                if self.temp:
                    self.word += self.temp
                    print("Word:", self.word)
                    self.root.after(0, self._update_ui, None, f"Word: {self.word}")

            # -------------------------------------------------
            # Backspace
            # -------------------------------------------------

            elif message == "back-space":
                self.word = self.word[:-1]
                print("Word:", self.word)
                self.root.after(0, self._update_ui, "⌫", f"Backspace → Word: {self.word}")

            # -------------------------------------------------
            # Speak
            # -------------------------------------------------

            elif message == ".":
                print("Speak:", self.word)

                if self.word:
                    word_to_speak = self.word
                    self.word = ""
                    self.root.after(0, self._update_ui, "🔊", f"Speaking: {word_to_speak}")
                    speak(word_to_speak)

            else:
                print("Error:", message)
                self.root.after(0, self._update_ui, "?", f"Error: {message}")

    # ---------------------------------------------------------
    # Cleanup on window close
    # ---------------------------------------------------------
    def _on_close(self):
        self.running = False
        self.sock.close()
        disconnect()
        self.root.destroy()


# =============================================================
# Entry Point
# =============================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = SilentVoiceApp(root)
    root.mainloop()
