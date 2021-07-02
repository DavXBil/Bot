import asyncio

import discord
import os

from discord.ext import commands,tasks

from .YoutubeDL import YTDLSource
from .Queue import SongQueue
from.AudioPlayer import AudioPlayer

class UserNotInVoiceChannelError(Exception):
    pass


class Music(commands.Cog):

    def __init__(self, bot: commands.Bot):

        self.bot = bot
        self.audio_players = {}

    
    def get_audio_player(self, ctx: commands.Context):

        state = self.audio_players.get(ctx.guild.id)

        if not state:
            state = AudioPlayer(self.bot, ctx)

            self.audio_players[ctx.guild.id] = state

        return state

    
    async def cog_before_invoke(self, ctx: commands.Context):
        ctx.audio_player = self.get_audio_player(ctx)


    @commands.command(name="play")
    async def playSongFromUrl(self, ctx, *, search: str):

        async with ctx.typing():

            source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop)

            await ctx.audio_player.songs.put(source)

            if ctx.voice_client.is_playing():
                await ctx.send("Song has been put to Queue")


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
            await ctx.audio_player.stop()

        else:
            await ctx.send("Nothing to stop")

    
    @commands.command(name="skip")
    async def skipSong(self, ctx):
        
        ctx.audio_player.skip()
             

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

            if not botInVoiceChannel:
                await userInVoiceChannel.channel.connect()


    @commands.command(name="leave")
    async def leaveVoiceChannel(self, ctx):

        await ctx.voice_client.disconnect()


    @commands.command(name="test")
    async def test(self, ctx):

        userInVoiceChannel = ctx.author.voice
        botInVoiceChannel = ctx.voice_client

        print(userInVoiceChannel)
        print(botInVoiceChannel)
