import sys

from .file_parser import FileParser
from .coordinates_parser import LatitudeParser, LongitudeParser
from .distance_parser import DistanceParser


class LocationParser(FileParser):
    def parse(self, f):
        _strs = [f.readline() for i in (range(3))]
        # readline does not raise EOF exceptions
        # so we stop if all strings were empty
        if all([len(s) == 0 for s in _strs]):
            raise EOFError

        self.latitude = LatitudeParser().parse(_strs[0])
        self.longitude = LongitudeParser().parse(_strs[1])
        self.distance = DistanceParser().parse(_strs[2])
        return self.latitude, self.longitude, self.distance


if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        # try:
        while True:
            try:
                print(LocationParser().parse(f))
            except EOFError:
                break

