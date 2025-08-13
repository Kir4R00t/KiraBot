import os
import discord
import random
import json
import logging
import requests

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from discord.ext import commands
from time import sleep

load_dotenv('.env')
BOT_TOKEN = os.getenv('DISCORD')

intents = discord.Intents.default()
intents.message_content = True

# This has no use for now basically
bot = commands.Bot(command_prefix='!', intents=intents)

logger = logging.getLogger(__name__)

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
    logger.info(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    # Commands sync
    try:
        logger.info("Synced commands: \n")
        synced = await bot.tree.sync()
        for x in synced:
            logger.info(f'{x}\n')
        if synced is None:
            logger.info(f'{x} is not synced\n')

    except Exception as error:
        logger.info(error)

    logger.info(f"Active discord members in {guild}:")
    for member in guild.members:
        logger.info(f'{member.name}\n')


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
async def rtd(interaction: discord.Interaction):
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
    load_dotenv('.env')
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
    load_dotenv('.env')
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

@bot.tree.command(name="trade", description="Issue a query to poe2 trade API")
async def trade(interaction: discord.Interaction, query: str): # , id: str
    load_dotenv('.env')
    
    # API endpoint
    base_url = "https://www.pathofexile.com/api/trade2/"
    search_url = base_url + "search/poe2/Standard"
    fetch_url = base_url + "fetch/"
    poe_session_id = os.getenv('POE_SESSION_ID')

    # Headers
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': '5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'Cookie': f'POESESSID={poe_session_id}',
        'Accept': '*/*',
        'Connection': 'keep-alive'
    }

    # Parse query JSON & query ID
    id = "youcanputwhateverinhere"
    raw_query_json = query
    query_id = id

    try:
        query = json.loads(raw_query_json)
        query['id'] =  query_id

    except json.JSONDecodeError as e:
        logger.info(f"Invalid JSON: {e}")
        exit()

    # Send search request
    try:
        response = requests.post(search_url, headers=headers, json=query)
        logger.info(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            response_json = response.json()
            logger.info("Search successful. First few results:")
            logger.info(json.dumps(response_json.get("result", [])[:10], indent=2))
        else:
            logger.info(f"Error Response: {response.text}")
            exit()
    except Exception as e:
        logger.info(f"Error sending search request: {e}")
        exit()

    # Fetch item details
    result_ids = response_json.get("result", [])[:10]
    if not result_ids:
        logger.info("No results found.")
        exit()

    result_ids_combined = ",".join(result_ids)
    fetch_snippet = f"{result_ids_combined}?query={query_id}"
    full_fetch_url = fetch_url + fetch_snippet

    # Send fetch request
    try:
        response = requests.get(full_fetch_url, headers=headers)
        logger.info(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            logger.info("Fetched item data:")
            logger.info(json.dumps(data, indent=2))
        
            embeds = []

            for result in data['result']:
                item = result.get("item", {})
                listing = result.get("listing", {})
                account = listing.get("account", {}).get("name", "Unknown")
                price = listing.get("price", {})
                mods = item.get("explicitMods", [])
                enchant = item.get("enchantMods", [])
                icon_url = item.get("icon")

                # Create embed for this item
                embed = discord.Embed(
                    title=f"{item.get('name', '')} {item.get('typeLine', '')}",
                    description=(
                        f"**iLvl**: {item.get('ilvl')}\n"
                        f"**League**: {item.get('league')}\n"
                        f"**Corrupted**: {item.get('corrupted')}\n"
                        f"**Note**: {item.get('note', 'N/A')}"
                    ),
                    color=discord.Color.gold()
                )
                embed.set_thumbnail(url=icon_url)
                embed.set_footer(text=f"Seller: {account} | Price: {price.get('amount')} {price.get('currency')}")

                if mods:
                    embed.add_field(
                        name="Explicit Mods",
                        value="\n".join(f"- {mod}" for mod in mods),
                        inline=False
                    )

                if enchant:
                    embed.add_field(
                        name="Enchant Mods",
                        value="\n".join(f"- {mod}" for mod in enchant),
                        inline=False
                    )

                embeds.append(embed)

            # Send first embed using interaction.response
            if embeds:
                await interaction.response.send_message(embed=embeds[0], ephemeral=False)
                
                # Send the rest
                '''for embed in embeds[1:]:
                    await interaction.followup.send(embed=embed)'''
            else:
                await interaction.response.send_message("No items found.", ephemeral=True)


            sleep(5)  # Avoid hammering the server
        else:
            logger.info(f"Error Response: {response.text}")
    except Exception as e:
        logger.info(f"Error fetching item data: {e}")

@bot.tree.command(name="show", description="Showoff your item from poe2, mouse over your item in poe2 and ctrl + c to get the item data")
async def show(interaction: discord.Interaction, item_data: str):

    item_data = item_data.split('\n')
    
    for line in item_data:
        if "Item Class" in line:
            item_class = line
        if "Rarity" in line:
            item_rarity = line
    
    embed = discord.Embed(
        title = "item_title",
            description=(
                'description'
            ),
        color=discord.Color.gold()
    )

    embed.add_field(
        name='Item Stats:',
        value='\n'.join(f'- {line}' for line in item_data),
        inline=False
    )
    
    try:
        await interaction.response.send_message(embed=embed, ephemeral=False)
    except Exception as e:
        logger.info(f'Exception: {e}')

# Run KiraBot
bot.run(BOT_TOKEN)
