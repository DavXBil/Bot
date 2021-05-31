import discord
import os

from discord.ext import commands,tasks

from .YoutubeDL import YTDLSource

class UserNotInVoiceChannel(Exception):
    pass


class Music(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="play")
    async def playSongFromUrl(self, ctx, *,search: str):

        source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop)
        
        await ctx.voice_client.play(source)

    @commands.command(name="pause")
    async def pauseSong(self, ctx):
        
        song = ctx.voice_client

        if(song.is_paused()):
            await ctx.send("Song already paused")
        else:
            await song.pause()
    
    @commands.command(name="stop")
    async def stopSong(self, ctx):
        
        song = ctx.voice_client

        await song.stop()

    @playSongFromUrl.before_invoke
    async def checkConnectionToVoiceChannel(self, ctx):

        userInVoiceChannel = ctx.author.voice
        botInVoiceChannel = ctx.voice_client

        print(userInVoiceChannel) 
        print(botInVoiceChannel)

        if not userInVoiceChannel:
            await ctx.send("You're not connected to a voice channel")
            raise commands.CommandError()
            
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
        
        testVariable = ctx.voice_client

        print(testVariable)
