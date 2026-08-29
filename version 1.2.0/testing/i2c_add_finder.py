from machine import I2C, Pin

i2c = I2C(
    0,
    scl=Pin(22),
    sda=Pin(21),
    freq=100000
)

# Select PCA channel 0
i2c.writeto(0x70, b'\x01')

print("Channel 0 selected")
print([hex(x) for x in i2c.scan()])



from machine import Pin, I2C

i2c = I2C(
    0,
    scl=Pin(22),
    sda=Pin(21),
    freq=100000
)

print("I2C scan:")
print([hex(x) for x in i2c.scan()])
