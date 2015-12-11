#!/usr/bin/python

def i2c_raspberry_pi_bus_number():
    return (1)
    
def i2c_read_byte(bus, address, register):
    return bus.read_byte_data(address, register)
 
def i2c_read_word_unsigned(bus, address, register):
    high = bus.read_byte_data(address, register)
    low = bus.read_byte_data(address, register+1)
    return (high << 8) + low

def i2c_read_word_signed(bus, address, register):
    value = i2c_read_word_unsigned(bus, address, register)
    if (value >= 0x8000):
        return -((0xffff - value) + 1)
    else:
        return value

def i2c_read_word_unsigned_l3g4200d(bus, address, register):
    high = bus.read_byte_data(address, register)
    low = bus.read_byte_data(address, register-1)
    return (high <<8)+ low

def i2c_read_word_signed_l3g4200d(bus, address,register):
    value = i2c_read_word_unsigned_l3g4200d(bus, address, register)
    if (value >= 0x8000):
        return - ((0xffff - value)+1)
    else:
        return value

def i2c_write_byte(bus, address, register, value):
    bus.write_byte_data(address, register, value)

def i2c_read_block(bus, address, start, length):
    return bus.read_i2c_block_data(address, start, length)

def twos_compliment(high_byte, low_byte):
    value = (high_byte << 8) + low_byte
    if (value >= 0x8000):
        return -((0xffff - value) + 1)
    else:
        return value
        
if __name__ == "__main__":
    print i2c_raspberry_pi_bus_number()
