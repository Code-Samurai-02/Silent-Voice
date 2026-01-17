import math

class IMU:
    def __init__(self, sensor):
        self.sensor = sensor
        self.has_mag = hasattr(sensor, "get_mag")
        self._angle = [0.0, 0.0]

    # RAW
    def accel(self):
        return self.sensor.get_accel()

    def gyro(self):
        return self.sensor.get_gyro()

    def mag(self):
        if not self.has_mag:
            raise RuntimeError("Magnetometer not available")
        return self.sensor.get_mag()

    # ACCEL ONLY
    def accel_angles(self):
        ax, ay, az = self.accel()
        roll = math.degrees(math.atan2(ay, az))
        pitch = math.degrees(math.atan2(-ax, math.sqrt(ay*ay + az*az)))
        return roll, pitch

    # COMPLEMENTARY FILTER
    def orientation(self, dt, alpha=0.98):
        ax, ay, az = self.accel()
        gx, gy, gz = self.gyro()

        accel_roll = math.degrees(math.atan2(ay, az))
        accel_pitch = math.degrees(math.atan2(-ax, math.sqrt(ay*ay + az*az)))

        self._angle[0] = alpha * (self._angle[0] + gx * dt) + (1 - alpha) * accel_roll
        self._angle[1] = alpha * (self._angle[1] + gy * dt) + (1 - alpha) * accel_pitch

        return self._angle[0], self._angle[1]

    # YAW (MPU9250 ONLY)
    def heading(self):
        if not self.has_mag:
            raise RuntimeError("Yaw requires magnetometer")
        mx, my, mz = self.mag()
        yaw = math.degrees(math.atan2(my, mx))
        return yaw + 360 if yaw < 0 else yaw
