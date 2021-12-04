import discord
from discord.ext import commands, tasks
from discord_slash import SlashCommand, SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_option

import Commands.subwiki as subwiki
import Commands.unsubwiki as unsubwiki
import Commands.showsubs as showsubs
import InternalCommands.wikiLoop as wikiLoop
import InternalCommands.routineMaintainence as maintainence

import asyncio

class wikiSubComms(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.wikiLoop.start()


    ##WIKILOOP##
    @tasks.loop(minutes = 1)
    async def wikiLoop(self):
        asyncio.create_task(wikiLoop.run(self.bot))


    #DAILY MAINTAINENCE
    @tasks.loop(hours = 24)
    async def routineMaintainence(self):
        asyncio.create_task(maintainence.run(self.bot))
    

    ##SUBSCRIBE##
    @commands.command(description = "Adds a daily wiki subscription to this channel", help = "Adds a daily wiki subscription for a sub at a given time (use wiki for default wikipedia)\n```wb!subwiki <sub> <time (hh:mm)>```")
    async def subwiki(self, ctx):
        asyncio.create_task(subwiki.run(ctx, None, None))
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
        asyncio.create_task(subwiki.run(ctx, sub, time))


    ##UNSUBSCRIBE##
    @commands.command(description = "Removes daily wiki subscription from this channel", help = "Removes a daily wiki subscription using index from showsubs command\n```wb!unsubwiki <index>```")
    async def unsubwiki(self, ctx):
        asyncio.create_task(unsubwiki.run(ctx, None))
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
        asyncio.create_task(unsubwiki.run(ctx, index))


    ##SHOWSUBS##
    @commands.command(description = "Shows list of all wiki subscriptions in this channel", help = "Shows list of all wiki subscription in this channel\n```wb!showsubs```")
    async def showsubs(self, ctx):
        asyncio.create_task(showsubs.run(ctx))
    @cog_ext.cog_slash(name = "showsubs", description = "Show all wiki subscriptions for this channel")
    async def _showsubs(self, ctx):
        asyncio.create_task(showsubs.run(ctx))