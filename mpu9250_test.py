from machine import I2C, Pin
from time import sleep, ticks_ms
from mpu9250 import MPU9250
from imu import IMU

i2c = I2C(0, scl=Pin(12), sda=Pin(13))

mpu = MPU9250(i2c)
imu = IMU(mpu)

last = ticks_ms()

while True:
    now = ticks_ms()
    dt = (now - last) / 1000
    last = now

    roll, pitch = imu.orientation(dt)
    yaw = imu.heading()   # MPU9250-only

    print("Roll:", roll, "Pitch:", pitch, "Yaw:", yaw)

    sleep(0.02)
