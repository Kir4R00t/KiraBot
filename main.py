import os
import discord
import random
import interactions
import requests
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from discord.ext import commands
from time import sleep

load_dotenv('token.env')
BOT_TOKEN = os.getenv('DISCORD')

intents = discord.Intents.default()
intents.message_content = True

# This has no use for now basically
bot = commands.Bot(command_prefix='!', intents=intents)


#
# Connection & Commands sync
#

@bot.event
async def on_ready():
    # Main bot guild (which is a serer of two ppl :v)
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
        print("Synced commands: \n")
        synced = await bot.tree.sync()
        for x in synced:
            print(f'{x}\n')
        if synced is None:
            print(f'{x} is not synced\n')

    except Exception as error:
        print(error)

    print(f"Active discord members in {guild}:")
    for member in guild.members:
        print(f'{member.name}\n')


#
# Bot reactions
#

# Yeah I know I am a comedy genius
@bot.event
async def on_message(message):
    if message.content.lower() == 'co':
        await message.channel.send("Gówno.")
    if message.content.lower() == 'what':
        await message.channel.send("Gówno.")
    if message.author.name == 'w12k':
        roll = random.randint(1, 10)
        if roll == 3:
            await message.channel.send("jestes dupa")


#
# Bot commands
#

# Lennyface
@bot.tree.command(name="lenny", description="( ͡° ͜ʖ ͡°)")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hey {interaction.user.mention} here is your ( ͡° ͜ʖ ͡°)", ephemeral=False)


# Ping
@bot.tree.command(name="ping", description="Pong!")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("pong!", ephemeral=False)


# Coinflip
@bot.tree.command(name="coinflip", description="Flip a coin")
async def coinflip(interaction: discord.Interaction):
    coin = random.randint(1, 2)
    if coin == 1:
        await interaction.response.send_message("Heads", ephemeral=False)
    else:
        await interaction.response.send_message("Tails", ephemeral=False)


# RTD
@bot.tree.command(name="rtd", description="Roll the dice")
async def coinflip(interaction: discord.Interaction):
    dice = random.randint(1, 6)
    await interaction.response.send_message(f"You have rolled {dice}", ephemeral=False)


# TEST
@bot.tree.command(name="test", description="test command")
async def test(interaction: discord.Interaction):
    await interaction.response.send_message(f"you are on server {guild}")


# GeoIP TODO: Add proper API error handling
@bot.tree.command(name="whois", description="Get info about given IP")
async def whois(interaction: discord.Interaction, ip: str):
    url = f"http://ip-api.com/json/{ip}"
    response = requests.get(url)
    data = response.json()

    country = data['country']
    city = data['city']
    isp = data['isp']

    try:
        await interaction.response.send_message(
            f' >>> ** Country: {country}  |  ' f'City: {city}  |  ' f'ISP: {isp} ** ',
            ephemeral=False)
    except:
        await interaction.response.send_message(f'API Error', ephemeral=False)


# Weather
@bot.tree.command(name="weather", description="Get weather info about given city")
async def weather(interacion: discord.Interaction, city: str):
    load_dotenv('token.env')
    api_key = os.getenv('OPENWEATHER')
    url = f'https://api.openweathermap.org/data/2.5/weather?&q={city}&units=metric&appid={api_key}'
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
        await interacion.response.send_message(f"API ERROR: {response.status_code}", ephemeral=False)

    await interacion.response.send_message(
        f'Weather data for {city}  >>> ** Temperature: {temperature}°C  | Humidity: {humidy}%  | Wind speed: {wind_speed}m/s  **',
        ephemeral=False)


# CATSSS
@bot.tree.command(name="gibcat", description="Get a random image of a cat :3")
async def gibcat(interaction: discord.Interaction):
    load_dotenv('token.env')
    api_key = os.getenv('CAT_API')
    url = f"https://api.thecatapi.com/v1/images/search?&api_key={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        cat_photo_url = (data[0]['url'])
        if data:
            await interaction.response.send_message(cat_photo_url, ephemeral=False)
        else:
            await interaction.response.send_message("No data from API", ephemeral=False)
    else:
        await interaction.response.send_message(f"API ERROR: {response.status_code}", ephemeral=False)


# GTA V Online data
@bot.tree.command(name="gta", description="Get GTA V Online weekly update data")
async def gta(interaction: discord.Interaction):
    # Begin the scroop
    url = "https://www.gtabase.com/grand-theft-auto-v/news/"
    response = requests.get(url)
    pre_soup = BeautifulSoup(response.text, 'html.parser')

    # Find update articles & Get latest update
    updates_container = pre_soup.find('div', class_='com-content-category-blog__items')
    latest_update = updates_container.find('div', class_='com-content-category-blog__item')

    # Overwrite url with latest update
    latest_update_link = latest_update.find('a', href=True)['href']
    url = "https://www.gtabase.com" + latest_update_link
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')

    # that's for final content
    content = {}

    headers = soup.find_all('h2')
    for header in headers:
        section_title = header.get_text(strip=True)
        section_content = []

        # Parse data for each section (sibling = next header)
        for sibling in header.find_next_siblings():
            if sibling.name == 'h2':
                break
            if sibling.name == 'p':
                section_content.append(sibling.get_text(strip=True))
            if sibling.name == 'ul':
                list_items = [li.get_text(strip=True) for li in sibling.find_all('li')]
                section_content.extend(list_items)

        # Put that into a neat dict
        content[section_title] = "\n".join(section_content)

    # Send the content as a message to the channel
    message = ""
    for title, data in content.items():
        message_part = f"**{title}**\n{data}\n"
        message += message_part + "\n"

    await interaction.response.send_message(message, ephemeral=False)


# Run KiraBot
bot.run(BOT_TOKEN)
