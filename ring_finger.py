from machine import Pin, I2C
import time
from mpu6050 import MPU6050

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

ring_up_max = 1.1
ring_up_min = 0.75

ring_half_max = 0.45
ring_half_min = -0.4

ring_down_max = -0.5
ring_down_min = -1.1



# ------------------------
# MAIN LOOP
# ------------------------
while True:
    ax, ay, az = mpu.get_accel()
    if (ax <= ring_up_max) and (ax >= ring_up_min):
        print("ring Up ")
    elif (ax <= ring_half_max) and (ax >= ring_half_min):
        print("ring Half")
    elif(ax <= ring_down_max) and (ax >= ring_down_min):
        print("ring Down")
    else:
        print("Error")
    

    time.sleep(0.2)


