from machine import I2C, Pin
import utime
from mpu6050 import MPU6050

i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
sensor = MPU6050(i2c)
start_time = utime.ticks_ms()

while True:
    t = (utime.ticks_ms() - start_time) / 1000.0
    ax, ay, az, gx, gy, gz = sensor.read_raw()
    print("{:.3f},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f}".format(t, ax, ay, az, gx, gy, gz))
    utime.sleep_ms(10)
