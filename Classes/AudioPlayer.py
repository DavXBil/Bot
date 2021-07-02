import asyncio

from async_timeout import timeout

from .Queue import SongQueue
from .Song import Embed

class VoiceError(Exception):
    pass

class AudioPlayer:

    def __init__(self, bot, ctx):

        self.bot = bot
        self._ctx = ctx

        self.current = None
        self.voice = ctx.voice_client
        self.next = asyncio.Event()
        self.songs = SongQueue()
        
        self.audio_player = bot.loop.create_task(self.audio_player_task())


    async def audio_player_task(self):

        while True:
            self.next.clear()
           
            self.current = await self.songs.get()

            embed = Embed(self.current)

            self.voice.play(self.current, after=self.play_next_song)

            await self._ctx.send(embed=embed.create_embed())

            await self.next.wait()


    def play_next_song(self, error=None):
        if error:
            raise VoiceError(str(error))

        self.next.set()


    def skip(self):
        if self.voice.is_playing:
            self.voice.stop()
            

    async def stop(self):
        self.songs.clear()
        self.voice.stop()