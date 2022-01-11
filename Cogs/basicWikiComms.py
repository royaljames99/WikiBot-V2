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
    @commands.command(description = "Search for pages within sub", help = "Search for pages within a sub (use wiki for default wikipedia)\n```wb!search <sub> <searchterms>```")
    async def search(self, ctx):
        import Commands.search as search
        asyncio.create_task(search.run(ctx, None, None))
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
        ])
    async def _search(self, ctx, sub, search_terms):
        import Commands.search as search
        asyncio.create_task(search.run(ctx, sub, search_terms))


    ##PAGE##
    @commands.command(description = "Get summary of a page from its title", help = "Get summary of a page by entering its name (use wiki as sub for default wikipedia)\n```wb!page <sub> <pageName>```")
    async def page(self, ctx):
        import Commands.page as page
        asyncio.create_task(page.run(ctx, None, None))
    @cog_ext.cog_slash(
        name = "page",
        description = "Get summary of wikipedia page from pagename",
        options = [
            create_option(
                name = "sub",
                description = "Fandom subwiki (found in url, use wiki for default wikipedia)",
                required = True,
                option_type = 3
            ),
            create_option(
                name = "pagename",
                description = "The name of the page to be fetched, leave blank for random page",
                required = False,
                option_type = 3
            )
        ])
    async def _page(self, ctx, sub, pagename = None):
        import Commands.page as page
        asyncio.create_task(page.run(ctx, sub, pagename))
