import unittest
import asyncio
from datapoints.geocoders.opencage_async import (
    OpenCageGeocoderAsync as Geocoder
)


def async_test(coro):
    def wrapper(*args, **kwargs):
        loop = asyncio.new_event_loop()
        return loop.run_until_complete(coro(*args, **kwargs))
    return wrapper


class TestOpenCageGeocoderAsync(unittest.TestCase):
    @async_test
    async def test_reverse_geocoding(self):
        latitude = -30.027350
        longitude = -51.182731
        response = await Geocoder().reverse_geocode(latitude, longitude)
        self.assertIn('geometry', response)
        self.assertIn('components', response)

    @unittest.expectedFailure
    @async_test
    async def test_reverse_geocoding_invalid_latitude(self):
        latitude = -100
        longitude = -51.182731
        response = await Geocoder().reverse_geocode(latitude, longitude)
        self.assertIn('geometry', response)
        self.assertIn('components', response)