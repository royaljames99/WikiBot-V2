import asyncio
import time

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
        print(sub)
    
    if sub.upper() == "WIKI":
        import InternalCommands.genW as genW
        asyncio.create_task(genW.run(ctx))
    else:
        from InternalCommands import checkSub, genFW
        valid = await asyncio.create_task(checkSub.run(sub))
        if valid:
            asyncio.create_task(genFW.run(ctx, sub))
        else:
            ctx.send("INVALID SUB")