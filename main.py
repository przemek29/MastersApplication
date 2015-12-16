#!/usr/bin/python
from imu import IMU
from bmp085 import BMP085
import smbus
import math
import serial

port = serial.Serial("/dev/ttyAMA0", baudrate=115200, timeout=3.0)
	
if __name__ == "__main__":

    bus = smbus.SMBus(1)
    imu_controller = IMU(bus, 0x69, 0x53, 0x1e, 0x68, "IMU")
   
    counter = 0
 
    #The main loop of IMU
    while True:
	imu_data = imu_controller.read_all()
	#if not (counter%200):
	    #barometer = BMP085(bus, 0x77, "-barometer")
   	    #pressure = barometer.read_pressure()
	    #temperature = barometer.read_temperature()

#        port.write(str(counter) + "," + str(imu_data) + "," + str(pressure) + "," + str(temperature) + "\r\n")
        port.write(str(counter) + "," + str(imu_data) + "\r\n")
        counter += 1
