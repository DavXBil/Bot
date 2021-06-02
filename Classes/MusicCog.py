import asyncio

import discord
import os

from discord.ext import commands,tasks

from .YoutubeDL import YTDLSource

class UserNotInVoiceChannelError(Exception):
    pass


class Music(commands.Cog):

    def __init__(self, bot: commands.Bot):

        self.bot = bot
   

    @commands.command(name="play")
    async def playSongFromUrl(self, ctx, *,search: str):

        voiceClient = ctx.voice_client

        async with ctx.typing():

            source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop)

            voiceClient.play(source)


    @commands.command(name="pause")
    async def pauseSong(self, ctx):
        
        voiceClient = ctx.voice_client

        if voiceClient.is_paused():
            await ctx.send("Song already paused")
        else:
            voiceClient.pause()

    
    @commands.command(name="stop")
    async def stopSong(self, ctx):

        voiceClient = ctx.voice_client

        if voiceClient.is_playing():
            voiceClient.stop()

        else:
            await ctx.send("Nothing to stop")

    @commands.command(name='resume')
    async def resumeSong(self, ctx):

        voiceClient = ctx.voice_client

        if voiceClient.is_paused():   
            voiceClient.resume()

        elif voiceClient.is_playing():
            await ctx.send("Song is not paused")

        else:
            await ctx.send("No Song is playing")   


    @playSongFromUrl.before_invoke
    async def checkConnectionToVoiceChannel(self, ctx):

        userInVoiceChannel = ctx.author.voice
        botInVoiceChannel = ctx.voice_client

        if not userInVoiceChannel:
            await ctx.send("You're not connected to a voice channel")
            raise UserNotInVoiceChannelError()
            
        else:

            if botInVoiceChannel:
                await ctx.send("I'm already in a voice chat")
                return
            else:
                await userInVoiceChannel.channel.connect()


    @commands.command(name="leave")
    async def leaveVoiceChannel(self, ctx):

        await ctx.voice_client.disconnect()


    @commands.command(name="test")
    async def test(self, ctx):

        await ctx.send("bonjour")
