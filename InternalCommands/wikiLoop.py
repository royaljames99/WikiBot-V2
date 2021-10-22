import asyncio
import json
import InternalCommands.timeStampOps as timestamp

async def run(bot):
    with open("./Data/wikiSubs.json", "r") as file:
        data = json.load(file)

    addon = await asyncio.create_task(timestamp.getTimeAddonNow())

    for serverId in data:
        for channelId in data[serverId]["CHANNELS"]:
            for hour in data[serverId]["CHANNELS"][channelId]["SUBS_BY_HOUR"]:
                for sub in data[serverId]["CHANNELS"][channelId]["SUBS_BY_HOUR"][hour]:
                    if sub["TIME"] == addon:
                        #get channel
                        channel =  bot.get_channel(int(channelId))
                        #send sub
                        if sub["SUB"].upper() == "WIKI":
                            import InternalCommands.genW as genW
                            asyncio.create_task(genW.run(channel))
                        else:
                            from InternalCommands import genFW
                            asyncio.create_task(genFW.run(channel, sub["SUB"]))