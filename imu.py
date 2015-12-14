#!/usr/bin/python
import time

from adxl345 import ADXL345
from l3g4200d import L3G4200D
from hmc5883l import HMC5883L
from bmp085 import BMP085
from mpu6050 import MPU6050
import smbus
import timeit
import math
class IMU(object):
    
    K = 0.98
    K1 = 1 - K
   


    
    def __init__(self, bus, gyro_address, accel_address, compass_address, box_address, name, gyro_scale=L3G4200D.FS_2000, accel_scale=ADXL345.AFS_16g):
        self.bus = bus
        self.gyro_address = gyro_address 
        self.accel_address = accel_address
        self.box_address = box_address
        self.name = name
        self.gyro_scale = gyro_scale 
        self.accel_scale = accel_scale
        self.box = MPU6050(bus, box_address, name + "-box")
        self.accelerometer = ADXL345(bus, accel_address, name + "-accelerometer", accel_scale)
        self.gyroscope = L3G4200D(bus, gyro_address, name + "-gyroscope", gyro_scale)
        self.compass = HMC5883L(bus, compass_address, name + "-compass")

        self.last_time = time.time()
        self.time_diff = 0

        self.pitch = 0
        self.roll = 0
        # take a reading from the device to allow it to settle after config changes
        self.read_all()
        # now take another to act a starting value
        self.read_all()
        self.pitch = self.rotation_x
        self.roll = self.rotation_y

    def read_all(self):
        '''Return pitch and roll in radians and the scaled x, y & z values from the gyroscope and accelerometer'''
        self.gyroscope.read_raw_data()
        self.accelerometer.read_raw_data()
        self.box.read_raw_data()
        
        self.gyro_scaled_x = round(self.gyroscope.read_scaled_gyro_x(),4)
        self.gyro_scaled_y = round(self.gyroscope.read_scaled_gyro_y(),4)
        self.gyro_scaled_z = round(self.gyroscope.read_scaled_gyro_z(),4)
        
        self.accel_scaled_x = round(self.accelerometer.read_scaled_accel_x(),4)
        self.accel_scaled_y = round(self.accelerometer.read_scaled_accel_y(),4)
        self.accel_scaled_z = round(self.accelerometer.read_scaled_accel_z(),4)
        
        self.rotation_x = self.accelerometer.read_x_rotation(self.accel_scaled_x, self.accel_scaled_y, self.accel_scaled_z)
        self.rotation_y = self.accelerometer.read_y_rotation(self.accel_scaled_x, self.accel_scaled_y, self.accel_scaled_z)

        #self.pressure = self.barometer.read_pressure()
        #self.temperature = self.barometer.read_temperature()

        self.gyro_1_scaled_x = round(self.box.read_scaled_gyro_x(),4)
        self.gyro_1_scaled_y = round(self.box.read_scaled_gyro_y(),4)
        self.gyro_1_scaled_z = round(self.box.read_scaled_gyro_z(),4)
        
        self.accel_1_scaled_x = round(self.box.read_scaled_accel_x(),4)
        self.accel_1_scaled_y = round(self.box.read_scaled_accel_y(),4)
        self.accel_1_scaled_z = round(self.box.read_scaled_accel_z(),4)
        
        
        
        return str(self.gyro_scaled_x) +","+ str(self.gyro_scaled_y)+","+str(self.gyro_scaled_z)+ "," + \
               str(self.accel_scaled_x)+ "," +str(self.accel_scaled_y)+ ","+ \
               str(self.accel_scaled_z)+ ","+str(self.gyro_1_scaled_x)+ ","+ str(self.gyro_1_scaled_y)+ ","+\
               str(self.gyro_1_scaled_z)+ ","+ str(self.accel_1_scaled_x)+ ","+ str(self.accel_1_scaled_y)+ ","+ \
               str(self.accel_1_scaled_z)

       # return str(int(self.pitch))+","+ str(int(self.roll))+","+ str(int(self.yaw))
	return (self.pitch, self.roll, self.yaw)	

    def set_compass_offsets(self,x_offset, y_offset, z_offset):
        self.compass.set_offsets(x_offset, y_offset, z_offset)

if __name__ == "__main__":
    bus = smbus.SMBus(1)#i2c_raspberry_pi_bus_number())
    imu_controller = IMU(bus, 0x69, 0x53, 0x1e, 0x68, "IMU")
    i = 0
    imu_controller.set_compass_offsets(9, -10, -140)
    hmc5883l = HMC5883L(bus, 0x1e, "magneto" )

    while True:
	data = imu_controller.read_all()
	magneto = hmc5883l.read_all()
	print str(i) + "," + str(data) + str(magneto)
	i+=1
	
 
