import asyncio
import json

async def run(ctx, index):
    
    if ctx.message != None:
        try:
            index = int(ctx.message.content.upper().strip().split(" ")[1])
        except:
            await ctx.send("Invalid Index")
            return

    with open("./Data/wikiSubs.json", "r") as file:
        data = json.load(file)

    strServerId = str(ctx.guild.id)
    strChannelId = str(ctx.channel.id)

    try:
        channelSubs = data[strServerId]["CHANNELS"][strChannelId]["SUBS_BY_HOUR"]
    except KeyError:
        ctx.send("There are no wiki subscriptions in this channel to remove")

    count = 0
    deleted = False
    for key in channelSubs:
        for i in channelSubs[key]:
            count += 1
            if count == index:
                del channelSubs[key][channelSubs[key].index(i)]
                deleted = True
                if len(channelSubs[key]) == 0:
                    channelSubs.pop(key, None)
        if deleted:
            break
    
    if deleted:
        with open("./Data/wikiSubs.json", "w") as file:
            json.dump(data, file, indent = 4)
        await ctx.send("Deleted")
    else:
        await ctx.send("Invalid index")