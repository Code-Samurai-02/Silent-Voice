import websocket
import serial
import time

ws = websocket.WebSocket()
ws.connect("ws://localhost:3000")

ser = serial.Serial("COM3",115200,timeout=1)

print("Listening...")

last_star_time = 0
STAR_DEBOUNCE_MS = 500
temp = ""
last_letter = None

valid_letters = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

while True:

    if ser.in_waiting:

        data = ser.readline().decode(errors="ignore")
        data = data.replace("\r","").replace("\n","")

        if not data:
            continue

        msg = f"Received: {data}"
        print(msg)
        ws.send(msg)

        if data in valid_letters:

            last_letter = data
            msg = f"Stored: {last_letter}"
            print(msg)
            ws.send(msg)

        elif data == " ":
            temp += " "
            ws.send("Space added")

        elif data == "*":

            current_time = time.time()*1000

            if (current_time-last_star_time) < STAR_DEBOUNCE_MS:
                continue

            last_star_time = current_time

            if last_letter:
                temp += last_letter
                msg = f"Appended: {last_letter}"
                print(msg)
                ws.send(msg)
                last_letter = None

        elif data == ".":

            msg = f"Final Output: {temp}"
            print(msg)
            ws.send(msg)

            temp=""
