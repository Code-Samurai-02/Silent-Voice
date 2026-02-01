from machine import Pin, I2C
import time
from mpu6050 import MPU6050
from imu import IMU

# -------------------------
# I2C SETUP
# -------------------------
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)

devices = i2c.scan()
print("I2C Devices:", devices)

if 0x68 not in devices:
    raise RuntimeError("MPU6050 not found")

mpu = MPU6050(i2c)
imu = IMU(mpu)

# -------------------------
# WARM UP SENSOR
# -------------------------
print("Warming up...")
for _ in range(100):
    imu.accel()
    time.sleep_ms(5)

x_max, y_max, z_max = imu.accel()
x_min, y_min, z_min = imu.accel()

last_time = time.ticks_ms()

DEADBAND = 0.002

# -------------------------
# LOOP
# -------------------------
while True:
    now = time.ticks_ms()
    dt = time.ticks_diff(now, last_time) / 1000
    last_time = now

    ax, ay, az = imu.accel()
    gx, gy, gz = imu.gyro()

    # ----- MIN MAX UPDATE -----
    if ax > x_max + DEADBAND:
        x_max = ax
    elif ax < x_min - DEADBAND:
        x_min = ax

    if ay > y_max + DEADBAND:
        y_max = ay
    elif ay < y_min - DEADBAND:
        y_min = ay

    if az > z_max + DEADBAND:
        z_max = az
    elif az < z_min - DEADBAND:
        z_min = az

    roll, pitch = imu.orientation(dt)

    print("ACCEL:", ax, ay, az)
    print("GYRO :", gx, gy, gz)
    print("ROLL :", roll, "PITCH:", pitch)
    print(f"MAX  -> X:{x_max:.3f} Y:{y_max:.3f} Z:{z_max:.3f}")
    print(f"MIN  -> X:{x_min:.3f} Y:{y_min:.3f} Z:{z_min:.3f}")
    print("--------------------------------")

    time.sleep_ms(20)
