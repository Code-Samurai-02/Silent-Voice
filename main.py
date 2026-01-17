from machine import I2C, Pin
from time import sleep, ticks_ms
from tca9548a import TCA9548A
from mpu6050 import MPU6050
from imu import IMU

i2c = I2C(0, scl=Pin(22), sda=Pin(21))
tca = TCA9548A(i2c)

# thumb 0
tca.select(0)
