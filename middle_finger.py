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

middle_up_max = 1.1
middle_up_min = 0.75

middle_half_max = 0.45
middle_half_min = -0.4

middle_down_max = -0.5
middle_down_min = -1.1



# ------------------------
# MAIN LOOP
# ------------------------
while True:
    ax, ay, az = mpu.get_accel()
    if (ax <= middle_up_max) and (ax >= middle_up_min):
        print("middle Up ")
    elif (ax <= middle_half_max) and (ax >= middle_half_min):
        print("middle Half")
    elif(ax <= middle_down_max) and (ax >= middle_down_min):
        print("middle Down")
    else:
        print("Error")
    

    time.sleep(0.2)


