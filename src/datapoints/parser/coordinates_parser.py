import re

class CoordinatesParser():
    dsm_regex = r'(?P<dsm>\d+°\d+′\d+″(N|S|W|E))'
    decimal_regex = r'(?P<decimal>-?\d+.\d+)'
    coordinates_regex = f'{dsm_regex}\s+{decimal_regex}'

    distance_regex = r'(?P<distance>\d+.\d+)\s+km'
    bearing_regex = r'Bearing:\s+(?P<bearing>\d+.\d+)°'

    @classmethod
    def read_input(cls):
        try:
            while True:

                try:
                    latitude = cls.parse_latitude(input())
                    if latitude is None:
                        raise AttributeError('Latitude')

                    longitude = cls.parse_longitude(input())
                    if longitude is None:
                        raise AttributeError('Longitude')

                    distance = cls.parse_distance(input())
                    if distance is None:
                        raise AttributeError('Distance')

                    yield latitude, longitude, distance

                except AttributeError as e:
                    print('AttributeError:', e)
                    pass

        except EOFError:
            return

    @classmethod
    def parse_latitude(cls, _str):
        match = re.search(cls.coordinates_regex, _str)
        return float(match.group('decimal')) if match else None

    @classmethod
    def parse_longitude(cls, _str):
        match = re.search(cls.coordinates_regex, _str)
        return float(match.group('decimal')) if match else None

    @classmethod
    def parse_distance(cls, _str):
        match = re.search(cls.distance_regex, _str)
        return float(match.group('distance')) if match else None

if __name__ == '__main__':
    for latitude, longitude, distance in CoordinatesParser().read_input():
        print(latitude, longitude, distance)