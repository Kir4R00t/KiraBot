import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv('token.env')  # Load environment variables from TOKEN.env file
TOKEN = os.getenv('TOKEN')
GUILD = os.getenv('HYPIXEL FF')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)


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


@bot.event
async def on_message(message):
    # Candice
    if message.content == 'Hey KiraBot do you know candice ?':
        await message.channel.send('YOUR MOTHER HUNG HERSELF 🔥🔥💀💀')

    # Wiktor
    if message.author.name == 'w12k':
        await message.channel.send('Jestes dupa')

    await bot.process_commands(message)


@bot.command()
async def lenny(ctx):
    await ctx.send("( ͡° ͜ʖ ͡°)")


bot.run(TOKEN)
