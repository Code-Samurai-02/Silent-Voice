import serial
import time
import middleware
ser = serial.Serial("COM5", 115200, timeout=1)

print("Listening...")
last_star_time = 0
STAR_DEBOUNCE_MS = 500
temp = ""              # Final accumulated message
last_letter = None     # Stores last received valid letter

valid_letters = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

while True:
    if ser.in_waiting:
        data = ser.readline().decode(errors="ignore")
        data = data.replace("\r", "").replace("\n", "")

        if not data or data == "Error":
            continue

        print("Received:", data)

        # If letter received, store it but don't append yet
        if data in valid_letters:
            last_letter = data
            print("Stored:", last_letter)

        # If '*' → confirm and append last stored letter
        elif data == " ":
            temp += " "
            time.sleep(1)
        elif data == "*":
            current_time = time.time() * 1000

            if (current_time - last_star_time) < STAR_DEBOUNCE_MS:
                continue  # ignore repeated star

            last_star_time = current_time

            if last_letter:
                temp += last_letter
                print("Appended:", last_letter)
                last_letter = None
            time.sleep(1)

        # If '.' → print full message
        elif data == ".":
            print("Final Output:", temp)
            middleware.send_text(str(temp))
            time.sleep(1.5)
            temp = ""
            last_letter = ""
            continue