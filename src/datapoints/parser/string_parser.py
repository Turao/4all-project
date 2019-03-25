import abc


class StringParser(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def parse(self, _str):
        pass
