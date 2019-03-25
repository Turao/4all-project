import unittest
from ..models.location import Location


class TestLocation(unittest.TestCase):
    def setUp(self):
        Location.create_table()
        self.mock_location = {
          'latitude': -30.027350,
          'longitude': -51.182731,
          'distance': 1.0,
          'country': 'Brasil',
          'state': 'RS',
          'city': 'Porto Alegre',
          'district': 'Montserrat',
          'postcode': '90480-003',
          'street': 'Avenida Carlos Gomes',
          'number': 565,
        }

    def tearDown(self):
        Location.drop_table()

    def test_initialization_with_good_arguments(self):
        location = Location.create(**self.mock_location)
        self.assertIsInstance(location, Location)