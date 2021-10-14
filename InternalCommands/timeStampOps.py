import time
import math
import asyncio

async def getTimeAddon(time):
    hour = int(time[0:1])
    minute = int(time[3:4])

    stamp = (hour * 3600) + (minute * 60)
     
    return stamp

async def getStampFromTime(timestr):
    #gets upper and lower bounds of time for a minute from a hh:mm time
    now = time.time()
    midnight = math.floor(now / 86400) * 86400
    lower = midnight + await asyncio.create_task(getTimeAddon(timestr))
    upper = lower + 60
    
    return upper, lower

async def getStampBoundsFromAddon(addon):
    #gets upper and lower bounds of time for a minute from addon stamp
    now = time.time()
    midnight = math.floor(now / 86400) * 86400
    lower = midnight + addon
    upper = lower + 60
    
    return upper, lower
