import abc


class FileParser(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def parse(self, f):
        pass
