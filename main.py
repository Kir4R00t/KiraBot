import os
import discord
from random import random
from dotenv import load_dotenv
from discord.ext import commands
from time import sleep

load_dotenv('token.env')  # Load environment variables from TOKEN.env file
TOKEN = os.getenv('TOKEN')
GUILD = os.getenv('HYPIXEL FF')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)


#
# Functions
#


#
# Bot events
#

# checking connection to server
@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    # Print bot connection
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )


# reactions to messages
@bot.event
async def on_message(message):
    # Candice
    if message.content == 'Hey KiraBot do you know candice ?':
        await message.channel.send('YOUR MOTHER HUNG HERSELF 🔥🔥💀💀')

    # Wiktor
    if message.author.name == 'w12k':
        await message.channel.send('Jestes dupa')

    # co ? > dupa
    def randomowo():
        liczba = random()

        if liczba < 0.3:
            return "dupa"
        elif 0.3 < liczba < 0.6:
            return "gowno"
        else:
            return "sranie"

    if not message.content == "co":
        if 'co ' in message.content:
            await message.channel.send(randomowo())
    else:
        await message.channel.send(randomowo())

    # Wiktor kurwa chodz
    if message.content == "Wiktor kurwa chodz":
        username = "w12k"
        guild = message.guild
        member = discord.utils.find(lambda m: m.name == username, guild.members)
        if member is not None:
            mention = member.mention
            for i in range(15):
                await message.channel.send(f"{mention} kurwa chodz")
                sleep(0.5)
    await bot.process_commands(message)


#
# Bot commands
#

# Lennyface
@bot.command()
async def lenny(ctx):
    await ctx.send("( ͡° ͜ʖ ͡°)")


#
# Music player
#


# Run KiraBot
bot.run(TOKEN)
