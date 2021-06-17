import asyncio

from async_timeout import timeout

from .Queue import SongQueue

class VoiceError(Exception):
    pass

class AudioPlayer:

    def __init__(self, bot, ctx):

        self.bot = bot
        self._ctx = ctx
        self.voice = ctx.voice_client
        self.next = asyncio.Event()
        self.songs = SongQueue()
        self.loop = False
        
        self.audio_player = bot.loop.create_task(self.audio_player_task())

    @property
    def loop(self):
        return self._loop

    @loop.setter
    def loop(self, value: bool):
        self._loop = value


    async def audio_player_task(self):

        while True:
            self.next.clear()

            if not self.loop:
                # Try to get the next song within 3 minutes.
                # If no song will be added to the queue in time,
                # the player will disconnect due to performance
                # reasons.
                try:
                    async with timeout(180):  # 3 minutes
                        self.current = await self.songs.get()
                except asyncio.TimeoutError:
                    self.bot.loop.create_task(self.stop())
                    return

            self.voice.play(self.current, after=self.play_next_song)

            await self.next.wait()

    def play_next_song(self, error=None):
        if error:
            raise VoiceError(str(error))

        self.next.set()

    async def stop(self):
        self.songs.clear()