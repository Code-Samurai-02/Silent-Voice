import time
import math

MPU_ADDR = 0x68
MAG_ADDR = 0x0C

class MPU9250:
    def __init__(self, i2c, addr=MPU_ADDR):
        self.i2c = i2c
        self.addr = addr

        self.i2c.writeto_mem(self.addr, 0x6B, b'\x00')
        time.sleep_ms(50)

        self.i2c.writeto_mem(self.addr, 0x37, b'\x02')  # bypass mag
        self.i2c.writeto_mem(MAG_ADDR, 0x0A, b'\x16')   # mag continuous

    def _read_word(self, addr, reg):
        h, l = self.i2c.readfrom_mem(addr, reg, 2)
        val = (h << 8) | l
        return val - 65536 if val > 32767 else val

    def get_accel(self):
        return (
            self._read_word(self.addr, 0x3B) / 16384,
            self._read_word(self.addr, 0x3D) / 16384,
            self._read_word(self.addr, 0x3F) / 16384
        )

    def get_gyro(self):
        return (
            self._read_word(self.addr, 0x43) / 131,
            self._read_word(self.addr, 0x45) / 131,
            self._read_word(self.addr, 0x47) / 131
        )

    def get_mag(self):
        data = self.i2c.readfrom_mem(MAG_ADDR, 0x03, 7)
        mx = (data[1] << 8) | data[0]
        my = (data[3] << 8) | data[2]
        mz = (data[5] << 8) | data[4]
        return (
            mx - 65536 if mx > 32767 else mx,
            my - 65536 if my > 32767 else my,
            mz - 65536 if mz > 32767 else mz
        )
