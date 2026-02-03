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

thumb_up_max = 1.1
thumb_up_min = 0.75

thumb_half_max = 0.7
thumb_half_min = 0.15

thumb_down_max = 0.1
thumb_down_min = -0.4



# ------------------------
# MAIN LOOP
# ------------------------
while True:
    ax, ay, az = mpu.get_accel()
    if (ax <= thumb_up_max) and (ax >= thumb_up_min):
        print("thumb Up ")
    elif (ax <= thumb_half_max) and (ax >= thumb_half_min):
        print("thumb Half")
    elif(ax <= thumb_down_max) and (ax >= thumb_down_min):
        print("thumb Down")
    else:
        print("Error")
    

    time.sleep(0.2)


