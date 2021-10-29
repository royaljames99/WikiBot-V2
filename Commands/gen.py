import asyncio
import time
import discord

async def run(ctx, sub):

    #toggleable anti swaine defence
    """ 
    if ctx.author.id == 730819280098164786:
        await ctx.send("FUCK OFF SWAINE")
        return
    """

    print(f"Command: gen in sub: {sub} at {time.time()}")
    if ctx.message != None:
        #Reg command

        try:
            sub = ctx.message.content.upper().strip().split(" ")[1]
        except:
            await ctx.send("INVALID COMMAND")

    else:
        #Slash command
        sub = sub.replace(" ", "_")

    msg = await ctx.send(embed = discord.Embed(title = "Working.....", description = "."))
    
    if sub.upper() == "WIKI":
        import InternalCommands.genW as genW
        asyncio.create_task(genW.run(msg))
    else:
        from InternalCommands import checkSub, genFW
        valid = await asyncio.create_task(checkSub.run(sub))
        if valid:
            asyncio.create_task(genFW.run(msg, sub))
        else:
            ctx.send("INVALID SUB")