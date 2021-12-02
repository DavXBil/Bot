from discord.ext import commands

from .youtube_dl import YTDLSource
from .audio_player import AudioPlayer

class UserNotInVoiceChannelError(Exception):
    pass


class Music(commands.Cog):
    """Manage the music related commands and the bot connection to voice channel"""
    def __init__(self, bot: commands.Bot):

        self.bot = bot
        self.audio_players = {}


    def get_audio_player(self, ctx: commands.Context):
        """gets the audio player"""
        state = self.audio_players.get(ctx.guild.id)

        if not state:
            state = AudioPlayer(self.bot, ctx)

            self.audio_players[ctx.guild.id] = state

        return state


    async def cog_before_invoke(self, ctx: commands.Context):
        ctx.audio_player = self.get_audio_player(ctx)


    @commands.command(name="play")
    async def play_song_from_url(self, ctx, *, search: str):
        """Plays a song from a youtube url"""
        async with ctx.typing():

            source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop)

            await ctx.audio_player.songs.put(source)

            if ctx.voice_client.is_playing():
                queue_size = len(ctx.audio_player.songs)
                await ctx.send("Song has been put to Queue, There is now " + str(queue_size) + " item(s) in queue.")            



    @commands.command(name="pause")
    async def pause_song(self, ctx):
        """Pauses playing song"""
        voice_client = ctx.voice_client

        if voice_client.is_paused():
            await ctx.send("Song already paused")

        else:
            voice_client.pause()


    @commands.command(name="stop")
    async def stop_song(self, ctx):
        """Calls the stop method from the Audioplayer class"""
        voice_client = ctx.voice_client

        if voice_client.is_playing():
            await ctx.audio_player.stop()

        else:
            await ctx.send("Nothing to stop")


    @commands.command(name="skip")
    async def skip_song(self, ctx):
        """skips the currently playing song"""
        ctx.audio_player.skip()


    @commands.command(name='resume')
    async def resume_song(self, ctx):
        """Resume paused song"""
        voice_client = ctx.voice_client

        if voice_client.is_paused():
            voice_client.resume()

        elif voice_client.is_playing():
            await ctx.send("Song is not paused")

        else:
            await ctx.send("No Song is playing")


    @play_song_from_url.before_invoke
    async def check_connection_to_voice_channel(self, ctx):
        """Check user's connection to a voice channel"""
        user_in_voice_channel = ctx.author.voice
        bot_in_voice_channel = ctx.voice_client

        if not user_in_voice_channel:
            await ctx.send("You're not connected to a voice channel")
            raise UserNotInVoiceChannelError()

        else:

            if not bot_in_voice_channel:
                await user_in_voice_channel.channel.connect()


    @commands.command(name="leave")
    async def leave_voice_channel(self, ctx):
        """Makes the bot leave the voice channel it is connected to"""
        await ctx.voice_client.disconnect()
