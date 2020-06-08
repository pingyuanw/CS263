import asyncio
import time

def compute_some_thing():
    x = 1
    for i in range(21500000):
        x = x*i

async def step1():
    compute_some_thing()
    await asyncio.sleep(1)

async def step2():
    await asyncio.wait([step1() for x in range(10)])
    compute_some_thing()
    await asyncio.sleep(1)

async def step3():
    await asyncio.wait([step2() for x in range(10)])
    compute_some_thing()
    await asyncio.sleep(1)

start = time.monotonic()

asyncio.get_event_loop().run_until_complete(step3())

print(time.monotonic() - start)
