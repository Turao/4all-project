from .geocoder import Geocoder
from aiohttp import ClientSession, TCPConnector
import os


class OpenCageGeocoder(Geocoder):
    def __init__(self,
                 app_key=os.environ.get('OPENCAGE_KEY'),
                 base_url='https://api.opencagedata.com/geocode/v1/json?%s'):
        self.app_key = app_key
        self.base_url = base_url

    async def reverse_geocode(self, latitude, longitude):
        url = self.base_url % 'q={}+{}&key={}'.format(latitude,
                                                      longitude,
                                                      self.app_key)
        conn = TCPConnector(limit=0)
        async with ClientSession(connector=conn) as session:
            data = await self.fetch(session, url)

            # opencage caps at 2.5k requests per day
            rate = data.get('rate')
            if rate and rate.get('remaining') == 0:
                raise RuntimeError('Rate Limit exceeded')

            # opencage returns a 200 response
            # if unable to reverse geocode
            # fortunately, they include an 'error' key
            if data and 'error' not in data:
                results = data.get('results')
                # take the first match since the api returns
                # multiple addresses (sorted by relevance)
                return results[0] if results else {}
