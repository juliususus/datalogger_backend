from abc import ABC, abstractmethod
import asyncio
import csv
from datetime import datetime
from pathlib import Path
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

class ILogger(ABC):
    def __init__(self, data_dir="/home/ht/HPSDataLogger/data/"):
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d-%H-%M-%S")
        self.data_record = {
            "timestamp": time.time(),
            "accel": {
                "x": float('nan'),
                "y": float('nan'),
                "z": float('nan')
            },
            "gyro": {
                "x": float('nan'),
                "y": float('nan'),
                "z": float('nan')
            },
            "temp": float('nan'),
            "gps": {
                "timestamp": float('nan'),
                "latitude": float('nan'),
                "longitude": float('nan'),
                "altitude": float('nan')
            }
        }

        # === Write csv header ===
        data_directory = Path(data_dir)
        data_directory.mkdir(parents=True, exist_ok=True)
        self.data_file = data_directory / f"{current_time}.csv"
        header = list(flattenDict(self.data_record).keys())
        with open(self.data_file, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(header)

    # === Acquisition logic ===
    @abstractmethod
    def readSensors(self):
        pass

    def storeRecord(self):
        flat_record = flattenDict(self.data_record)
        data_values = list(flat_record.values())
        with open(self.data_file, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(data_values)

    async def loggingLoop(self, interval):
        while True:
            self.readSensors()
            self.storeRecord()
            await asyncio.sleep(interval)
