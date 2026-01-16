from machine import I2C
import time
import math

class MPU6050:
    # MPU6050 Registers
    PWR_MGMT_1   = 0x6B
    SMPLRT_DIV   = 0x19
    CONFIG       = 0x1A
    GYRO_CONFIG  = 0x1B
    ACCEL_CONFIG = 0x1C

    ACCEL_XOUT_H = 0x3B
    TEMP_OUT_H   = 0x41
    GYRO_XOUT_H  = 0x43

    def __init__(self, i2c, addr=0x68):
        self.i2c = i2c
        self.addr = addr
        self._init_sensor()

    def _write_reg(self, reg, data):
        self.i2c.writeto_mem(self.addr, reg, bytes([data]))

    def _read_reg(self, reg, nbytes=1):
        return self.i2c.readfrom_mem(self.addr, reg, nbytes)

    def _init_sensor(self):
        self._write_reg(self.PWR_MGMT_1, 0x00)  # Wake up
        time.sleep_ms(100)
        self._write_reg(self.SMPLRT_DIV, 0x07)
        self._write_reg(self.CONFIG, 0x00)
        self._write_reg(self.GYRO_CONFIG, 0x00)   # ±250 °/s
        self._write_reg(self.ACCEL_CONFIG, 0x00)  # ±2g

    def _read_raw(self, reg):
        data = self._read_reg(reg, 2)
        value = (data[0] << 8) | data[1]
        if value > 32767:
            value -= 65536
        return value

    def get_accel_raw(self):
        return (
            self._read_raw(self.ACCEL_XOUT_H),
            self._read_raw(self.ACCEL_XOUT_H + 2),
            self._read_raw(self.ACCEL_XOUT_H + 4)
        )

    def get_gyro_raw(self):
        return (
            self._read_raw(self.GYRO_XOUT_H),
            self._read_raw(self.GYRO_XOUT_H + 2),
            self._read_raw(self.GYRO_XOUT_H + 4)
        )

    def get_accel(self):
        ax, ay, az = self.get_accel_raw()
        return (
            ax / 16384.0,
            ay / 16384.0,
            az / 16384.0
        )

    def get_gyro(self):
        gx, gy, gz = self.get_gyro_raw()
        return (
            gx / 131.0,
            gy / 131.0,
            gz / 131.0
        )

    def get_temperature(self):
        temp_raw = self._read_raw(self.TEMP_OUT_H)
        return (temp_raw / 340.0) + 36.53
