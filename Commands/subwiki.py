import asyncio
import json
import InternalCommands.timeStampOps as timestamp
import InternalCommands.checkSub as checkSub
import discord

async def run(ctx, sub, time):
    
    if ctx.message != None:
        #reg command
        try:
            sub = ctx.message.content.upper().strip().split(" ")[1]
            time = ctx.message.content.upper().strip().split(" ")[2]
        except:
            await ctx.send("INVALID COMMAND")
            return

    else:
        pass

    try:
        if int(time[3:4]) > 59 or int(time[3:4]) < 0 or int(time[0:1]) > 23 or int(time[0:1]) < 0:
            await ctx.send("INVALID TIME")
            return
    except:
        await ctx.send("INVALID TIME")
        return
    hour = time[0:1]

    if sub.upper() != "WIKI":
        valid = asyncio.create_task(checkSub.run(sub))
        if not valid:
            await ctx.send("INVALID SUB")
            return
    

    #assemble sub
    timeStamp = await asyncio.create_task(timestamp.getTimeAddon(time))
    subToAdd = {"SUB": sub, "TIME": timeStamp, "SUBSCRIBER_ID": ctx.author.id}

    #load sub data
    with open("./Data/wikiSubs.json", "r") as file:
        data = json.load(file)


    ###############JUST DON'T LOOK BELOW FOR YOUR OWN SANITY###############

    #add the sub
    strServerId = str(ctx.guild.id)
    strChannelId = str(ctx.channel.id)
    
    #check if sub for server already exists
    found = False
    for key in data:
        if key == strServerId:
            found = True
    
    if found:

        #check if server sub limit reached
        ####TO DO####

        #check if user is authorised
        ####TO DO####

        #check if channel already exists
        found2 = False
        for key in data[strServerId]["CHANNELS"]:
            if key == strChannelId:
                found2 = True
        
        if found2:
            
            #check if channel sub limit reached
            ####TO DO####

            #check if hour exists
            found3 = False
            for key in data[strServerId]["CHANNELS"][strChannelId]["SUBS_BY_HOUR"]:
                if key == hour:
                    found3 = True
            
            if found3:
                data[strServerId]["CHANNELS"][strChannelId]["SUBS_BY_HOUR"][hour].append(subToAdd)
            else:
                data[strServerId]["CHANNELS"][strChannelId]["SUBS_BY_HOUR"][hour] = [subToAdd]
        
        else:
            data[strServerId]["CHANNELS"][strChannelId] = {"CHANNELCAP": -1, "SUBS_BY_HOUR": {hour:[subToAdd]}}
    else:
        data[strServerId] = {"SERVERCAP": 5, "AUTHORISED_USERS": [], "CHANNELS":{strChannelId: {"CHANNELCAP": -1, "SUBS_BY_HOUR": {hour: [subToAdd]}}}}


    with open("./Data/wikiSubs.json", "w") as file:
        json.dump(data, file, indent = 4)

    await ctx.send("DONE")
    print(f"wiki subscription for server [{ctx.guild.id}] channel [{ctx.channel.id}] with sub [{sub}] added by user [{ctx.author.name}]")