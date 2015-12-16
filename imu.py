#!/usr/bin/python
from adxl345 import ADXL345
from l3g4200d import L3G4200D
from hmc5883l import HMC5883L
from bmp085 import BMP085
from mpu6050 import MPU6050
import math

class IMU(object):
    
    def __init__(self, bus, gyro_address, accel_address, compass_address, box_address, name, gyro_scale=L3G4200D.FS_2000, accel_scale=ADXL345.AFS_16g):
        self.bus = bus
        self.gyro_address = gyro_address 
        self.accel_address = accel_address
        self.box_address = box_address
        self.gyro_scale = gyro_scale 
        self.accel_scale = accel_scale
	self.name = name
        self.box = MPU6050(bus, box_address, name + "-box")
        self.accelerometer = ADXL345(bus, accel_address, name + "-accelerometer", accel_scale)
        self.gyroscope = L3G4200D(bus, gyro_address, name + "-gyroscope", gyro_scale)
        self.compass = HMC5883L(bus, compass_address, name + "-compass")

        self.read_all()

    def read_all(self):
        self.gyroscope.read_raw_data()
        self.accelerometer.read_raw_data()
        self.box.read_raw_data()
	self.compass.read_raw_data()
	 
	self.compass.set_offsets(9, -10, -140)
        
        self.gyro_scaled_x = round(self.gyroscope.read_scaled_gyro_x(),4)
        self.gyro_scaled_y = round(self.gyroscope.read_scaled_gyro_y(),4)
        self.gyro_scaled_z = round(self.gyroscope.read_scaled_gyro_z(),4)
        
        self.accel_scaled_x = round(self.accelerometer.read_scaled_accel_x(),4)
        self.accel_scaled_y = round(self.accelerometer.read_scaled_accel_y(),4)
        self.accel_scaled_z = round(self.accelerometer.read_scaled_accel_z(),4)
        
        self.gyro_1_scaled_x = round(self.box.read_scaled_gyro_x(),4)
        self.gyro_1_scaled_y = round(self.box.read_scaled_gyro_y(),4)
        self.gyro_1_scaled_z = round(self.box.read_scaled_gyro_z(),4)
        
        self.accel_1_scaled_x = round(self.box.read_scaled_accel_x(),4)
        self.accel_1_scaled_y = round(self.box.read_scaled_accel_y(),4)
        self.accel_1_scaled_z = round(self.box.read_scaled_accel_z(),4)
        
	self.compass_all = self.compass.read_all()          
        
        return str(self.gyro_scaled_x) +","+ str(self.gyro_scaled_y)+","+str(self.gyro_scaled_z)+ "," + \
               str(self.accel_scaled_x) + "," + str(self.accel_scaled_y)+ ","+ \
               str(self.accel_scaled_z) + "," + str(self.gyro_1_scaled_x)+ ","+ str(self.gyro_1_scaled_y)+ ","+\
               str(self.gyro_1_scaled_z) + "," + str(self.accel_1_scaled_x)+ ","+ str(self.accel_1_scaled_y)+ ","+ \
               str(self.accel_1_scaled_z) + "," + str(self.compass_all)


    def set_compass_offsets(self,x_offset, y_offset, z_offset):
        self.compass.set_offsets(x_offset, y_offset, z_offset)
