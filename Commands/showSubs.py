import asyncio
import json
import InternalCommands.timeStampOps as timestamp
import discord

async def run(ctx):
    serverId = ctx.guild.id
    strServerId = str(serverId)

    channelId = ctx.channel.id
    strChannelId = str(channelId)

    #get subs for channel
    with open("./Data/wikiSubs.json", "r") as file:
        data = json.load(file)
    
    try:
        server = data[strServerId]

        try:
            channel = server["CHANNELS"][strChannelId]

        except KeyError:
            await ctx.send("There are no subscriptions for this channel")
            return

    except KeyError:
        await ctx.send("There are no subsciptions on this server")
        return
    
    #extract subs
    subs = []
    for key in channel["SUBS_BY_HOUR"]:
        for sub in channel["SUBS_BY_HOUR"][key]:
            subs.append(sub)

    #format subs for display
    text = ""
    count = 0
    for sub in subs:
        count += 1

        #get subscriber name
        name = await ctx.bot.fetch_user(sub["SUBSCRIBER_ID"]).name
        wikiSub = sub["SUB"]
        time = await asyncio.create_task(timestamp.getStampFromAddon(sub["TIME"]))

        #format
        text += f"{str(count)}.\n    SUB: {wikiSub}\n    TIME: {time}\n    SUBSCRIBER: {name}\n"

    #send
    embed = discord.Embed(title = "WIKI SUBS FOR THIS CHANNEL:", description = text)
    await ctx.send(embed = embed)