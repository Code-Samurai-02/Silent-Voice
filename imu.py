import time
import math

class IMU:
    """
    Generic IMU wrapper.
    Works with MPU6050 and MPU9250 drivers.
    """

    def __init__(self, sensor):
        """
        sensor: instance of MPU6050 or MPU9250
        """
        self.sensor = sensor
        self.has_mag = hasattr(sensor, "magnet")

    # -------- RAW DATA --------
    def accel(self):
        return self.sensor.get_accel() if hasattr(self.sensor, "get_accel") else self.sensor.accel()

    def gyro(self):
        return self.sensor.get_gyro() if hasattr(self.sensor, "get_gyro") else self.sensor.gyro()

    def mag(self):
        if not self.has_mag:
            raise RuntimeError("Magnetometer not available")
        return self.sensor.magnet()

    def temperature(self):
        if hasattr(self.sensor, "get_temperature"):
            return self.sensor.get_temperature()
        return self.sensor.temperature()

    # -------- ORIENTATION (ACCEL ONLY) --------
    def accel_angles(self):
        """
        Returns roll, pitch from accelerometer (degrees)
        """
        ax, ay, az = self.accel()

        roll = math.degrees(math.atan2(ay, az))
        pitch = math.degrees(math.atan2(-ax, math.sqrt(ay*ay + az*az)))

        return roll, pitch

    # -------- COMPLEMENTARY FILTER --------
    def orientation(self, dt, alpha=0.98):
        """
        Simple complementary filter
        Call at fixed dt (seconds)
        """
        if not hasattr(self, "_angle"):
            self._angle = [0.0, 0.0]

        ax, ay, az = self.accel()
        gx, gy, gz = self.gyro()

        accel_roll = math.degrees(math.atan2(ay, az))
        accel_pitch = math.degrees(math.atan2(-ax, math.sqrt(ay*ay + az*az)))

        self._angle[0] = alpha * (self._angle[0] + gx * dt) + (1 - alpha) * accel_roll
        self._angle[1] = alpha * (self._angle[1] + gy * dt) + (1 - alpha) * accel_pitch

        return self._angle[0], self._angle[1]

    # -------- HEADING (IF MAG PRESENT) --------
    def heading(self):
        if not self.has_mag:
            raise RuntimeError("Heading requires magnetometer")

        mx, my, mz = self.mag()
        heading = math.degrees(math.atan2(my, mx))
        if heading < 0:
            heading += 360
        return heading
