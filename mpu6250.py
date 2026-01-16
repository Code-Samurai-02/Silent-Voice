from machine import I2C
import time
import math

class MPU9250:
    MPU_ADDR = 0x68
    MAG_ADDR = 0x0C

    PWR_MGMT_1 = 0x6B
    ACCEL_CONFIG = 0x1C
    GYRO_CONFIG = 0x1B
    ACCEL_XOUT_H = 0x3B
    TEMP_OUT_H = 0x41
    GYRO_XOUT_H = 0x43

    INT_PIN_CFG = 0x37
    USER_CTRL = 0x6A

    # Magnetometer registers (AK8963)
    AK8963_CNTL1 = 0x0A
    AK8963_XOUT_L = 0x03

    def __init__(self, i2c, addr=MPU_ADDR):
        self.i2c = i2c
        self.addr = addr
        self._init_mpu()
        self._init_mag()

    def _write(self, reg, val):
        self.i2c.writeto_mem(self.addr, reg, bytes([val]))

    def _read(self, reg, n=1):
        return self.i2c.readfrom_mem(self.addr, reg, n)

    def _read_raw(self, reg):
        data = self._read(reg, 2)
        val = (data[0] << 8) | data[1]
        if val > 32767:
            val -= 65536
        return val

    def _init_mpu(self):
        self._write(self.PWR_MGMT_1, 0x00)
        time.sleep_ms(100)
        self._write(self.ACCEL_CONFIG, 0x00)  # ±2g
        self._write(self.GYRO_CONFIG, 0x00)   # ±250 dps
        self._write(self.INT_PIN_CFG, 0x02)   # Enable bypass for magnetometer

    def _init_mag(self):
        self.i2c.writeto_mem(self.MAG_ADDR, self.AK8963_CNTL1, b'\x00')
        time.sleep_ms(10)
        self.i2c.writeto_mem(self.MAG_ADDR, self.AK8963_CNTL1, b'\x16')  # Continuous, 16-bit
        time.sleep_ms(10)

    # -------- ACCEL --------
    def accel(self):
        ax = self._read_raw(self.ACCEL_XOUT_H) / 16384.0
        ay = self._read_raw(self.ACCEL_XOUT_H + 2) / 16384.0
        az = self._read_raw(self.ACCEL_XOUT_H + 4) / 16384.0
        return ax, ay, az

    # -------- GYRO --------
    def gyro(self):
        gx = self._read_raw(self.GYRO_XOUT_H) / 131.0
        gy = self._read_raw(self.GYRO_XOUT_H + 2) / 131.0
        gz = self._read_raw(self.GYRO_XOUT_H + 4) / 131.0
        return gx, gy, gz

    # -------- TEMP --------
    def temperature(self):
        raw = self._read_raw(self.TEMP_OUT_H)
        return (raw / 333.87) + 21.0

    # -------- MAG --------
    def magnet(self):
        data = self.i2c.readfrom_mem(self.MAG_ADDR, self.AK8963_XOUT_L, 7)
        x = (data[1] << 8) | data[0]
        y = (data[3] << 8) | data[2]
        z = (data[5] << 8) | data[4]

        if x > 32767: x -= 65536
        if y > 32767: y -= 65536
        if z > 32767: z -= 65536

        return x, y, z
