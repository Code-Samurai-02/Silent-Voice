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
        print("Index Up ")
    elif (ax <= index_half_max) and (ax >= index_half_min):
        print("Index Half")
    elif(ax <= index_down_max) and (ax >= index_down_min):
        print("Index Down")
    else:
        print("Error")
    

    time.sleep(0.2)

