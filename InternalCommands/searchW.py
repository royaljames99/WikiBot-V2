import requests
import discord

session = requests.session()

async def run(ctx, searchTerms):

    title = "Loading..."
    description = "...."
    embed = discord.Embed(title = title, description = description)
    msg = await ctx.send(embed = embed)

    req = session.get(f"https://en.wikipedia.org/w/api.php?action=opensearch&namespace=0&search={searchTerms}&limit=10&format=json")

    data = req.json()

    results = []
    for i in range(len(data[1])):
        results.append([data[1][i], data[3][i]])

    title = f"SEARCH RESULTS FOR {searchTerms.upper()}"
    description = ""
    count = 0
    for i in results:
        count += 1
        description += f"{count}. [{i[0]}]({i[1]})\n"
    
    embed = discord.Embed(title = title, description = description)
    msg = await msg.edit(embed = embed)