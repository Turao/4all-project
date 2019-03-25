import asyncio
import random
import time
from .models.location import Location
from .geocoders.opencage_async import (
    OpenCageGeocoderAsync as Geocoder
)


class Hermes():
    @staticmethod
    async def get_random_places(nplaces):
        # generate random valued (latitude, longitude) tuples
        latlon = [
            (random.uniform(-90, 90), random.uniform(-180, 180))
            for i in range(nplaces)
        ]

        results = await Geocoder(base_url='http://localhost:8080/%s').reverse_geocode_batch(latlon)

        locations = []
        for result in results:
            geometry = result.get('geometry')
            components = result.get('components')
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
            locations.append(Location(**location_data))

        print('Locations', len(locations))

        Location.bulk_create_safe(locations, batch_size=200)
        print('Locations in DB:', Location.select().count())


start = time.time()
requests = 2000
loop = asyncio.get_event_loop()
loop.run_until_complete(Hermes.get_random_places(requests))
end = time.time()

time = end - start
print('Time:', time)
rps = requests/time
print('RPS: {:.2f}'.format(rps))
rpd = rps * 24*60*60
print('Requests per day: {:.2f}'.format(rpd))
