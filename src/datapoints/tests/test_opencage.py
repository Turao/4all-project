import unittest
import asyncio
import random
from datapoints.geocoders.opencage_geocoder import (
    OpenCageGeocoder as Geocoder
)
import os


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

    @async_test
    async def test_mock_reverse_geocode_batch(self):
        print('Testing on mock server - make sure mock server is running')

        base_host = os.environ.get('MOCK_SERVER_HOST')
        base_port = os.environ.get('MOCK_SERVER_PORT')
        base_url = f'http://{base_host}:{base_port}/%s'

        geocoder = Geocoder(base_url=base_url)
        nlocations = 100
        latlon_tuples = [
            (random.uniform(-90, 90), random.uniform(-90, 90))
            for i in range(nlocations)
        ]

        results = await geocoder.reverse_geocode_batch(latlon_tuples)
        self.assertGreater(len(results), 0)
        self.assertIsNotNone(results)
