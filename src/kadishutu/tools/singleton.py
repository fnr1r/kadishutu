from abc import ABC


class AbstractSingleton(ABC):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(AbstractSingleton, cls).__new__(cls)
        return cls.instance
