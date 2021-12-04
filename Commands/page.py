import asyncio
import requests
import discord
import InternalCommands.genW as genW
import InternalCommands.genFW as genFW


async def run(ctx, sub, pageName):
    #handle non slash commands
    if sub == None:
        try:
            sub = ctx.message.content.upper().strip().split(" ")[1]
        except:
            await ctx.send("INVALID COMMAND")
        try:
            pageName = "_".join(ctx.message.content.strip().split(" ")[2:])
        except:
            pageName = None
    
    else:
        sub = sub.replace(" ", "_")

    print(sub, pageName)

    embed = discord.Embed(title = "Working.....", description = ".")
    msg = await ctx.send(embed = embed)

    if sub.upper() == "WIKI":
        asyncio.create_task(genW.run(msg, pageName))
    else:
        asyncio.create_task(genFW.run(msg, sub, pageName))