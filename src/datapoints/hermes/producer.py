import abc
import asyncio
from ..parser.location_parser import LocationParser
from ..models.location import Location


class Producer(metaclass=abc.ABCMeta):
    def __init__(self, lock, buffer):
        self.lock = lock
        self.buffer = buffer

    async def put(self, item):
        async with self.lock:
            self.buffer.append(item)

    @abc.abstractmethod
    def produce(self):
        pass


class HermesProducer(Producer):
    def __init__(self, lock, buffer, filepath, geocoder):
        super().__init__(lock, buffer)
        self.filepath = filepath
        self.geocoder = geocoder

    def produce(self):
        # send requests
        for lat, lon, distance in LocationParser().parse(self.filepath):
            asyncio.create_task(self.request_location(lat, lon))

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

        await self.put(Location(**location_data))