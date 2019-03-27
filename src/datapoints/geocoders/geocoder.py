import asyncio
import abc
from .http_requester import HTTPRequester


class Geocoder(HTTPRequester, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def reverse_geocode(self, latitude, longitude):
        pass

    async def reverse_geocode_batch(self, latlon_tuples):
        tasks = (
            self.reverse_geocode(lat, lon)
            for lat, lon in latlon_tuples
        )
        results = await asyncio.gather(*tasks)
        return results
