import logging


class Logger():
    def __init__(self, name='Default Logger', level=logging.FATAL):
        self._logger = logging.getLogger(name)
        self._logger. addHandler(logging.StreamHandler())
        self._logger.setLevel(level)

    def set_level(self, level):
        self._logger.setLevel(level)