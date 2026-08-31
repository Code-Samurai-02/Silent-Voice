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

    print("Channel", channel, "scan:", [hex(x) for x in i2c.scan()])

    mpus[channel].begin()

    time.sleep_ms(50)

    print("MPU", channel + 1, "initialized")


# =========================
# AX for all fingers
# =========================

finger_ax = [0.0, 0.0, 0.0, 0.0, 0.0]

# =========================
# Main Loop
# =========================
while True:

    for channel in range(5):

        # Select PCA9548A channel
        select_channel(channel)

        # Read accelerometer
        ax, ay, az = mpus[channel].get_accel()
        finger_ax[channel] = ax
        
        print("-----------------------------")
        if(finger_ax[0] > 0.55):
            print("Thumb Up")
        elif(finger_ax[0] < 0.55 and finger_ax[0] > 0):
            print("Thumb Half")
        elif(finger_ax[0] < 0):
            print("Thumb Down")
        else:
            print("Thumb Error")
            
            
            print("-----------------------------")
        if(finger_ax[1] > 0.55):
            print("Index Up")
        elif(finger_ax[1] < 0.55 and finger_ax[1] > -0.55):
            print("Index Half")
        elif(finger_ax[1] < -0.55):
            print("Index Down")
        else:
            print("Index Error")
        
        
        
        print("-----------------------------")
        if(finger_ax[2] > 0.55):
            print("Middle Up")
        elif(finger_ax[2] < 0.55 and finger_ax[2] > -0.45):
            print("Middle Half")
        elif(finger_ax[2] < -0.45):
            print("Middle Down")
        else:
            print("Middle Error")
        
        
        print("-----------------------------")
        if(finger_ax[3] > 0.55):
            print("Ring Up")
        elif(finger_ax[3] < 0.55 and finger_ax[3] > -0.45):
            print("Ring Half")
        elif(finger_ax[3] < -0.45):
            print("Ring Down")
        else:
            print("Ring Error")
            
            
            
        print("-----------------------------")
        if(finger_ax[4] > 0.65):
            print("Pinky Up")
        elif(finger_ax[4] < 0.65 and finger_ax[4] > -0.15):
            print("Pinky Half")
        elif(finger_ax[4] < -0.15):
            print("Pinky Down")
        else:
            print("Pinky Error")
    time.sleep_ms(100)


#working full hand prototype all finger