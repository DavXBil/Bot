import asyncio


class SongQueue(asyncio.Queue) :
    """playlist queue class"""

    def __len__(self):
        return self.qsize()

    def clear(self):
        """Clears the queue"""
        self._queue.clear()
        