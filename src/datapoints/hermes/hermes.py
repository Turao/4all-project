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


if __name__ == '__main__':
    start = time.time()

    loop = asyncio.get_event_loop()
    
    # set defaults
    batch_size = 200
    timeout = 5
    try:
        batch_size = sys.argv[2]
        timeout = sys.argv[3]
    except Exception:
        pass
    
    hermes = Hermes(geocoder=OpenCageGeocoder())
    loop.run_until_complete(hermes.enrich(sys.argv[1], batch_size, timeout))

    end = time.time()

    time = end - start
    print('Time:', time)
