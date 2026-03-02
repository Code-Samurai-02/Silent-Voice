from machine import I2C, Pin
from time import sleep, ticks_ms
from mpu6050 import MPU6050
from imu import IMU

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
TCA_ADDR = 0x70

def tca_select(channel):
    i2c.writeto(TCA_ADDR, bytearray([1 << channel]))

# ---------- Safe Read Function ----------
def safe_accel(imu_obj, channel, addr):
    try:
        tca_select(channel)
        return imu_obj.accel()
    
    except OSError as e:

        # Try soft recovery
        try:
            sleep(0.01)
            tca_select(channel)
            return imu_obj.accel()
        except:
            pass

            try:
                tca_select(channel)
                mpu = MPU6050(i2c, addr=addr)
                imu_new = IMU(mpu)
                return imu_new.accel()
            except:
                return (0, 0, 0)

# ---------- Initialization ----------
tca_select(0)
imu1 = IMU(MPU6050(i2c, addr=0x69))

tca_select(1)
imu2 = IMU(MPU6050(i2c, addr=0x68))

tca_select(2)
imu3 = IMU(MPU6050(i2c, addr=0x68))

tca_select(3)
imu4 = IMU(MPU6050(i2c, addr=0x68))

tca_select(4)
imu5 = IMU(MPU6050(i2c, addr=0x68))


a = 0
# ---------- Main Loop ----------
while True:

    ax1, ay1, az1 = safe_accel(imu1, 0, 0x68)
    ax2, ay2, az2 = safe_accel(imu2, 1, 0x69)
    ax3, ay3, az3 = safe_accel(imu3, 2, 0x68)
    ax4, ay4, az4 = safe_accel(imu4, 3, 0x69)
    ax5, ay5, az5 = safe_accel(imu5, 3, 0x69)
    
    if(ax1 == 0 or ay1 == 0 or az1 == 0 or ax2 == 0 or ay2 == 0 or az2 == 0 or ax3 == 0 or ay3 == 0 or az3 == 0 or ax4 == 0 or ay4 == 0 or az4 == 0 or ax5 == 0 or ay5 == 0 or az5 == 0):
        continue
    print(f"{ax1},{ay1},{az1},{ax2},{ay2},{az2},{ax3},{ay3},{az3},{ax4},{ay4},{az4},{ax5},{ay5},{az5},Z")
    a = a + 1
    if a == 1000 :
        break
    sleep(0.02)
