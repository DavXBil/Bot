import os


from discord.ext import commands
from dotenv import load_dotenv

from Classes.music_cog import Music


load_dotenv()
load_dotenv(".env", verbose=True)

token = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix = '!')

bot.add_cog(Music(bot))

@bot.event
async def on_ready():
    """Message when bot is ready"""
    print('ready')

bot.run(token)
