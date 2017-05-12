#
# core_module.py
# Read/write to modern robotics "core" modules
# Peter Brier
#
# Protocol:
# See https://github.com/pbrier/ftc_app/wiki/Modern-Robotics-interfaces
#
#
#
import traceback
import serial
from serial.tools import list_ports

port_speed = 250000
device_type_table = {"M": "DEVICE_ID_DC_MOTOR_CONTROLLER", "S": "DEVICE_ID_SERVO_CONTROLLER", "I": "DEVICE_ID_LEGACY_MODULE" }


#
# MR core module class
#
class core_module(object):
    def __init__(self, serial_port_name):
        self.serial = serial.Serial(serial_port_name, port_speed, timeout=1)  # open serial port, nonblocking
        self.serial_number = "None"
        self.port_name = self.serial.name
        self.device_name = "None"
        self.device_type = "None"
        self.serial.sendBreak(duration=1.0)
        self.open = True

    def flush(self):
        self.serial.flushInput()
        self.serial.flushOutput()

    # Send the read register command and respond back with the answer
    def read(self, address, length):
        bytes = [85, 256-86, 256-128,address, length]
        # print bytes
        self.flush()
        self.serial.write("".join(map(chr, bytes)))
        response = self.serial.read(5+length)
        if (response == None) or (len(response) != 5+length):
            print "No response on " + self.device_type + " device " + self.device_name + " via port " + self.port_name
            return None
        return response[5:]

    # Send the "write registers" command to write a range of registers
    def write(self, address, length, data):
        self.flush()        
        bytes = [85, 256-86, 0, address, length, data]
        self.serial.write("".join(map(chr, bytes)))
        response = self.serial.read(5)
        if len(response) != 5:
            return False
        return True
        
    def close(self):
        self.serial.close()             # close port

        
# Interface to All core modules connected:        
class core_module_handler(object):
    # find all core modules
    def __init__(self):
        self.modules = []
        for port in list_ports.comports():
            module = core_module(port[0])
            module.device_name = port[2];
            module.serial_number = port[2].split('+')[2]
            self.identify(module)
            self.modules.append(module)
                
    def identify(self, module):
        print module.port_name, module.serial_number,
        data = module.read(0,3)
        if data == None:
            print "No response on identify module"
        elif len(data) == 3:
            module.device_type = device_type_table[ data[2] ]
            print module.device_type
        else:
            print "Cannot identify device type"

    
# test function to constantly communicate to all core modules    
modules = core_module_handler()    

i = 0
while True:
    print
    print
    print i
    i += 1
    for m in modules.modules:
        try:
            modules.identify(m)
        except Exception, e:
            traceback.print_exc()  
            pass
