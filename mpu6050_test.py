from machine import I2C, Pin
from time import ticks_ms, sleep
from mpu6050 import MPU6050
from imu import IMU

# Initialize once (IMPORTANT: move outside loop)
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
mpu = MPU6050(i2c)
imu = IMU(mpu)

last = ticks_ms()

print("time,roll,pitch")  # CSV header

while True:
    try:
        now = ticks_ms()
        dt = (now - last) / 1000
        last = now

        roll, pitch = imu.orientation(dt)

        # Send CSV format
        print(f"{now},{roll},{pitch}")

        sleep(0.02)

    except Exception as e:
        print("Error:", e)