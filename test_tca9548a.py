from machine import I2C, Pin
from tca9548a import TCA9548A
import time

# -------- I2C SETUP (adjust pins if needed) --------
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)

print("Base I2C scan:", i2c.scan())

# -------- INIT MULTIPLEXER --------
mux = TCA9548A(i2c)

print("\nTesting TCA9548A channels...\n")

# -------- TEST EACH CHANNEL --------
for ch in range(8):
    try:
        mux.select(ch)
        devices = i2c.scan()
        print("Channel", ch, "-> Devices:", devices)
        time.sleep(0.3)
    except Exception as e:
        print("Channel", ch, "ERROR:", e)

# -------- DISABLE ALL CHANNELS --------
mux.disable()
print("\nAll channels disabled")
