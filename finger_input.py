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

ax, ay, az = mpu.get_accel()

#min
x_min = ax
#max
x_max = ax


# ------------------------
# MAIN LOOP
# ------------------------
while True:
    ax, ay, az = mpu.get_accel()
    if ax > x_max :
        x_max = ax
    elif ax < x_min :
        x_min = ax
    print("ACCEL -> X:{:.2f}".format(ax))
    print("----------------------------------")
    print(f"MAX -> x : {x_max}")
    print(f"MIN -> x : {x_min}")
    

    time.sleep(0.2)

