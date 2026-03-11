import serial
import time
import middleware
import middleware_hi


while True:
    lan = int(input("Choose your language(1/2): 1.English, 2.Hindi : "))
    if lan ==1 or lan == 2:
        print("Langauge", lan)
        break
    else:
        print("Wrong input")
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
        elif data == "#":
            #backspace functionality
            if temp:
                temp = temp[:-1]
                print("Backspace: Current message:", temp)
                time.sleep(1)

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
            if (lan == 1):
                middleware.send_text(str(temp))
            elif (lan == 2): 
                middleware_hi.send_text(str(temp))
            time.sleep(1.5)
            temp = ""
            last_letter = ""
            continue