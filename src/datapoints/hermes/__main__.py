import asyncio
import sys
import time
from .hermes import Hermes
from ..geocoders.opencage_geocoder import (
    OpenCageGeocoder
)


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