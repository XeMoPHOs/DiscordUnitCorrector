# Discord Unit Corrector Bot
#
# This bot is licenced under the MIT License [Copyright (c) 2018 Wendelstein7]
#
# This is a Discord bot running python3 using the Discord.py library
# This bot will listen for any messages in Discord that contain non-SI units and when detected, reply with the message converted to SI-Units.
# Are you tired of a car that weighs 100 Stones, is 10 feet high, and can drive 50 miles at 5 degrees freedom?
# Worry no more! Your car weighs 0.64t, is 3.05m high, and can drive 80.47km at -15°C from now on!
# Simply add this bot to your server! You can choose to run it yourself or add the version that is updated and hosted by me [Wendelstein 7]

# The unit conversion library was riginally created by ficolas2, https://github.com/ficolas2, 2018/01/21
# The unit conversion library has been modified and updated by ficolas2 and Wendelstein7, https://github.com/Wendelstein7

# Licenced under: MIT License, Copyright (c) 2018 Wendelstein7 and ficolas2

import discord
from discord.ext import commands
import random

import time
import datetime
from datetime import datetime, date
from datetime import timedelta

import unitconversion
import unitpedialib

description = """A Discord bot that corrects non-SI units to SI ones!"""
bot = commands.Bot(command_prefix='!', description=description)

starttime = datetime.now()
longprefix = ':symbols: UnitCorrector | '
shortprefix = ':symbols: '

@bot.event
async def on_ready():
    print('Discord Unit Corrector Bot: Logged in as {} (id: {})\n'.format(bot.user.name, bot.user.id))

@bot.event
async def on_message(message):
    if bot.user.id is not message.author.id and (message.guild is None or (message.guild is not None and discord.utils.get(message.guild.roles, name='imperial certified') not in message.author.roles)):
        processedMessage = unitconversion.process(message.content)
        if processedMessage is not None:
            correctionText = ("I think " + (message.author.name if message.guild is not None else "you") + " meant to say: ```" + processedMessage + "```")
            await message.channel.send(correctionText)
    await bot.process_commands(message)

@bot.command()
async def unitcorrector(ctx):
    """Lists supported units by the unit corrector bot."""
    await ctx.send(shortprefix + 'Unit Corrector\nSupported units are:\n```inch, foot, mile, (all those squared), acre, pint, quart, gallon, foot-pound, pound-force, pound-foot, mph, ounce, pound, stone and degrees freedom```')

@bot.command()
async def uptime(ctx):
    """Shows how long this instance of the bot has been online."""
    await ctx.send(shortprefix + 'Uptime\n```Bot started: {}\nBot uptime: {}```'.format(starttime, (datetime.now() - starttime)))

@bot.command()
async def unitpedia(ctx, search: str):
    """Gives information about an unit. Try !unitpedia mi, !unitpedia litre, !unitpedia °C, etc..."""
    result = unitpedialib.lookup(search)
    if result is not "notfound":
        await ctx.send(embed=result)
    else:
        await ctx.send(shortprefix + 'Sorry, your search query has not returned any results. Try to search using diffrent words or abbreviations.\n\n*Unitpedia is not complete and needs community submissions. If you want to help expand unitpedia, please visit <https://github.com/Wendelstein7/DiscordUnitCorrector>.*')

@bot.command()
async def about(ctx):
    """Shows information about the bot aswell as the relevant version numbers, uptime and useful links."""
    embed = discord.Embed(title="UnitCorrector", colour=discord.Colour(0xffffff), url="https://github.com/Wendelstein7/DiscordUnitCorrector", description="A fully functional public Discord bot that automatically corrects non-SI units (imperial, etc) to SI-ones (metric, etc) This bot will listen for any messages in Discord that contain non-SI units and when detected, reply with the message converted to SI-Units.\n\n*Are you tired of a car that weighs 100 Stones, is 10 feet high, and can drive 50 miles at 5 degrees freedom? Worry no more! Your car weighs 0.64t, is 3.05m high, and can drive 80.47km at -15°C from now on!*")
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/405724335525855232/c8c782f4c2de5d221d4beb203829ed9c.webp?size=256")
    embed.add_field(name=":information_source: **Commands**", value="Please use the `!help` to list all possible commands!")
    embed.add_field(name=":hash: **Developers**", value="**Googly** - Creator and main developer\n**ficolas** - Developer")
    embed.add_field(name=":symbols: **Contributing**", value="Want to help with the bot? You're welcome to do so!\n[Visit our GitHub for more information!](https://github.com/Wendelstein7/KeyStoneBot)")
    embed.add_field(name=":new: **Version information**", value="Bot version: `{}`\nDiscord.py version: `{}`\nPython version: `{}`".format(date.fromtimestamp(os.path.getmtime('keystonebot.py')), discord.__version__, sys.version.split(' ')[0]), inline=True)
    embed.add_field(name=":up: **Uptime information**", value="Bot started: `{}`\nBot uptime: `{}`".format(starttime, (datetime.now() - starttime)), inline=True)
    embed.add_field(name=":free: **Adding the bot**", value="Want to add this bot to **your** server? [Click here to add it!](https://discordapp.com/oauth2/authorize?client_id=405724335525855232&scope=bot&permissions=67619905)")
    await ctx.send(embed=embed)


with open('token', 'r') as content_file: # INFO: To run the bot yourself you must enter your bots private token in a (new) file called 'token'
    content = content_file.read()

bot.run(content)
