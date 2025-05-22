import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from Classes.music_cog import Music


load_dotenv()
load_dotenv(".env", verbose=True)

token = os.getenv('DISCORD_TOKEN')

# Définir les intents pour le bot
intents = discord.Intents.default()
intents.message_content = True  # Activer l'intent pour le contenu des messages, nécessaire pour certains événements

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    """Message when bot is ready"""
    print('ready')
    await bot.add_cog(Music(bot))

bot.run(token)
