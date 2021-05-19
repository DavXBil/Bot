import discord
import os

from discord.ext import commands,tasks
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix = '!')

@bot.command(name="test")
async def test(ctx):
    await ctx.send('hello')

bot.run(token)