import network
import time
from machine import I2C, Pin
from mpu6050 import MPU6050
import socket


#button 
space_button = Pin(26, Pin.IN, Pin.PULL_UP)
next_button = Pin(27, Pin.IN, Pin.PULL_UP)
stop_button = Pin(12, Pin.IN, Pin.PULL_UP)
back_space_button = Pin(13, Pin.IN, Pin.PULL_UP)

#wifi info

SSID = "SAHIL"
PASSWORD = "12345678"

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)

#wifi led
led = Pin(2, Pin.OUT)
#trying to connect until connected 
while not wifi.isconnected():
    print("Connecting...")
    time.sleep(1)

led.value(1)
print("ESP32 IP:", wifi.ifconfig()[0])

#reciver info



laptop_ip = "10.162.164.159"
laptop_port = 5001

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
data = {
    "message": "Hello from ESP32"
}

# =========================
# ESP32 I2C
# =========================
i2c = I2C(
    0,
    scl=Pin(22),
    sda=Pin(21),
    freq=400000
)

PCA_ADDR = 0x70
MPU_ADDR = 0x68


# =========================
# PCA9548A
# =========================
def select_channel(channel):
    i2c.writeto(PCA_ADDR, bytes([1 << channel]))
    time.sleep_ms(2)


# =========================
# Create MPU6050 objects
# =========================
mpu1_thumb  = MPU6050(i2c, MPU_ADDR)
mpu2_index  = MPU6050(i2c, MPU_ADDR)
mpu3_middle = MPU6050(i2c, MPU_ADDR)
mpu4_ring   = MPU6050(i2c, MPU_ADDR)
mpu5_pinky  = MPU6050(i2c, MPU_ADDR)


# =========================
# Initialize all sensors
# =========================
mpus = [
    mpu1_thumb,
    mpu2_index,
    mpu3_middle,
    mpu4_ring,
    mpu5_pinky
]



for channel in range(5):
    select_channel(channel)
    print("Channel", channel, "scan:", [hex(x) for x in i2c.scan()])
    mpus[channel].begin()
    time.sleep_ms(50)
    print("MPU", channel + 1, "initialized")


# =========================
# AX for all fingers
# =========================

finger_ax = [0.0, 0.0, 0.0, 0.0, 0.0]


while True:
    if space_button.value() == 0:   # Button pressed
        temp = "space"
        print(temp)
        sock.sendto(temp.encode(), (laptop_ip, laptop_port))
        time.sleep_ms(1000)
        continue
    elif next_button.value() == 0:   # Button pressed
        temp = "next"
        print(temp)
        sock.sendto(temp.encode(), (laptop_ip, laptop_port))
        time.sleep_ms(1000)
        continue
    elif stop_button.value() == 0:   # Button pressed
        temp = "."
        print(temp)
        sock.sendto(temp.encode(), (laptop_ip, laptop_port))
        time.sleep_ms(1000)
        continue
    elif back_space_button.value() == 0:   # Button pressed
        temp = "back-space"
        print(temp)
        sock.sendto(temp.encode(), (laptop_ip, laptop_port))
        time.sleep_ms(1000)
        continue
    temp = ""
    for channel in range(5):
        
        # Select PCA9548A channel
        select_channel(channel)

        # Read accelerometer
        ax, ay, az = mpus[channel].get_accel()
        finger_ax[channel] = ax
    print("-----------------------------")
    if(finger_ax[0] > 0.65):
        print("Thumb_Up")
        temp = temp + "Thumb_Up"
    elif(finger_ax[0] < 0.65 and finger_ax[0] > 0):
        print("Thumb_Half")
        temp = temp + "Thumb_Half"
    elif(finger_ax[0] < 0):
        print("Thumb_Down")
        temp = temp + "Thumb_Down"
    else:
        print("Thumb_Error")
        temp = temp + "Thumb_Error"
                
    temp = temp + "-"
    print("-----------------------------")
    if(finger_ax[1] > 0.55):
        print("Index_Up")
        temp = temp + "Index_Up"
    elif(finger_ax[1] < 0.55 and finger_ax[1] > -0.55):
        print("Index_Half")
        temp = temp + "Index_Half"
    elif(finger_ax[1] < -0.55):
        print("Index_Down")
        temp = temp + "Index_Down"
    else:
        print("Index_Error")
        temp = temp + "Index_Error"
            
    temp = temp + "-"
    print("-----------------------------")
    if(finger_ax[2] > 0.55):
        print("Middle_Up")
        temp = temp + "Middle_Up"
    elif(finger_ax[2] < 0.55 and finger_ax[2] > -0.45):
        print("Middle_Half")
        temp = temp + "Middle_Half"
    elif(finger_ax[2] < -0.45):
        print("Middle_Down")
        temp = temp + "Middle_Down"
    else:
        print("Middle_Error")
        temp = temp + "Middle_Error"
            
    temp = temp + "-"
    print("-----------------------------")
    if(finger_ax[3] > 0.65):
        print("Ring_Up")
        temp = temp + "Ring_Up"
    elif(finger_ax[3] < 0.65 and finger_ax[3] > -0.45):
        print("Ring_Half")
        temp = temp + "Ring_Half"
    elif(finger_ax[3] < -0.45):
        print("Ring_Down")
        temp = temp + "Ring_Down"
    else:
        print("Ring_Error")
        temp = temp + "Ring_Error"
                
    temp = temp + "-"
    print("-----------------------------")
    if(finger_ax[4] > 0.65):
        print("Pinky_Up")
        temp = temp + "Pinky_Up"
    elif(finger_ax[4] < 0.65 and finger_ax[4] > 0):
        print("Pinky_Half")
        temp = temp + "Pinky_Half"
    elif(finger_ax[4] < 0):
        print("Pinky_Down")
        temp = temp + "Pinky_Down"
    else:
        print("Pinky_Error")
        temp = temp + "Pinky_Error"
        
    # SEND DATA TO LAPTOP
    sock.sendto(temp.encode(), (laptop_ip, laptop_port))
    time.sleep_ms(10)

