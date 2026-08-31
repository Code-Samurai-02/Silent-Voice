import network
import time
import urequests

SSID = "SAHIL"
PASSWORD = "12345678"

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)

while not wifi.isconnected():
    print("Connecting...")
    time.sleep(1)

print("ESP32 IP:", wifi.ifconfig()[0])


laptop_ip = "10.32.173.160"

url = "http://" + laptop_ip + ":5000/data"

data = {
    "message": "Hello from ESP32"
}

response = urequests.post(
    url,
    json=data
)