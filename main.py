import os
import discord
from dotenv import load_dotenv

load_dotenv('token.env')  # Load environment variables from TOKEN.env file
TOKEN = os.getenv('TOKEN')
GUILD = os.getenv('HYPIXEL FF')


client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    # Print bot connection
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

client.run(TOKEN)
