import os
import discord
import random
import interactions
import requests
from dotenv import load_dotenv
from discord.ext import commands
from time import sleep

load_dotenv('token.env')
BOT_TOKEN = os.getenv('DISCORD')

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
        for x in synced:
            print(f'{x}\n')
    except Exception as error:
        print(error)

    print(f"Active discord members in {guild}:")
    for member in guild.members:
        print(f'{member.name}\n')


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


# GeoIP
@bot.tree.command(name="whois", description="Get info about given IP")
async def whois(interaction: discord.Interaction, ip: str):
    url = f"http://ip-api.com/json/{ip}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()

        country = data['country']
        city = data['city']
        isp = data['isp']
    else:
        await interaction.response.send_message(f'Error: no data for {ip}', ephemeral=True)
    
    await interaction.response.send_message(f'Country: {country}  |  ' f'City: {city}  |  ' f'ISP: {isp}  |  ', ephemeral=True)

# Weather
@bot.tree.command(name="weather", description="Get weather info about given city")
async def weather(interacion: discord.Interaction, city: str):
    load_dotenv('token.env')
    api_key = os.getenv('OPENWEATHER')

    url = f'https://api.openweathermap.org/data/2.5/weather?&q={city}&units=metric&appid=' + api_key

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temperature = data['main']['temp']
        humidy = data['main']['humidity']

        if 'wind' in data:
            wind_speed = data['wind']['speed']
        else:
            wind_speed = "No wind data"
    else:
        await interacion.response.send_message(f'Error: no data for {city}', ephemeral=True)

    await interacion.response.send_message(f'Weather data for {city}  >>> | 'f'Temperature: {temperature}°C  |  ' f'Humidity: {humidy}%  |  ' f'Wind speed: {wind_speed}m/s  ', ephemeral=True)

# Run KiraBot
bot.run(BOT_TOKEN)
