# Silent-Voice


ax = x axis 
ay = y axis
az = z axis

ax, ay, az = mpu.get_accel()

if ax > 0.2:
    print("RIGHT")
elif ax < -0.2:
    print("LEFT")
else:
    print("CENTER")
