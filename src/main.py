#!/usr/bin/python3

from api import API
from logger.MockLogger import MockLogger

import asyncio
import threading

def loggingThread(logger, interval):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.run(logger.loggingLoop(interval=interval))

async def main():
    logger = RaspberryPiLogger()
    interval = 0.1
    thread = threading.Thread(target=loggingThread, args=(logger, interval))
    thread.start()
    # await asyncio.gather(runAPI(logger))
    API().runAPI(logger)

if __name__=="__main__":
    asyncio.run(main())
