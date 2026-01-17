from machine import Pin, I2C
from time import sleep
from mpu6050 import MPU6050

# ESP32 default I2C pins
i2c = I2C(0, scl=Pin(22), sda=Pin(21))

mpu = MPU6050(i2c)

while True:
    ax, ay, az = mpu.get_accel()
    gx, gy, gz = mpu.get_gyro()
    roll, pitch = mpu.get_angles()

    print("Accel (g):", ax, ay, az)
    print("Gyro (°/s):", gx, gy, gz)
    print("Roll:", roll, "Pitch:", pitch)
    print("-" * 30)

    sleep(0.5)
