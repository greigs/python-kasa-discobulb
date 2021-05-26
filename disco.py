import asyncio
import kasa
import random
from operator import itemgetter, attrgetter

searchTimeout = 20 # default is 5, but this seems more reliable
active1 = 0
active2 = 1

# async def randomset(bulbs, t):
#     for b in bulbs:
#         await b.set_hsv(random.randint(10, 360), 100, 100, transition=t)
#         await b.update()


async def orderedset(bulbs, t):
    global active1
    turnoff1 = active1 - 1
    if turnoff1 < 0:
        turnoff1 = 5

    global active2
    turnoff2 = active2 - 1
    if turnoff2 < 0:
        turnoff2 = 5
    tasks = [ 
        bulbs[active1].set_hsv(0, 0, 100, transition=500),
        bulbs[active2].set_hsv(0, 0, 20, transition=500),
        bulbs[turnoff1].set_brightness(0, transition=500)
        # bulbs[turnoff2].set_hsv(195, 100, 100, transition=500),
    ]
    await asyncio.wait(tasks)
    if active1 == 5:
        active1 = 0
    else:
        active1 = active1 + 1
    if active2 == 5:
        active2 = 0
    else:
        active2 = active2 + 1

async def initBulb(ip):
    bulb = kasa.SmartBulb(ip)
    await bulb.update()
    print(flush=True)
    print(bulb.alias, flush=True)
    print(ip, flush=True)
    return bulb

async def main():
    print('Disco time. Searching for Kasa RGB bulbs...', flush=True)
    print('Ctrl + C to exit at any time', flush=True)
    
    found_devices = sorted(await kasa.Discover.discover(timeout=searchTimeout))
    bulb_devices = []
    for devStr in found_devices: 
        dev = await kasa.Discover.discover_single(devStr)
        if (dev.is_bulb and dev.is_color):
            bulb_devices.append(await initBulb(devStr))
    bulb_devices = sorted(bulb_devices, key=attrgetter('alias'))
    print(flush=True)
    for ordered in bulb_devices:
        print(ordered.alias, flush=True)

    if not bulb_devices:
        print('No Kasa RGB bulb devices found', flush=True)
    else:
        while True:
            await orderedset(bulb_devices, 1)
            await asyncio.sleep(0.3)

loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(main())
except KeyboardInterrupt:
    print("Received exit command, exiting", flush=True)
