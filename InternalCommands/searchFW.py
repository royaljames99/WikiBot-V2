import requests
import discord

session = requests.session()

async def run(ctx, sub, searchTerms):
    
    title = "Loading..."
    description = "...."
    embed = discord.Embed(title = title, description = description)
    msg = await ctx.send(embed = embed)

    req = session.get(f"https://{sub}.fandom.com/api.php?action=query&format=json&prop=info&generator=prefixsearch&inprop=url&gpssearch={searchTerms}&gpsnamespace=0&gpslimit=10")

    data = req.json()

    pages = data["query"]["pages"]

    results = []
    for i in pages.keys():
        results.append([pages[i]["title"], pages[i]["fullurl"]])
    
    title = f"SEARCH RESULTS FOR {searchTerms.upper()} IN {sub.upper()}"

    description = ""
    counter = 0
    for i in results:
        counter += 1
        description += f"{counter}. [{i[0]}]({i[1]})\n"

    embed = discord.Embed(title = title, description = description)
    msg = await msg.edit(embed = embed)