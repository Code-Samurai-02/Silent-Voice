import socket
from tts.tts_client import connect, speak, disconnect

# -----------------------------
# UDP
# -----------------------------
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 5001))

print("UDP server listening...")

# -----------------------------
# TTS
# -----------------------------
connect()

# -----------------------------
# Variables MUST be outside loop
# -----------------------------
temp = ""
word = ""


while True:
    data, addr = sock.recvfrom(1024)

    message = data.decode().strip()

    print("Received:", message)

    # -----------------------------
    # Letters
    # -----------------------------

    if message == "Thumb_Up-Index_Down-Middle_Down-Ring_Down-Pinky_Down":
        print("a")
        temp = "a"

    elif message == "Thumb_Half-Index_Up-Middle_Up-Ring_Up-Pinky_Up":
        print("b")
        temp = "b"

    elif message == "Thumb_Up-Index_Half-Middle_Half-Ring_Half-Pinky_Half":
        print("c")
        temp = "c"

    elif message == "Thumb_Half-Index_Up-Middle_Down-Ring_Down-Pinky_Down":
        print("d")
        temp = "d"

    elif message == "Thumb_Half-Index_Half-Middle_Half-Ring_Half-Pinky_Half":
        print("e")
        temp = "e"

    elif message == "Thumb_Half-Index_Half-Middle_Up-Ring_Up-Pinky_Up":
        print("f")
        temp = "f"

    elif message == "Thumb_Up-Index_Down-Middle_Down-Ring_Half-Pinky_Up":
        print("g")
        temp = "g"

    elif message == "Thumb_Down-Index_Half-Middle_Half-Ring_Down-Pinky_Down":
        print("h")
        temp = "h"

    elif message == "Thumb_Up-Index_Down-Middle_Down-Ring_Down-Pinky_Up":
        print("i")
        temp = "i"

    elif message == "Thumb_Up-Index_Down-Middle_Half-Ring_Half-Pinky_Up":
        print("j")
        temp = "j"

    elif message == "Thumb_Up-Index_Up-Middle_Up-Ring_Down-Pinky_Down":
        print("k")
        temp = "k"

    elif message == "Thumb_Up-Index_Up-Middle_Down-Ring_Down-Pinky_Down":
        print("l")
        temp = "l"

    elif message == "Thumb_Half-Index_Up-Middle_Up-Ring_Down-Pinky_Up":
        print("m")
        temp = "m"

    elif message == "Thumb_Half-Index_Up-Middle_Down-Ring_Half-Pinky_Up":
        print("n")
        temp = "n"

    elif message == "Thumb_Down-Index_Down-Middle_Down-Ring_Down-Pinky_Up":
        print("o")
        temp = "o"

    elif message == "Thumb_Up-Index_Up-Middle_Down-Ring_Half-Pinky_Up":
        print("p")
        temp = "p"

    elif message == "Thumb_Half-Index_Down-Middle_Down-Ring_Half-Pinky_Up":
        print("q")
        temp = "q"

    elif message == "Thumb_Down-Index_Up-Middle_Up-Ring_Down-Pinky_Down":
        print("r")
        temp = "r"

    elif message == "Thumb_Half-Index_Half-Middle_Half-Ring_Down-Pinky_Down":
        print("s")
        temp = "s"

    elif message == "Thumb_Up-Index_Half-Middle_Down-Ring_Down-Pinky_Down":
        print("t")
        temp = "t"

    elif message == "Thumb_Half-Index_Up-Middle_Up-Ring_Down-Pinky_Down":
        print("u")
        temp = "u"

    elif message == "Thumb_Up-Index_Down-Middle_Up-Ring_Down-Pinky_Up":
        print("v")
        temp = "v"

    elif message == "Thumb_Half-Index_Up-Middle_Up-Ring_Up-Pinky_Down":
        print("w")
        temp = "w"

    elif message == "Thumb_Half-Index_Half-Middle_Down-Ring_Down-Pinky_Down":
        print("x")
        temp = "x"

    elif message == "Thumb_Up-Index_Up-Middle_Down-Ring_Down-Pinky_Up":
        print("y")
        temp = "y"

    elif message == "Thumb_Up-Index_Up-Middle_Up-Ring_Down-Pinky_Up":
        print("z")
        temp = "z"

    # -----------------------------
    # Space
    # -----------------------------

    elif message == "space":
        print("SPACE")
        word += " "

    # -----------------------------
    # Add current letter to word
    # -----------------------------

    elif message == "next":
        if temp:
            word += temp
            print("Word:", word)

    # -----------------------------
    # Backspace
    # -----------------------------

    elif message == "back-space":
        word = word[:-1]
        print("Word:", word)

    # -----------------------------
    # Speak
    # -----------------------------

    elif message == ".":
        print("Speak:", word)

        if word:
            speak(word)
            word = ""

    else:
        print("Error:", message)