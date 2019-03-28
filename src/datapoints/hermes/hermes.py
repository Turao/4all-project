import asyncio
from .consumer import HermesConsumer
from .producer import HermesProducer


class Hermes():
    def __init__(self, geocoder):
        self.geocoder = geocoder
        self._locations = []
        self._lock = asyncio.Lock()

    async def enrich(self, filepath, batch_size, timeout=None):
        producer = HermesProducer(self._lock, self._locations,
                                  filepath, self.geocoder)
        producer.produce()

        consumer = HermesConsumer(self._lock, self._locations, batch_size)
        consumer.consume()

        if timeout:
            await asyncio.sleep(timeout)
            consumer._task.cancel()
