#!/usr/bin/python3

import asyncio
from logger import Logger


async def main():
    logger = Logger()

    await asyncio.gather(logger.loggingLoop(interval=0.1))

if __name__=="__main__":
    asyncio.run(main())
