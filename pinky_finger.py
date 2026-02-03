from machine import Pin, I2C
import time
from mpu6050 import MPU6050
import network
import socket
import time

# 1. Connect to Wi-Fi
ssid = 'Airtel_AIRTEL'
password = 'Airtel@2007'
pi_ip = '192.168.1.8'  # Change to your Pi's actual IP
port = 5000

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

print("Connecting to WiFi...")
while not wlan.isconnected():
    time.sleep(1)

print("Connected! IP:", wlan.ifconfig()[0])

# 2. Send the string
def send_message(message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    sock.sendto(message.encode(), (pi_ip, port))
    print(f"Sent: {message}")
# ------------------------
# I2C SETUP (ESP32)
# ------------------------
i2c = I2C(0, scl=Pin(15), sda=Pin(4), freq=400000)

print("Scanning I2C...")
devices = i2c.scan()
print("Devices:", devices)

if 0x68 not in devices:
    raise Exception("MPU6050 not found")

mpu = MPU6050(i2c)

print("MPU6050 Ready")

pinky_up_max = 1.1
pinky_up_min = 0.75

pinky_half_max = 0.45
pinky_half_min = -0.3

pinky_down_max = -0.4
pinky_down_min = -1.1



# ------------------------
# MAIN LOOP
# ------------------------
while True:
    ax, ay, az = mpu.get_accel()
    if (ax <= pinky_up_max) and (ax >= pinky_up_min):
        print("Pinky Up ")
        send_message("Pinky Up")
    elif (ax <= pinky_half_max) and (ax >= pinky_half_min):
        print("Pinky Half")
        send_message("Pinky Half")
    elif(ax <= pinky_down_max) and (ax >= pinky_down_min):
        print("Pinky Down")
        send_message("Pinky Down")
    else:
        print("Error")
    

    time.sleep(0.2)


