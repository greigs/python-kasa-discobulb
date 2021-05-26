import asyncio
import kasa
import random

runtimeSeconds = 60

async def randomset(bulbs, t):
    for b in bulbs:
        await b.set_hsv(random.randint(10, 360), 100, 100, transition=t)
        await b.update()
    

async def initBulb(ip):
    bulb = kasa.SmartBulb(ip)
    await bulb.update()
    print(bulb.alias)
    return bulb

async def main():
    print('disco time')
    
    found_devices = await kasa.Discover.discover()
    bulb_devices = []
    for devStr in found_devices: 
        dev = await kasa.Discover.discover_single(devStr)
        if (dev.is_bulb and dev.is_color):
            bulb_devices.append(await initBulb(devStr))
            print(devStr)
    
    for x in range(1, runtimeSeconds):
        await randomset(bulb_devices, 1_000)
        await asyncio.sleep(1)

    print('done')

asyncio.run(main())
