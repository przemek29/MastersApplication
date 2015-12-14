
from imu import IMU
from bmp085 import BMP085
import smbus
import math

if __name__ == "__main__":

    bus = smbus.SMBus(1)
    imu_controller = IMU(bus, 0x69, 0x53, 0x1e, 0x68, "IMU")
    
    counter = 0

    while True:
	imu_data = imu_controller.read_all()
	if not (counter%125):
	    barometer = BMP085(bus, 0x77, "-barometer")
   	    pressure = barometer.read_pressure()
	    temperature = barometer.read_temperature()

	print str(counter) + "," + str(imu_data)
	#print str(counter) + "," + str(imu_data) + "," + str(pressure) + "," + str(temperature) 
	#print str(counter) + "," + str(pressure) + "," + str(temperature)
	counter += 1
