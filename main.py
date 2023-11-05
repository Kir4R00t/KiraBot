import os
import discord
import random
import interactions
import yt_dlp
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


# reactions to messages
@bot.event
async def on_message(message):
    # Wiktor
    if message.author.name == 'w12k':
        await message.channel.send('Jestes dupa')

    # co ? > dupa
    def randomowo():
        liczba = random.random()

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
    if message.content == "Wiktor kurwa chodz" and message.author != "w12k":
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


#
# TEST COMMANDS
#

@bot.tree.command(name="test", description="test command")
async def test(interaction: discord.Interaction):
    await interaction.response.send_message(f"you are on server {guild}")


#
# MUSIC PLAYER (shit is not working currently)
#

@bot.tree.command(name="play", description="Play music from youtube !")
async def play(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['url']

    voice_channel = ctx.author.voice.channel
    voice_client = await voice_channel.connect()
    voice_client.play(discord.FFmpegPCMAudio(url2, options="-ar 48000"))


@bot.tree.command(name="stop", description="Stop the music player")
async def stop(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client
    if voice_client and voice_client.is_playing():
        voice_client.stop()
        await voice_client.disconnect(force=True)
    else:
        await interaction.response.send_message("KiraB0t is not playing music rn bruh", ephemeral=True)


# Run KiraBot
bot.run(TOKEN)
