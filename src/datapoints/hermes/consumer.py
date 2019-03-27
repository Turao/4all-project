import abc
import asyncio
from ..models.location import Location 


class Consumer(metaclass=abc.ABCMeta):
    def __init__(self, lock, buffer):
        self.lock = lock
        self.buffer = buffer

    async def take(self, n):
        async with self.lock:
            if len(self.buffer) >= n:
                items = self.buffer[:n]
                self.buffer = self.buffer[n:]
                return items


class HermesConsumer(Consumer):
    def __init__(self, lock, buffer, batch_size=200):
        super().__init__(lock, buffer)
        self.batch_size = batch_size

    def consume(self):
        # we'll only schedule its execution
        # so we can asign _task and be able to cancel if needed
        self._task = asyncio.create_task(self._consume())

    async def _consume(self):
        try:
            while True:
                batch = await self.take(self.batch_size)
                if batch:
                    self.save_to_database(batch)
                await asyncio.sleep(0.2)
        except asyncio.CancelledError:
            print('Consumer timed out')
            # could save remaining here, but since I don't have the lock
            # asking for it here could left this task running...

    def save_to_database(self, batch):
        Location.bulk_create_safe(batch, len(batch))
