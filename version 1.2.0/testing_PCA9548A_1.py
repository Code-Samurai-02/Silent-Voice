from machine import I2C, Pin
import time

# ESP32 I2C
i2c = I2C(
    0,
    scl=Pin(22),
    sda=Pin(21),
    freq=400000
)

PCA_ADDR = 0x70
MPU_ADDR = 0x68


# Select PCA9548A channel
def select_channel(channel):
    i2c.writeto(PCA_ADDR, bytes([1 << channel]))


# Initialize MPU6050
def init_mpu():
    # Wake MPU6050
    i2c.writeto_mem(
        MPU_ADDR,
        0x6B,
        b'\x00'
    )

    time.sleep_ms(100)


# Read accelerometer
def read_accel():
    data = i2c.readfrom_mem(
        MPU_ADDR,
        0x3B,
        6
    )

    ax = int.from_bytes(data[0:2], 'big', True)
    ay = int.from_bytes(data[2:4], 'big', True)
    az = int.from_bytes(data[4:6], 'big', True)

    return ax, ay, az


# Read gyroscope
def read_gyro():
    data = i2c.readfrom_mem(
        MPU_ADDR,
        0x43,
        6
    )

    gx = int.from_bytes(data[0:2], 'big', True)
    gy = int.from_bytes(data[2:4], 'big', True)
    gz = int.from_bytes(data[4:6], 'big', True)

    return gx, gy, gz


# Initialize all 5 MPU6050s
for channel in range(5):

    select_channel(channel)

    init_mpu()

    print("MPU", channel + 1, "initialized")


# Continuously read all 5 sensors
while True:

    for channel in range(5):

        # Select sensor
        select_channel(channel)

        # Read data
        accel = read_accel()
        gyro = read_gyro()

        print(
            "MPU{} | ACC: {} | GYRO: {}".format(
                channel + 1,
                accel,
                gyro
            )
        )

    print("-----------------------------")

    time.sleep_ms(100)
    
    #working properly 