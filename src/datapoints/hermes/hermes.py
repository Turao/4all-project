import asyncio
import time
import sys
from .consumer import HermesConsumer
from .producer import HermesProducer
from ..geocoders.opencage_geocoder import (
    OpenCageGeocoder
)


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


start = time.time()

loop = asyncio.get_event_loop()
hermes = Hermes(geocoder=OpenCageGeocoder(base_url='http://localhost:8080/%s'))
loop.run_until_complete(hermes.enrich(sys.argv[1], 200, 5))

end = time.time()

time = end - start
print('Time:', time)
