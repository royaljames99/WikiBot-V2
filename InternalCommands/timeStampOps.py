import time
import math
import asyncio

async def getTimeAddonFromString(time):
    hour = int(time[0:2])
    minute = int(time[3:5])

    stamp = (hour * 3600) + (minute * 60)
     
    return stamp


async def getTimeAddonNow():
    now = time.time()

    todayTime = now % 86400
    hour = (math.floor(todayTime / 3600) + 1) % 24
    minute = math.floor((todayTime % 3600) / 60)

    stamp = (hour * 3600) + (minute * 60)
    return stamp


async def getDisplayTime(addon): #47280
    hour = str(math.floor(addon / 3600))
    minute = str(math.floor((addon % 3600) / 60))

    if len(hour) == 1:
        hour = "0" + hour
    if len(minute) == 1:
        minute = "0" + minute

    assembled = hour + ":" + minute
    return assembled