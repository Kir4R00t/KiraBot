import os
import discord
import random
import interactions
import requests
from dotenv import load_dotenv
from discord.ext import commands
from time import sleep

load_dotenv('token.env')
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)


#
# Connection & commands sync
#

@bot.event
async def on_ready():
    global guild
    for guild in bot.guilds:
        if guild.name == guild:
            break

    # Bot connection info
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    # Commands sync
    try:
        synced = await bot.tree.sync()
        print(f"Synced {synced} command(s)")
    except Exception as error:
        print(error)

    print(f"Active discord members in {guild}:")
    for member in guild.members:
        print(member.name)


#
# Bot commands
#


# Lennyface
@bot.tree.command(name="lenny", description="( ͡° ͜ʖ ͡°)")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hey {interaction.user.mention} here is your ( ͡° ͜ʖ ͡°)", ephemeral=True)


# Ping
@bot.tree.command(name="ping", description="Pong!")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("pong!", ephemeral=True)


# Coinflip
@bot.tree.command(name="coinflip", description="Flip a coin")
async def coinflip(interaction: discord.Interaction):
    coin = random.randint(1, 2)
    if coin == 1:
        await interaction.response.send_message("Heads", ephemeral=True)
    else:
        await interaction.response.send_message("Tails", ephemeral=True)


# RTD
@bot.tree.command(name="rtd", description="Roll the dice")
async def coinflip(interaction: discord.Interaction):
    dice = random.randint(1, 6)
    await interaction.response.send_message(f"You have rolled {dice}", ephemeral=True)


# TEST
@bot.tree.command(name="test", description="test command")
async def test(interaction: discord.Interaction):
    await interaction.response.send_message(f"you are on server {guild}")


# GeoIP TODO: Add API error handling
@bot.tree.command(name="whois", description="Get info about given IP")
async def whois(interaction: discord.Interaction, ip: str):
    url = f"http://ip-api.com/json/{ip}"
    response = requests.get(url)
    data = response.json()

    country = data['country']
    city = data['city']
    region = data['region']
    isp = data['isp']

    await interaction.response.send_message(f'Country: {country} ||| ' f'Region: {region} ||| ' f'City: {city} ||| ' f'ISP: {isp} ||| ', ephemeral=True)

# Run KiraBot
bot.run(TOKEN)
