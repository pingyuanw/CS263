import asyncio
import time

def compute_some_thing():
    x = 1
    for i in range(10240):
        x = x*i

async def put_elephant_into_fridge():
    compute_some_thing()
    await asyncio.sleep(1)

async def ship():
    await asyncio.wait([put_elephant_into_fridge() for x in range(10)])
    compute_some_thing()
    await asyncio.sleep(1)

async def get_100_elephant():
    await asyncio.wait([ship() for x in range(10)])
    compute_some_thing()
    await asyncio.sleep(1)

start = time.monotonic()
# asyncio.get_event_loop().run_until_complete(get_100_elephant())
task = asyncio.wait([get_100_elephant() for x in range(10000)])
asyncio.get_event_loop().run_until_complete(task)

print(time.monotonic() - start)
