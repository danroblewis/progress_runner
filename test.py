import random
import asyncio


async def work(num):
    await asyncio.sleep(random.random())
    return random.random() > 0.1

