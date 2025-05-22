import asyncio
import functools

import discord
from yt_dlp import YoutubeDL
from discord.ext import commands

class YTDLError(Exception):
    pass

class YTDLSource(discord.PCMVolumeTransformer):

    YTDL_OPTIONS = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0',
    }

    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn -af aresample=resampler=soxr',
    }

    ytdl = YoutubeDL(YTDL_OPTIONS)


    def __init__(
        self, ctx: commands.Context, source: discord.FFmpegPCMAudio, *,
        data: dict, volume: float = 0.5
        ):

        super().__init__(source, volume)

        self.requester = ctx.author
        self.channel = ctx.channel
        self.data = data
        self.uploader = data.get('uploader')
        self.uploader_url = data.get('uploader_url')
        self.title = data.get('title')
        self.thumbnail = data.get('thumbnail')
        self.tags = data.get('tags')
        self.url = data.get('webpage_url')
        self.stream_url = data.get('url')
        self.duration = self.parse_duration(int(data.get('duration')))


    # @classmethod
    # async def create_source(
    #     cls, ctx: commands.Context,
    #     search: str, *, loop: asyncio.AbstractEventLoop
    #     ):
    #     """extract info from url"""
    #
    #     partial = functools.partial(cls.ytdl.extract_info, search, download=False, process=False)
    #     data = await loop.run_in_executor(None, partial)
    #
    #     webpage_url = data['webpage_url']
    #     partial = functools.partial(cls.ytdl.extract_info, webpage_url, download=False)
    #     processed_info = await loop.run_in_executor(None, partial)
    #
    #     return cls(ctx, discord.FFmpegPCMAudio(processed_info['url'], **cls.FFMPEG_OPTIONS),
    #         data = processed_info)
    @classmethod
    async def create_source(cls, ctx, search: str, *, loop, download=False):
        loop = loop or asyncio.get_event_loop()
        partial = functools.partial(cls.ytdl.extract_info, search, download=download)
        data = await loop.run_in_executor(None, partial)

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if not download else cls.ytdl.prepare_filename(data)
        return cls(ctx, discord.FFmpegPCMAudio(filename, **cls.FFMPEG_OPTIONS), data=data)

    def parse_duration(self, duration: int):
        """parses song's duration time"""
        minutes, seconds = divmod(duration, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        duration = []
        if days > 0:
            duration.append('{} days'.format(days))
        if hours > 0:
            duration.append('{} hours'.format(hours))
        if minutes > 0:
            duration.append('{} minutes'.format(minutes))
        if seconds > 0:
            duration.append('{} seconds'.format(seconds))

        return ', '.join(duration)
