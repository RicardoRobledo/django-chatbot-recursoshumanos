from abc import ABC, abstractmethod


__author__ = 'Ricardo'
__version__ = '0.1'


__all__ = ['BaseState']


class BaseState(ABC):
    """
    This class define the generic functionality to add in states
    """

    @abstractmethod
    def send_message():
        pass

    @abstractmethod
    def transition():
        pass
