class TCA9548A:
    """
    MicroPython driver for TCA9548A / PCA9548A I2C multiplexer
    """

    def __init__(self, i2c, addr=0x70):
        self.i2c = i2c
        self.addr = addr

    def select(self, channel):
        if channel < 0 or channel > 7:
            raise ValueError("Channel must be 0–7")
        self.i2c.writeto(self.addr, bytes([1 << channel]))

    def disable(self):
        self.i2c.writeto(self.addr, b'\x00')

    def scan(self, channel):
        self.select(channel)
        return self.i2c.scan()

    def scan_all(self):
        devices = {}
        for ch in range(8):
            self.select(ch)
            devices[ch] = self.i2c.scan()
        self.disable()
        return devices
