import math

class MPU6050:
    def __init__(self, i2c, addr=0x68):
        self.i2c = i2c
        self.addr = addr
        self.i2c.writeto_mem(self.addr, 0x6B, b'\x00')  # wake up

    def _read_word(self, reg):
        h, l = self.i2c.readfrom_mem(self.addr, reg, 2)
        val = (h << 8) | l
        return val - 65536 if val > 32767 else val

    def get_accel(self):
        return (
            self._read_word(0x3B) / 16384,
            self._read_word(0x3D) / 16384,
            self._read_word(0x3F) / 16384
        )

    def get_gyro(self):
        return (
            self._read_word(0x43) / 131,
            self._read_word(0x45) / 131,
            self._read_word(0x47) / 131
        )
