import serial
import keyboard
import time

# CHANGE COM PORT
# Windows example: "COM5"
# Linux example: "/dev/ttyUSB0"
# Mac example: "/dev/cu.usbserial-xxxx"

ser = serial.Serial("COM3", 115200, timeout=1)

print("Listening...")
temp = ""
while True:
    if ser.in_waiting:
        data = ser.readline().decode().strip()
        if data == "Error":
            continue
        if data:
            print("Received:", data)
            if keyboard.is_pressed('a'):
                temp = temp + data
                time.sleep(0.3)
            elif keyboard.is_pressed('s'):
                temp = temp + " "
                time.sleep(0.3)
            elif keyboard.is_pressed('d'):
                temp = temp + "."
                print(temp)
                break
            