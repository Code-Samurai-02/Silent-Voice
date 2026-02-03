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

while True:
    send_message("Hello from the ESP32!")
    time.sleep(5)