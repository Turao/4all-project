import re
import abc
from .string_parser import StringParser


class CoordinatesParser(StringParser, metaclass=abc.ABCMeta):
    dsm_regex = r'(?P<dsm>\d+°\d+′\d+″(N|S|W|E))'
    decimal_regex = r'(?P<decimal>-?\d+.\d+)'
    coordinates_regex = f'{dsm_regex}\s+{decimal_regex}'


class LatitudeParser(CoordinatesParser):
    latitude_regex = f'Latitude.*{CoordinatesParser.coordinates_regex}'

    def parse(self, _str):
        match = re.search(self.latitude_regex, _str)
        self.latitude = float(match.group('decimal')) if match else None
        return self.latitude


class LongitudeParser(CoordinatesParser):
    longitude_regex = f'Longitude.*{CoordinatesParser.coordinates_regex}'

    def parse(self, _str):
        match = re.search(self.longitude_regex, _str)
        self.longitude = float(match.group('decimal')) if match else None
        return self.longitude
