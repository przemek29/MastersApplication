#!/usr/bin/python
import math

import i2cutils as I2CUtils

class HMC5883L(object):

    TWO_PI = 2 * math.pi

    CONF_REG_A = 0
    CONF_REG_B = 1
    MODE_REG = 2
    DATA_START_BLOCK = 3
    DATA_XOUT_H = 0
    DATA_XOUT_L = 1
    DATA_ZOUT_H = 2
    DATA_ZOUT_L = 3
    DATA_YOUT_H = 4
    DATA_YOUT_L = 5

    SAMPLE_RATE = { 0 : 0.75, 1 : 1.5, 2 : 3, 3 : 7.5, 4 : 15, 5 : 30, 6 : 75, 7 :-1 }

    SAMPLE_MODE = { 0 : "CONTINUOUS", 1 : "SINGLE", 2 : "IDLE", 3 : "IDLE" }

    GAIN_SCALE = {
                    0 : [ 0.88, 1370, 0.73 ],
                    1 : [ 1.30, 1090, 0.92 ],
                    2 : [ 1.90, 820, 1.22 ],
                    3 : [ 2.50, 660, 1.52 ],
                    4 : [ 4.00, 440, 2.27 ],
                    5 : [ 4.70, 390, 2.56 ],
                    6 : [ 5.60, 330, 3.03 ],
                    7 : [ 8.10, 230, 4.35 ]
                 }


    def __init__(self, bus, address, name, samples=3, rate=4, gain=1, sampling_mode=0, x_offset=0, y_offset=0, z_offset=0):
        self.bus = bus
        self.address = address
        self.name = name
        self.samples = samples
        self.gain = gain
        self.sampling_mode = sampling_mode
        
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.z_offset = z_offset
        
	#Turn off magnetometer as slave and create a connection as multimaster
	I2CUtils.i2c_write_byte(self.bus, 0x68, 0x37, 0x32)
	
        # Set the number of samples
        conf_a = (samples << 5) + (rate << 2)
        I2CUtils.i2c_write_byte(self.bus, self.address, HMC5883L.CONF_REG_A, conf_a)
        
        # Set the gain
        conf_b = gain << 5
        I2CUtils.i2c_write_byte(self.bus, self.address, HMC5883L.CONF_REG_B, conf_b)

        # Set the operation mode
        I2CUtils.i2c_write_byte(self.bus, self.address, HMC5883L.MODE_REG, self.sampling_mode)        

        self.raw_data = [0, 0, 0, 0, 0, 0]
        
        # Now read all the values as the first read after a gain change returns the old value
        self.read_raw_data()
    
    def read_raw_data(self):

        self.raw_data = I2CUtils.i2c_read_block(self.bus, self.address, HMC5883L.DATA_START_BLOCK, 6)
        self.raw_x = I2CUtils.twos_compliment(self.raw_data[HMC5883L.DATA_XOUT_H], self.raw_data[HMC5883L.DATA_XOUT_L]) - self.x_offset
        self.raw_y = I2CUtils.twos_compliment(self.raw_data[HMC5883L.DATA_YOUT_H], self.raw_data[HMC5883L.DATA_YOUT_L]) - self.y_offset
        self.raw_z = I2CUtils.twos_compliment(self.raw_data[HMC5883L.DATA_ZOUT_H], self.raw_data[HMC5883L.DATA_ZOUT_L]) - self.z_offset
    
        self.scaled_x = self.raw_x * HMC5883L.GAIN_SCALE[self.gain][2]
        self.scaled_y = self.raw_y * HMC5883L.GAIN_SCALE[self.gain][2]
        self.scaled_z = self.raw_z * HMC5883L.GAIN_SCALE[self.gain][2]
	
    def read_all(self):
	self.read_raw_data()
	return str(self.scaled_x - 122) + "," + str(self.scaled_y + 34) + "," + str(self.scaled_z +484)

    def set_offsets(self, x_offset, y_offset, z_offset):
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.z_offset = z_offset
    
    

