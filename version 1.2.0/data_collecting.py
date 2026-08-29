from machine import I2C, Pin
import time
from mpu6050 import MPU6050

# =========================
# ESP32 I2C
# =========================
i2c = I2C(
    0,
    scl=Pin(22),
    sda=Pin(21),
    freq=400000
)

PCA_ADDR = 0x70
MPU_ADDR = 0x68


# =========================
# PCA9548A
# =========================
def select_channel(channel):
    i2c.writeto(PCA_ADDR, bytes([1 << channel]))
    time.sleep_ms(2)


# =========================
# Create MPU6050 objects
# =========================
mpu1_thumb  = MPU6050(i2c, MPU_ADDR)
mpu2_index  = MPU6050(i2c, MPU_ADDR)
mpu3_middle = MPU6050(i2c, MPU_ADDR)
mpu4_ring   = MPU6050(i2c, MPU_ADDR)
mpu5_pinky  = MPU6050(i2c, MPU_ADDR)


# =========================
# Initialize all sensors
# =========================
mpus = [
    mpu1_thumb,
    mpu2_index,
    mpu3_middle,
    mpu4_ring,
    mpu5_pinky
]

for channel in range(5):

    select_channel(channel)

    # Wake up MPU on this channel
    mpus[channel].i2c.writeto_mem(
        MPU_ADDR,
        0x6B,
        b'\x00'
    )

    time.sleep_ms(50)

    print("MPU", channel + 1, "initialized")


# =========================
# Min / Max for AX
# =========================
min_ax = [0.0] * 5
max_ax = [0.0] * 5
first_read = [True] * 5


# =========================
# Main Loop
# =========================
while True:

    for channel in range(5):

        # Select PCA9548A channel
        select_channel(channel)

        # Read accelerometer
        ax, ay, az = mpus[channel].get_accel()

        # Read gyroscope
        gx, gy, gz = mpus[channel].get_gyro()

        # -------------------------
        # Min / Max AX
        # -------------------------
        if first_read[channel]:

            min_ax[channel] = ax
            max_ax[channel] = ax

            first_read[channel] = False

        if ax < min_ax[channel]:
            min_ax[channel] = ax

        if ax > max_ax[channel]:
            max_ax[channel] = ax


        # -------------------------
        # Print
        # -------------------------
        print(
            "MPU", channel + 1,
            "| AX:", ax,
            "| AY:", ay,
            "| AZ:", az
        )

        print(
            "     GX:", gx,
            "| GY:", gy,
            "| GZ:", gz
        )

        print(
            "     MAX AX:", max_ax[channel],
            "| MIN AX:", min_ax[channel]
        )

        print("-----------------------------")


    time.sleep_ms(100)


#wroking data collecting prototype v1.2