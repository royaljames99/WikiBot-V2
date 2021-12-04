import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_option
import asyncio

class generalComms(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    ##PING##
    @commands.command(description = "ping", help = "It pongs\n```wb!ping```")
    async def ping(self, ctx):
        import Commands.ping as ping
        asyncio.create_task(ping.run(ctx))
    @cog_ext.cog_slash(name = "ping", description = "Pongs to your ping")
    async def _ping(self, ctx):
        import Commands.ping as ping
        asyncio.create_task(ping.run(ctx))