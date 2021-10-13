from os import name
import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_option
import asyncio

class wikiSubComms(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    ##SUBSCRIBE##
    @commands.command()
    async def subwiki(self, ctx):
        pass
    @cog_ext.cog_slash(
        name = "subwiki",
        description = "Setup a daily wiki subscription",
        options = [
            create_option(
                name = "sub",
                description = "Fandom subwiki (found in url, use wiki for default wikipedia)",
                required = True,
                option_type = 3
            ),
            create_option(
                name = "time",
                description = "Time for the wiki to send (mm:hh)",
                required = True,
                option_type = 3
            )
        ])
    async def _subWiki(self, ctx, sub, time):
        pass


    ##UNSUBSCRIBE##
    @commands.command()
    async def unsubwiki(self, ctx):
        pass
    @cog_ext.cog_slash(
        name = "unsubwiki",
        description = "Remove a daily wiki subscription",
        options = [
            create_option(
                name = "index",
                description = "Index of subscription to remove",
                required = True,
                option_type = 4
            )
        ])
    async def _unSubWiki(self, ctx, index):
        pass


    ##SHOWSUBS##
    @commands.command()
    async def showsubs(self, ctx):
        pass
    @cog_ext.cog_slash(name = "showsubs", description = "Show all wiki subscriptions for this channel")
    async def _showsubs(self, ctx):
        pass