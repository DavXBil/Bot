import discord
import os

from discord.ext import commands,tasks

from YoutubeDL import YTDLSource


class Music(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="play")
    async def playUrl(self, ctx):
        
        await print('wow')

    @playUrl.before_invoke
    async def checkConnectionToVoiceChannel(self, ctx):

        userInVoiceChannel = ctx.author.voice
        botInVoiceChannel = ctx.voice_client

        if not userInVoiceChannel:
            await ctx.send("You're not connected to a voice channel")
        elif not botInVoiceChannel:
            await userInVoiceChannel.channel.connect()

    @commands.command(name="leave")
    async def leaveVoiceChannel(self, ctx):

        await ctx.voice_client.disconnect()

    @commands.command(name="test")
    async def test(self, ctx):
        
        testVariable = ctx.voice_client

        print(testVariable)