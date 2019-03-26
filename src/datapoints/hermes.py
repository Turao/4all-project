import asyncio
import time
import sys
from .parser.location_parser import LocationParser
from .models.location import Location
from .geocoders.opencage_async import (
    OpenCageGeocoderAsync as Geocoder
)


class Hermes():
    @staticmethod
    async def get_locations_from_file(f):
        # generate latitude and longitude values
        latlon_tuples = [
            (lat, lon)
            for lat, lon, distance in LocationParser().parse(f)
        ]

        latlon_tuples = latlon_tuples[:500]

        results = await Geocoder().reverse_geocode_batch(latlon_tuples)

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

        Location.bulk_create_safe(locations, batch_size=50)
        print('Locations in DB:', Location.select().count())


start = time.time()
requests = 500
loop = asyncio.get_event_loop()
loop.run_until_complete(Hermes.get_locations_from_file(sys.argv[1]))
end = time.time()

time = end - start
print('Time:', time)
rps = requests/time
print('RPS: {:.2f}'.format(rps))
rpd = rps * 24*60*60
print('Requests per day: {:.2f}'.format(rpd))