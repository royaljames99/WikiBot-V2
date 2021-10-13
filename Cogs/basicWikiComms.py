import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_option
import asyncio

class basicComms(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    ##GEN##
    @commands.command(description = "Generate random wiki from sub", help = "Generate random wiki from sub (use wiki for default wikipedia)\n```wb!gen <sub>```") #Regular
    async def gen(self, ctx):
        import Commands.gen as gen
        asyncio.create_task(gen.run(ctx, None))
    @cog_ext.cog_slash( #Slash
        name = "gen",
        description = "Generate random wiki from sub (use wiki for default wikipedia)",
        options = [
            create_option(
                name = "sub",
                description = "Fandom subwiki (found in url, use wiki for default wikipedia)",
                required = True,
                option_type = 3
            )
        ])
    async def _gen(self, ctx, sub):
        import Commands.gen as gen
        asyncio.create_task(gen.run(ctx, sub))

    
    ##SEARCH##
    @commands.command()
    async def search(self, ctx):
        import Commands.search as search
        asyncio.create_task(search.run(ctx, None))
    @cog_ext.cog_slash(
        name = "search",
        description = "Seach wikipedia (including fandom) for search terms",
        options = [
            create_option(
                name = "sub",
                description = "Fandom subwiki (found in url, use wiki for default wikipedia)",
                required = True,
                option_type = 3
            ),
            create_option(
                name = "search_terms",
                description = "The terms to search by",
                required = True,
                option_type = 3
            )
        ]
    )
    async def _search(self, ctx, sub, search_terms):
        import Commands.search as search
        asyncio.create_task(search.run(ctx, sub, search_terms))