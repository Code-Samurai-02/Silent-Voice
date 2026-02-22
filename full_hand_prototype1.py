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


thumb_up_max = 1.1
thumb_up_min = 0.75

thumb_half_max = 0.7
thumb_half_min = -0.2

thumb_down_max = -0.3
thumb_down_min = -1.1

index_up_max = 1.1
index_up_min = 0.7

index_half_max = 0.65
index_half_min = -0.6

index_down_max = -0.61
index_down_min = -1.1

middle_up_max = 1.1
middle_up_min = 0.75

middle_half_max = 0.45
middle_half_min = -0.4

middle_down_max = -0.5
middle_down_min = -1.1

ring_up_max = 1.1
ring_up_min = 0.75

ring_half_max = 0.45
ring_half_min = -0.4

ring_down_max = -0.5
ring_down_min = -1.1

pinky_up_max = 1.1
pinky_up_min = 0.75

pinky_half_max = 0.45
pinky_half_min = -0.3

pinky_down_max = -0.4
pinky_down_min = -1.1





h_list = []
# ---------- Main Loop ----------
while True:
    h_list = []
    ax1, ay1, az1 = safe_accel(imu1, 0, 0x69)
    ax2, ay2, az2 = safe_accel(imu2, 1, 0x68)
    ax3, ay3, az3 = safe_accel(imu3, 2, 0x68)
    ax4, ay4, az4 = safe_accel(imu4, 3, 0x68)
    ax5, ay5, az5 = safe_accel(imu5, 4, 0x68)
    
    if(ax1 == 0 or ay1 == 0 or az1 == 0 or ax2 == 0 or ay2 == 0 or az2 == 0 or ax3 == 0 or ay3 == 0 or az3 == 0 or ax4 == 0 or ay4 == 0 or az4 == 0 or ax5 == 0 or ay5 == 0 or az5 == 0):
        continue
    if (ax1 <= thumb_up_max) and (ax1 >= thumb_up_min):
        # print("Thumb Up ")
        h_list.append("Thumb Up")
    elif (ax1 <= thumb_half_max) and (ax1 >= thumb_half_min):
        #print("Thumb Half")
        h_list.append("Thumb Half")
    elif(ax1 <= thumb_down_max) and (ax1 >= thumb_down_min):
        #print("Thumb Down")
        h_list.append("Thumb Down")
    else:
        print("Error")
    if (ax2 <= index_up_max) and (ax2 >= index_up_min):
        #print("Index Up")
        h_list.append("Index Up")
    elif (ax2 <= index_half_max) and (ax2 >= index_half_min):
        #print("Index Half")
        h_list.append("Index Half")
    elif(ax2 <= index_down_max) and (ax2 >= index_down_min):
        #print("Index Down")
        h_list.append("Index Down")
    else:
        print("Error")
    if (ax3 <= middle_up_max) and (ax3 >= middle_up_min):
        #print("Middle Up ")
        h_list.append("Middle Up")
    elif (ax3 <= middle_half_max) and (ax3 >= middle_half_min):
        #print("Middle Half")
        h_list.append("Middle Half")
    elif(ax3 <= middle_down_max) and (ax3 >= middle_down_min):
        #print("Middle Down")
        h_list.append("Middle Down")
    else:
        print("Error")
    if (ax4 <= ring_up_max) and (ax4 >= ring_up_min):
        # print("Ring Up ")
        h_list.append("Ring Up")
    elif (ax4 <= ring_half_max) and (ax4 >= ring_half_min):
        #print("Ring Half")
        h_list.append("Ring Half")
    elif(ax4 <= ring_down_max) and (ax4 >= ring_down_min):
        #print("Ring Down") 
        h_list.append("Ring Down")
    else:
        print("Error")
    if (ax5 <= pinky_up_max) and (ax5 >= pinky_up_min):
        #print("Pinky Up ")
        h_list.append("Pinky Up")
    elif (ax5 <= pinky_half_max) and (ax5 >= pinky_half_min):
        #print("Pinky Half")
        h_list.append("Pinky Half")
    elif(ax5 <= pinky_down_max) and (ax5 >= pinky_down_min):
        #print("Pinky Down")
        h_list.append("Pinky Down")
    else:
        print("Error")
    
    
    if len(h_list) != 5 :
        continue
    else:
        if h_list[0] == "Thumb Up" and h_list[1] == "Index Down" and h_list[2] == "Middle Down" and h_list[3] == "Ring Down" and h_list[4] == "Pinky Down":
            print("A")
        elif h_list[0] == "Thumb Half" and h_list[1] == "Index Up" and h_list[2] == "Middle Up" and h_list[3] == "Ring Up" and h_list[4] == "Pinky Up":
            print("B")
        elif h_list[0] == "Thumb Up" and h_list[1] == "Index Half" and h_list[2] == "Middle Half" and h_list[3] == "Ring Half" and h_list[4] == "Pinky Half":
            print("C")
        elif h_list[0] == "Thumb Half" and h_list[1] == "Index Up" and h_list[2] == "Middle Down" and h_list[3] == "Ring Down" and h_list[4] == "Pinky Down":
            print("D")
        elif h_list[0] == "Thumb Half" and h_list[1] == "Index Half" and h_list[2] == "Middle Half" and h_list[3] == "Ring Half" and h_list[4] == "Pinky Half":
            print("E")
        elif h_list[0] == "Thumb Half" and h_list[1] == "Index Half" and h_list[2] == "Middle Up" and h_list[3] == "Ring Up" and h_list[4] == "Pinky Up": 
            print("F")
        elif h_list[0] == "Thumb Up" and h_list[1] == "Index Down" and h_list[2] == "Middle Down" and h_list[3] == "Ring Half" and h_list[4] == "Pinky Up":
            print("G")
        elif h_list[0] == "Thumb Down" and h_list[1] == "Index Half" and h_list[2] == "Middle Half" and h_list[3] == "Ring Down" and h_list[4] == "Pinky Down":
            print("H")
        elif h_list[0] == "Thumb Up" and h_list[1] == "Index Down" and h_list[2] == "Middle Down" and h_list[3] == "Ring Down" and h_list[4] == "Pinky Up":
            print("I")
        elif h_list[0] == "Thumb Up" and h_list[1] == "Index Down" and h_list[2] == "Middle Half" and h_list[3] == "Ring Half" and h_list[4] == "Pinky Up":
            print("J")
        elif h_list[0] == "Thumb Up" and h_list[1] == "Index Up" and h_list[2] == "Middle Up" and h_list[3] == "Ring Down" and h_list[4] == "Pinky Down":
            print("K")
        elif h_list[0] == "Thumb Up" and h_list[1] == "Index Up" and h_list[2] == "Middle Down" and h_list[3] == "Ring Down" and h_list[4] == "Pinky Down":
            print("L")
        elif h_list[0] == "Thumb Half" and h_list[1] == "Index Up" and h_list[2] == "Middle Up" and h_list[3] == "Ring Down" and h_list[4] == "Pinky Up":
            print("M")
        elif h_list[0] == "Thumb Half" and h_list[1] == "Index Up" and h_list[2] == "Middle Down" and h_list[3] == "Ring Half" and h_list[4] == "Pinky Up":
            print("N")
        elif h_list[0] == "Thumb Down" and h_list[1] == "Index Down" and h_list[2] == "Middle Down" and h_list[3] == "Ring Down" and h_list[4] == "Pinky Up":
            print("O")
        elif h_list[0] == "Thumb Up" and h_list[1] == "Index Up" and h_list[2] == "Middle Down" and h_list[3] == "Ring Half" and h_list[4] == "Pinky Up":
            print("P")
        elif h_list[0] == "Thumb Half" and h_list[1] == "Index Down" and h_list[2] == "Middle Down" and h_list[3] == "Ring Half" and h_list[4] == "Pinky Up":
            print("Q")
        elif h_list[0] == "Thumb Down" and h_list[1] == "Index Up" and h_list[2] == "Middle Up" and h_list[3] == "Ring Half" and h_list[4] == "Pinky Half":
            print("R")
        elif h_list[0] == "Thumb Half" and h_list[1] == "Index Half" and h_list[2] == "Middle Half" and h_list[3] == "Ring Down" and h_list[4] == "Pinky Down":
            print("S")
        elif h_list[0] == "Thumb Up" and h_list[1] == "Index Half" and h_list[2] == "Middle Down" and h_list[3] == "Ring Down" and h_list[4] == "Pinky Down":
            print("T")
        elif h_list[0] == "Thumb Down" and h_list[1] == "Index Up" and h_list[2] == "Middle Up" and h_list[3] == "Ring Down" and h_list[4] == "Pinky Down":
            print("U")
        elif h_list[0] == "Thumb Up" and h_list[1] == "Index Down" and h_list[2] == "Middle Up" and h_list[3] == "Ring Down" and h_list[4] == "Pinky Up":
            print("V")
        elif h_list[0] == "Thumb Half" and h_list[1] == "Index Up" and h_list[2] == "Middle Up" and h_list[3] == "Ring Up" and h_list[4] == "Pinky Down":
            print("W")
        elif h_list[0] == "Thumb Half" and h_list[1] == "Index Half" and h_list[2] == "Middle Down" and h_list[3] == "Ring Down" and h_list[4] == "Pinky Down":
            print("X")
        elif h_list[0] == "Thumb Up" and h_list[1] == "Index Up" and h_list[2] == "Middle Down" and h_list[3] == "Ring Down" and h_list[4] == "Pinky Up":
            print("Y")
        elif h_list[0] == "Thumb Up" and h_list[1] == "Index Up" and h_list[2] == "Middle Up" and h_list[3] == "Ring Down" and h_list[4] == "Pinky Up":
            print("Z")
    print(h_list)
    sleep(0.02)

