from machine import I2C, Pin
from time import sleep, ticks_ms
from tca9548a import TCA9548A
from mpu6050 import MPU6050
from imu import IMU

i2c = I2C(0, scl=Pin(22), sda=Pin(21))
tca = TCA9548A(i2c)

# Init IMU 0
tca.select(0)
mpu0 = MPU6050(i2c)
imu0 = IMU(mpu0)

# Init IMU 1
tca.select(1)
mpu1 = MPU6050(i2c)
imu1 = IMU(mpu1)

last0 = ticks_ms()
last1 = ticks_ms()

while True:
    # ---- IMU 0 ----
    tca.select(0)
    now = ticks_ms()
    dt0 = (now - last0) / 1000
    last0 = now
    r0, p0 = imu0.orientation(dt0)

    # ---- IMU 1 ----
    tca.select(1)
    now = ticks_ms()
    dt1 = (now - last1) / 1000
    last1 = now
    r1, p1 = imu1.orientation(dt1)

    print(f"IMU0 → Roll:{r0:.2f} Pitch:{p0:.2f}")
    print(f"IMU1 → Roll:{r1:.2f} Pitch:{p1:.2f}")
    print("-" * 35)

    sleep(0.02)
