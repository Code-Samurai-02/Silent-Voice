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

letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

i = 0
temp_char = letters[0]

while True:
    temp_char = letters[i]
    if ser.in_waiting:
        data = ser.readline().decode(errors="ignore")
        data = data.replace("\r", "").replace("\n", "")

        if not data or data == "Error":
            continue

        
        print(temp_char, "Received:", data)
        # If letter received, store it but don't append yet
        if data in valid_letters:
            last_letter = data
            print("Stored:", last_letter)
            if last_letter == temp_char:
                print("Ok Next")
                i +=1
    time.sleep(1)
