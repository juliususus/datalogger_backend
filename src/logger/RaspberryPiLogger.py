from ILogger import ILogger

import sys
sys.path.insert(1,'/home/ht/HPSDataLogger/i2clibraries')
from i2c_adxl345 import *
from i2c_itg3205 import *
import pynmea2
import serial
import time

def flattenDict(d, parent_key='', sep='_'):
    items = []
    for key, val in d.items():
        flat_key = f"{parent_key}{sep}{key}" if parent_key else key
        if isinstance(val, dict):
            items.extend(flattenDict(val, flat_key, sep=sep).items())
        else:
            items.append((flat_key, val))
    return dict(items)

class RaspberryPiLogger(ILogger):
    def __init__(self, data_dir="/home/ht/HPSDataLogger/data/"):
        super().__init__(data_dir=data_dir)

        # === Initialize sensors ===
        self.adxl345 = i2c_adxl345(0)
        self.itg3205 = i2c_itg3205(0)
        self.ser = serial.Serial("/dev/serial0",timeout=0.001)


    # === Acquisition logic ===
    def readSensors(self):
        try:
            self.data_record["timestamp"] = time.time()

            out_accel = self.adxl345.getAxes()
            self.data_record["accel"] = {"x": out_accel[0], "y": out_accel[1], "z": out_accel[2]}

            temp = self.itg3205.getDieTemperature()
            self.data_record["temp"] = temp

            (gyro_x, gyro_y, gyro_z) = self.itg3205.getDegPerSecAxes()
            self.data_record["gyro"] = {"x": gyro_x, "y": gyro_y, "z": gyro_z}

            gps_data = (self.ser.readline().decode("unicode_escape"))
            if gps_data[0:6]=="$GPGGA":
                gps_msg = pynmea2.parse(gps_data)
                self.data_record["gps"]["altitude"] = gps_msg.altitude
                self.data_record["gps"]["timestamp"] = gps_msg.timestamp
            elif gps_data[0:6]=="$GPRMC":
                gps_msg = pynmea2.parse(gps_data)
                self.data_record["gps"]["latitude"] = gps_msg.latitude
                self.data_record["gps"]["longitude"] = gps_msg.longitude
        except:
            pass
