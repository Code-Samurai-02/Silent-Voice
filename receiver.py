import serial

ser = serial.Serial("COM7", 115200, timeout=1)

print("Listening...")

temp = ""              # Final accumulated message
last_letter = None     # Stores last received valid letter

valid_letters = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

while True:
    if ser.in_waiting:
        data = ser.readline().decode().strip()

        if not data or data == "Error":
            continue

        print("Received:", data)

        # If letter received, store it but don't append yet
        if data in valid_letters:
            last_letter = data
            print("Stored:", last_letter)

        # If '*' → confirm and append last stored letter
        elif data == "*":
            if last_letter:
                temp += last_letter
                print("Appended:", last_letter)
                last_letter = None   # optional reset

        # If '.' → print full message
        elif data == ".":
            print("Final Output:", temp)
            break