from machine import I2C, Pin
import struct

class MPU6050:
    def __init__(self, i2c, addr=0x68):
        self.i2c = i2c
        self.addr = addr
        # Wake up MPU6050 (clear sleep bit in PWR_MGMT_1 register 0x6B)
        self.i2c.writeto_mem(self.addr, 0x6B, bytes([0]))

    def read_raw(self):
        # Read 14 consecutive registers starting at ACCEL_XOUT_H (0x3B)
        data = self.i2c.readfrom_mem(self.addr, 0x3B, 14)
        # Unpack 7 signed 16-bit integers (big-endian)
        ax, ay, az, temp_raw, gx, gy, gz = struct.unpack('>hhhhhhh', data)
        
        # Scale values (Accelerometer +-2g, Gyroscope +-250 deg/s)
        accel_x = ax / 16384.0
        accel_y = ay / 16384.0
        accel_z = az / 16384.0
        gyro_x = gx / 131.0
        gyro_y = gy / 131.0
        gyro_z = gz / 131.0
        
        return accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z
