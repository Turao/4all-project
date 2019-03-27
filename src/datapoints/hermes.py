import asyncio
import time
import sys
from .helpers.stream import Stream
from .parser.location_parser import LocationParser
from .models.location import Location
from .geocoders.opencage_geocoder import (
    OpenCageGeocoder
)


class Hermes():
    def __init__(self, geocoder):
        self.geocoder = geocoder
        self._locations = []
        self._lock = asyncio.Lock()

    async def push(self, location):
        async with self._lock:
            self._locations.append(location)

    async def take(self, batch_size):
        try:
            while True:
                async with self._lock:
                    if len(self._locations) >= batch_size:
                        self.save_in_database(self._locations[:batch_size])
                        self._locations = self._locations[batch_size:]
                await asyncio.sleep(0.2)
        except asyncio.CancelledError:
            print('Consumer timed out')
            # could save remaining here, but since I don't have the lock
            # asking for it here could left this task running...

    async def enrich(self, filepath, batch_size):
        consumer = asyncio.create_task(self.take(batch_size))

        # send requests
        for lat, lon, distance in LocationParser().parse(filepath):
            asyncio.create_task(self.request_location(lat, lon))

        # all requests scheduled, we wait a few seconds until we timeout
        timeout_sec = 30
        await asyncio.sleep(timeout_sec)
        consumer.cancel()

    async def request_location(self, latitude, longitude):
        data = await self.geocoder.reverse_geocode(latitude, longitude)

        geometry = data.get('geometry')
        components = data.get('components')
        location_data = {
            'latitude': geometry.get('lat'),
            'longitude': geometry.get('lng'),
            '_type': components.get('_type'),
            'country': components.get('country'),
            'country_code': components.get('country_code'),
            'state': components.get('state'),
            'city': components.get('city'),
            'district': components.get('suburb'),
            'postcode': components.get('postcode'),
            'street': components.get('road'),
            'number': components.get('house_number')
        }

        await self.push(Location(**location_data))

    def save_in_database(self, locations):
        print('saving locations...')
        Location.bulk_create_safe(locations, len(locations))


    # async def enrich(self, filepath, batch_size=200):
    #     async for locations in self.request_from_file(filepath, batch_size):
    #         Location.bulk_create_safe(locations, batch_size)


    # async def request_from_file(self, filepath, batch_size=200):
    #     # read the file and extract location data from each line
    #     latlon_tuples = (
    #         (lat, lon)
    #         for lat, lon, distance in LocationParser().parse(filepath)
    #     )
    #     # batch reverse geocoding
    #     for latlon_batch in Stream.take(latlon_tuples, batch_size):
    #         yield await self.reverse_geocode_batch(latlon_batch)

    # async def reverse_geocode_batch(self, latlon_tuples):
    #     results = await self.geocoder.reverse_geocode_batch(latlon_tuples)
    #     print('got the results!')

    #     locations = []
    #     for result in results:
    #         geometry = result.get('geometry')
    #         components = result.get('components')
    #         location_data = {
    #             'latitude': geometry.get('lat'),
    #             'longitude': geometry.get('lng'),
    #             '_type': components.get('_type'),
    #             'country': components.get('country'),
    #             'country_code': components.get('country_code'),
    #             'state': components.get('state'),
    #             'city': components.get('city'),
    #             'district': components.get('suburb'),
    #             'postcode': components.get('postcode'),
    #             'street': components.get('road'),
    #             'number': components.get('house_number')
    #         }
    #         locations.append(Location(**location_data))
    #     return locations


start = time.time()

loop = asyncio.get_event_loop()
hermes = Hermes(geocoder=OpenCageGeocoder(base_url='http://localhost:8080/%s'))
loop.run_until_complete(hermes.enrich(sys.argv[1], 200))

end = time.time()

time = end - start
print('Time:', time)
# rps = requests/time
# print('RPS: {:.2f}'.format(rps))
# rpd = rps * 24*60*60
# print('Requests per day: {:.2f}'.format(rpd))
