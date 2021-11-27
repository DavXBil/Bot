import asyncio
import itertools



class SongQueue(asyncio.Queue) :
    """playlist queue class"""
    def __getitem__(self, item):
        if isinstance(item, slice):
            return list(itertools.islice(self._queue, item.start, item.stop, item.step))
        else:
            return self._queue[item]

    def __iter__(self):
        return iter(self._queue.__iter__())

    def __len__(self):
        return self.qsize()

    def clear(self):
        self._queue.clear()

    def remove(self, index: int):
        del self._queue[index]
        