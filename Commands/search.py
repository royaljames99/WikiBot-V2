import asyncio
import time

async def run(ctx, sub, searchTerms):

    #toggleable anti swaine defence
    """ 
    if ctx.author.id == 730819280098164786:
        await ctx.send("FUCK OFF SWAINE")
        return
    """
    
    print(f"Command: search in sub: {sub} for values: {searchTerms} at {time.time()}")
    if ctx.message != None:
        #Reg command

        try:
            sub = ctx.message.content.upper().strip().split(" ")[1]
            searchTerms = ctx.message.content.upper().strip().split(" ")[2:]
        except:
            await ctx.send("INVALID COMMAND")
            return

    else:
        #Slash command
        sub = sub.replace(" ", "_")
    
    if sub.upper() == "WIKI":
        import InternalCommands.searchW as searchW
        asyncio.create_task(searchW.run(ctx, searchTerms))
    else:
        from InternalCommands import checkSub, searchFW
        valid = await asyncio.create_task(checkSub.run(sub))
        if valid:
            asyncio.create_task(searchFW.run(ctx, sub, searchTerms))
        else:
            await ctx.send("INVALID SUB")