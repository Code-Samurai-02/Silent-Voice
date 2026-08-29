from machine import Pin, I2C
import time
from mpu6050 import MPU6050
import network
import socket



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

index_up_max = 1.1
index_up_min = 0.7

index_half_max = 0.65
index_half_min = -0.6

index_down_max = -0.61
index_down_min = -1.1



# ------------------------
# MAIN LOOP
# ------------------------
while True:
    ax, ay, az = mpu.get_accel()
    if (ax <= index_up_max) and (ax >= index_up_min):
        print("Index Up")
        send_message("Index Up")
    elif (ax <= index_half_max) and (ax >= index_half_min):
        print("Index Half")
        send_message("Index Half")
    elif(ax <= index_down_max) and (ax >= index_down_min):
        print("Index Down")
        send_message("Index Down")
    else:
        print("Error")
        send_message("Index Error")
    

    time.sleep(0.2)


