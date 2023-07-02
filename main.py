import os
import discord
from random import random
from dotenv import load_dotenv
from discord.ext import commands
from time import sleep

load_dotenv('token.env')  # Load environment variables from TOKEN.env file
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)


#
# Bot events
#

# checking connection to server
@bot.event
async def on_ready():
    global guild
    for guild in bot.guilds:
        if guild.name == guild:
            break

    # Print bot connection
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    # Check if commands are working
    try:
        synced = await bot.tree.sync()
        print(f"Synced {synced} command(s)")
    except Exception as error:
        print(error)

    print(f"Active discord members in {guild}:")
    for member in guild.members:
        print(member.name)


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
@bot.tree.command(name="lenny", description="( ͡° ͜ʖ ͡°)")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hey {interaction.user.mention} here is your ( ͡° ͜ʖ ͡°)", ephemeral=True)


@bot.tree.command(name="ping", description="Display KiraBot's latency")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f'My Ping is {round(bot.latency * 1000)}ms')


#
# Music player
#


# Run KiraBot
bot.run(TOKEN)
