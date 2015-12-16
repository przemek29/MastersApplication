#!/usr/bin/python
import math
import time
import smbus

import i2cutils as I2CUtils

class ADXL345(object):

    POWER_CTL = 0x2d
    DATA_FORMAT = 0x31
    FIFO_CTL = 0x38
    
    AFS_2g = 0
    AFS_4g = 1
    AFS_8g = 2
    AFS_16g = 3

    ACCEL_START_BLOCK = 0x32
    ACCEL_XOUT_H = 1
    ACCEL_XOUT_L = 0
    ACCEL_YOUT_H = 3
    ACCEL_YOUT_L = 2
    ACCEL_ZOUT_H = 5
    ACCEL_ZOUT_L = 4

    ACCEL_SCALE = 0.004 # Always set to this as we are using FULL_RES

    def __init__(self, bus, address, name, afs_scale=AFS_2g):

        self.bus = bus
        self.address = address
        self.name = name

        self.afs_scale = afs_scale
        
        self.raw_accel_data = [0, 0, 0, 0, 0, 0]
        
        self.accel_raw_x = 0
        self.accel_raw_y = 0
        self.accel_raw_z = 0
        
        self.accel_scaled_x = 0
        self.accel_scaled_y = 0
        self.accel_scaled_z = 0
        
        self.pitch = 0.0
        self.roll = 0.0
        self.last_time = time.time()
        self.time_diff = 0
        
        
        # Wake up the device
        I2CUtils.i2c_write_byte(self.bus, self.address,ADXL345.POWER_CTL, 0b00001000)
        
        # Set data to FULL_RES and user defined scale 
        data_format = 1 << 3 | afs_scale
        I2CUtils.i2c_write_byte(self.bus, self.address,ADXL345.DATA_FORMAT, data_format)

        # Disable FIFO mode
        I2CUtils.i2c_write_byte(self.bus, self.address,ADXL345.FIFO_CTL, 0b00000000)
           
    def read_raw_data(self):
        self.raw_accel_data = I2CUtils.i2c_read_block(self.bus, self.address, ADXL345.ACCEL_START_BLOCK, 6)
        
        self.accel_raw_x = I2CUtils.twos_compliment(self.raw_accel_data[ADXL345.ACCEL_XOUT_H], self.raw_accel_data[ADXL345.ACCEL_XOUT_L])
        self.accel_raw_y = I2CUtils.twos_compliment(self.raw_accel_data[ADXL345.ACCEL_YOUT_H], self.raw_accel_data[ADXL345.ACCEL_YOUT_L])
        self.accel_raw_z = I2CUtils.twos_compliment(self.raw_accel_data[ADXL345.ACCEL_ZOUT_H], self.raw_accel_data[ADXL345.ACCEL_ZOUT_L])

        self.accel_scaled_x = self.accel_raw_x * ADXL345.ACCEL_SCALE
        self.accel_scaled_y = self.accel_raw_y * ADXL345.ACCEL_SCALE
        self.accel_scaled_z = self.accel_raw_z * ADXL345.ACCEL_SCALE
        
    def distance(self, x, y):
        return math.sqrt((x * x) + (y * y))
    
    def read_raw_accel_x(self):
        return self.accel_raw_x
        
    def read_raw_accel_y(self):
        return self.accel_raw_y
        
    def read_raw_accel_z(self):
        return self.accel_raw_z
    
    def read_scaled_accel_x(self):
        return self.accel_scaled_x
    
    def read_scaled_accel_y(self):
        return self.accel_scaled_y

    def read_scaled_accel_z(self):
        return self.accel_scaled_z

