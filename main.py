from machine import I2C, Pin
from time import ticks_ms, sleep
from mpu6050 import MPU6050
from imu import IMU
from tca9548a import TCA9548A

i2c = I2C(0, scl=Pin(22), sda=Pin(21))
tca = TCA9548A(i2c)

tca.select(0)
mpu = MPU6050(i2c)
imu = IMU(mpu)
ax, ay, az = imu.accel()
x_max = ax
y_max = ay
z_max = az

x_min = ax
y_min = ay
z_min = az

while True:
    tca.select(0)
    ax, ay, az = imu.accel()
    print("X:", ax, "Y:", ay, "Z: ", az)
    # MAX
    if ax > x_max:
        x_max = ax
    if ay > y_max:
        y_max = ay
    if az > z_max:
        z_max = az

    # MIN
    if ax < x_min:
        x_min = ax
    if ay < y_min:
        y_min = ay
    if az < z_min:
        z_min = az

    print("Min -", "X:", x_min, "Y:", y_min, "Z: ", z_min)
    print("Max -", "X:", x_max, "Y:", y_max, "Z: ", z_max)
    sleep(0.2)

