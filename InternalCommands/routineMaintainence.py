import json
import copy
import asyncio
import discord
import InternalCommands.checkSub as checkSub
import InternalCommands.timeStampOps as timeOps

async def informOfSubRemoval(bot, sub, serverId, channelId):
    subName = sub["SUB"]
    subTime = sub["TIME"]
    subTimeFormatted = await asyncio.create_task(timeOps.getDisplayTime(subTime))
    subscriberId = sub["SUBSCRIBER_ID"]
    subscriberName = await bot.fetch_user(subscriberId)
    subscriberName = subscriberName.name
    print(f"sub being removed: server: {serverId}, channel: {channelId}, sub: {subName}, time: {subTimeFormatted}")

    embed = discord.Embed(title = "NOTICE OF SUB REMOVAL", description = f"A daily wiki subscription has been removed from this channel due to the sub no longer being valid:\n\nWIKI: {subName}\nTIME: {subTimeFormatted}\nSUBSCRIBER: {subscriberName}")

    channel = await bot.fetch_channel(channelId)
    await channel.send(embed = embed)



async def run(bot):
    print("\nperforming maintainence:")

    with open("./Data/wikiSubs.json", "r") as file:
        data = json.load(file)



    newData = copy.deepcopy(data)


    #check validity of subs
    subsVerified = ["WIKI"]
    subsDiscredited = []
    for serverId in data.keys():
        for channelId in data[serverId]["CHANNELS"].keys():
            for hour in data[serverId]["CHANNELS"][channelId]["SUBS_BY_HOUR"].keys():
                for subIndex in range(0, len(data[serverId]["CHANNELS"][channelId]["SUBS_BY_HOUR"][hour])):

                    sub = data[serverId]["CHANNELS"][channelId]["SUBS_BY_HOUR"][hour][subIndex]
                    if sub["SUB"] not in subsVerified and sub["SUB"] not in subsDiscredited:
                        valid = await asyncio.create_task(checkSub.run(sub["SUB"]))
                        if valid:
                            subsVerified.append(sub["SUB"])
                        else:
                            subsDiscredited.append(sub["SUB"])
                            subName = sub["SUB"]
                            print(f"SUB DISCREDITED: {subName}")
                            asyncio.create_task(informOfSubRemoval(bot, sub, serverId, channelId))
                            del newData[serverId]["CHANNELS"][channelId]["SUBS_BY_HOUR"][hour][subIndex]

                    else:
                        if sub["SUB"] in subsDiscredited:
                            asyncio.create_task(informOfSubRemoval(bot, sub, serverId, channelId))
                            del newData[serverId]["CHANNELS"][channelId]["SUBS_BY_HOUR"][hour][subIndex]




    data = copy.deepcopy(newData) #update reference data dictionary for next stage, will continue to make edits to newData

    #remove channels and servers with no subs
    for serverId in data.keys():
        serverEmpty = True
        for channelId in data[serverId]["CHANNELS"].keys():
            channelEmpty = True
            for hour in data[serverId]["CHANNELS"][channelId]["SUBS_BY_HOUR"].keys():
                if len(data[serverId]["CHANNELS"][channelId]["SUBS_BY_HOUR"][hour]) > 0:
                    channelEmpty = False
                    serverEmpty = False
            if channelEmpty:
                print(f"sub category removed: server: {serverId}, channel: {channelId}")
                del newData[serverId]["CHANNELS"][channelId]
        if serverEmpty:
            print(f"sub category removed: server: {serverId}")
            del newData[serverId]



    print("maintainence complete\n")
    with open("./Data/wikiSubs.json", "w") as file:
        json.dump(newData, file, indent = 4)