import discord
from discord.ext import commands
from discord_slash import SlashCommand
import importlib
import os
from dotenv import load_dotenv

load_dotenv()

#init bot
bot = commands.Bot(command_prefix = "wb!") #https://stackoverflow.com/questions/56796991/discord-py-changing-prefix-with-command eventually implement this
slash = SlashCommand(bot, sync_commands=True)

#load cogs
bot.add_cog(importlib.import_module("Cogs.basicWikiComms").basicComms(bot))
bot.add_cog(importlib.import_module("Cogs.generalComms").generalComms(bot))
bot.add_cog(importlib.import_module("Cogs.wikiSubComms").wikiSubComms(bot))

#on_ready
@bot.event
async def on_ready():
    print("woo")

#run it motherfuckers
bot.run(os.getenv("token"))