"""
Class     : Record
tipologia : Classe astratta
"""
from abc import ABCMeta, abstractmethod
class Record(metaclass=ABCMeta):
    def __init__(self):
        pass
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        pass
    def __repr__(self):
        raise NotImplementedError()
    def __str__(self):
        raise NotImplementedError()
