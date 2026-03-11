from logger.ILogger import ILogger
from utils import coordinatesToSpeed

import csv
import pandas as pd
import random
import time

def unflattenDict(d, sep='_'):
    def unflattenRecursion(key, val, d, sep='_'):
        if(d is None):
            d = dict()
        key_parts = key.split(sep, 1)
        if(len(key_parts) <= 1):
            d[key_parts[0]] = val
        else:
            d[key_parts[0]] = unflattenRecursion(
                key_parts[1], val, d.setdefault(key_parts[0], None), sep=sep)
        return d

    res = dict()
    for key in d.keys():
        key_parts = key.split(sep, 1)
        if(len(key_parts) <= 1):
            res[key_parts[0]] = d[key]
        else:
            res[key_parts[0]] = unflattenRecursion(
                key_parts[1], d[key], res.setdefault(key_parts[0], None), sep=sep)
    return res


class ReadCSVLogger(ILogger):
    def __init__(self, data_dir="./src/data"):
        super().__init__(data_dir=data_dir)
        self.reader = csv.reader(open(f'{data_dir}/2025-12-04-15-38-50.csv'), delimiter=',')
        self.data_keys = next(self.reader)

    # === Acquisition logic ===
    def readSensors(self):
        previous_gps = self.data_record["gps"]
        data_values = next(self.reader)
        self.data_record = unflattenDict(dict(zip(self.data_keys, data_values)))
        self.data_record["sog"] = coordinatesToSpeed(previous_gps["latitude"], previous_gps["longitude"], previous_gps["timestamp"], self.data_record["gps"]["latitude"], self.data_record["gps"]["longitude"], self.data_record["gps"]["timestamp"])
