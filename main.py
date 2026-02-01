from machine import Pin, I2C
import time

from mpu6050 import MPU6050
from imu import IMU

# -------------------------
# I2C CONFIGURATION
# -------------------------
# ESP32 Default Pins
# SDA -> GPIO21
# SCL -> GPIO22

i2c = I2C(
    0,
    scl=Pin(22),
    sda=Pin(21),
    freq=400000
)

# Scan I2C bus
devices = i2c.scan()
print("I2C Devices:", devices)

if 0x68 not in devices:
    raise RuntimeError("MPU6050 not found")

# -------------------------
# SENSOR INIT
# -------------------------
mpu = MPU6050(i2c)
imu = IMU(mpu)

# -------------------------
# LOOP VARIABLES
# -------------------------
last_time = time.ticks_ms()

#MAX
x_max, y_max, z_max = imu.accel()

#MIN
x_min, y_min, z_min = imu.accel()



# -------------------------
# MAIN LOOP
# -------------------------
while True:
    now = time.ticks_ms()
    dt = time.ticks_diff(now, last_time) / 1000
    last_time = now

    ax, ay, az = imu.accel()
    gx, gy, gz = imu.gyro()
    if (ax > x_max):
      x_max = ax
    elif(ax < x_min):
      x_min = ax
    if (ay > y_max):
      y_max = ay
    elif(ay < y_min):
      y_min = ay
    if (az > z_max):
      z_max = az
    elif(az < z_min):
      z_min = az
    
    
    roll, pitch = imu.orientation(dt)

    print("ACCEL:", ax, ay, az)
    print("GYRO :", gx, gy, gz)
    print("ROLL :", roll, "PITCH:", pitch)
    print("----------------------")
    ptint(f"Max - x : ({x_max}), y : ({y_max}), z : ({z_max})")
    ptint(f"Min - x : ({x_min}), y : ({y_min}), z : ({z_min})")
    

    time.sleep(0.05)
