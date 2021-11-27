import asyncio

from .queue import SongQueue
from .song import Embed

class VoiceError(Exception):
    pass

class AudioPlayer:
    """Manage the song reading"""
    def __init__(self, bot, ctx):

        self.bot = bot
        self._ctx = ctx

        self.current = None
        self.voice = ctx.voice_client
        self.next = asyncio.Event()
        self.songs = SongQueue()

        self.audio_player = bot.loop.create_task(self.player_task())


    async def player_task(self):
        """plays the song, displays song informations"""
        while True:

            self.next.clear()

            self.current = await self.songs.get()

            embed = Embed(self.current)

            self.voice.play(self.current, after=self.play_next_song)

            await self._ctx.send(embed=embed.create_embed())

            await self.next.wait()


    def play_next_song(self, error=None):
        """plays next song"""
        if error:
            raise VoiceError(str(error))

        self.next.set()


    def skip(self):
        """skip the current playing song"""
        if self.voice.is_playing:
            self.voice.stop()


    async def stop(self):
        """stops song playing, call clear method from SongQueue class"""
        self.songs.clear()
        self.voice.stop()
