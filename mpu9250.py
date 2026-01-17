from machine import I2C, Pin
from time import sleep
from imu import MPU9250

# ESP32 I2C pins
i2c = I2C(0, scl=Pin(22), sda=Pin(21))

imu = MPU9250(i2c)

while True:
    ax, ay, az = imu.get_accel()
    gx, gy, gz = imu.get_gyro()
    mx, my, mz = imu.get_mag()
    roll, pitch, yaw = imu.get_orientation()

    print("Accel:", ax, ay, az)
    print("Gyro :", gx, gy, gz)
    print("Mag  :", mx, my, mz)
    print("RPY  :", roll, pitch, yaw)
    print("-" * 30)

    sleep(0.5)
