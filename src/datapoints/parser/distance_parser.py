import re
from .string_parser import StringParser


class DistanceParser(StringParser):
    distance_regex = r'(?P<distance>\d+.\d+)\s+km'
    bearing_regex = r'Bearing:\s+(?P<bearing>\d+.\d+)°'

    def parse(self, _str):
        match = re.search(self.distance_regex, _str)
        self.distance = float(match.group('distance')) if match else None
        return self.distance
