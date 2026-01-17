from machine import I2C, Pin
from time import sleep
from mpu6050 import MPU6050
from imu import IMU

i2c = I2C(0, scl=Pin(22), sda=Pin(21))

mpu = MPU6050(i2c)   # hardware driver
imu = IMU(mpu)      # wrapper

dt = 0.02  # 20 ms loop

while True:
    roll, pitch = imu.orientation(dt)

    print("Roll:", roll, "Pitch:", pitch)

    sleep(dt)
