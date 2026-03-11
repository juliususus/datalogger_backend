from logger.ILogger import ILogger
from utils import coordinatesToSpeed

import random
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

class MockLogger(ILogger):
    def __init__(self, data_dir="./data"):
        super().__init__(data_dir=data_dir)

    # === Acquisition logic ===
    def readSensors(self):
        previous_gps = self.data_record["gps"]
        self.data_record["timestamp"] = time.time()
        self.data_record["accel"] = {"x": random.uniform(-100, 100), "y": random.uniform(-100, 100), "z": random.uniform(-100, 100)}
        self.data_record["gyro"] = {"x": random.uniform(0, 360), "y": random.uniform(0, 360), "z": random.uniform(0, 360)}
        self.data_record["temp"] = random.uniform(10, 30)
        self.data_record["gps"] = {"timestamp": time.time(), "latitude": random.uniform(46.991007, 46.991004), "longitude": random.uniform(15.42088, 15.420909), "altitude": random.uniform(0, 394)}
        self.data_record["sog"] = coordinatesToSpeed(previous_gps["latitude"], previous_gps["longitude"], previous_gps["timestamp"], self.data_record["gps"]["latitude"], self.data_record["gps"]["longitude"], self.data_record["gps"]["timestamp"])
